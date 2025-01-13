import csv
import json
import logging
import openpyxl

from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.signals import user_login_failed

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from datetime import date, datetime, timedelta

import sentry_sdk
from .forms import CustomPasswordChangeForm
from coreapp.models import Report

from sentry_sdk import capture_message, capture_exception, set_context, set_user  # Sentry integration

# Logger setup for login-related events
logger = logging.getLogger('login')

User = get_user_model()

#*******************************************************************HELPER FUNCTIONS *****************************************************
@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    logger = logging.getLogger('django')
    username = credentials.get('username', 'UNKNOWN')
    ip = get_client_ip(request)
    logger.warning(
        f"Failed login attempt: username='{username}', IP='{ip}', time={now()}"
    )

# Helper Function to Extract Client IP
def get_client_ip(request):
    """Extract client IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def is_team(user):
    """Check if the user is a LTW team member."""
    return user.groups.filter(name="Team").exists()

def custom_serializer(obj):
    """
    Custom serializer to handle datetime and date objects for JSON export.
    """
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as 'YYYY-MM-DD HH:MM:SS'
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
    raise TypeError(f"Type {type(obj)} not serializable")

def trigger_error(request):
    set_user({
        "id": 123,
        "email": "user@example.com",
        "username": "testuser",
    })

    # Add custom context
    set_context("order_details", {
        "order_id": 456,
        "status": "pending",
    })

    # Add tags
    sentry_sdk.set_tag("feature", "checkout")
    sentry_sdk.set_tag("priority", "high")

    # Trigger an error
    capture_message("Test error with tags and context")
    raise Exception("Triggered error for testing Sentry.")


# Custom Rate Limiter Function
def custom_rate_limiter(ip, username=None, limit=5, period=60, block_duration=300):
    """
    Custom rate limiter function to limit login attempts per IP or username.
    - Tracks attempts in a sliding window of `period` seconds.
    - Allows up to `limit` attempts within the window.
    - Dynamically blocks IPs for `block_duration` seconds after repeated offenses.
    """
    # Blocked IP cache key
    block_key = f"blocked_ip:{ip}"
    if cache.get(block_key):
        logger.warning(f"IP {ip} is temporarily blocked.")
        return True  # Block requests from this IP

    # Track login attempts cache key
    attempt_key = f"login_attempts:{ip}"
    if username:
        attempt_key += f":{username}"

    # Get recent attempts
    attempts = cache.get(attempt_key, [])
    current_time = now()

    # Keep attempts within the sliding window
    recent_attempts = [ts for ts in attempts if (current_time - ts).seconds < period]
    recent_attempts.append(current_time)  # Add current attempt

    # Update cache with recent attempts
    cache.set(attempt_key, recent_attempts, timeout=period)

    # If rate limit exceeded, block the IP
    if len(recent_attempts) > limit:
        logger.warning(f"Rate limit exceeded for IP={ip}, Username={username}")
        cache.set(block_key, True, timeout=block_duration)  # Temporarily block this IP
        capture_message(f"IP {ip} temporarily blocked for repeated offenses.")  # Log to Sentry
        return True

    return False  # Allow login attempt

def some_view(request):
    # Set user information
    if request.user.is_authenticated:
        set_user({
            "id": request.user.id,
            "email": request.user.email,
            "username": request.user.username,
        })
    else:
        set_user(None)  # Anonymous user

    # Add custom context
    set_context("request_metadata", {
        "ip_address": get_client_ip(request),
        "user_agent": request.META.get("HTTP_USER_AGENT"),
    })
    return HttpResponse("View executed!")

# ********************************************************************* HELPER FUNCTIONS *************************************************************


@method_decorator(ratelimit(key='ip', rate='5/m', block=False), name='dispatch')
class CustomLoginView(LoginView):
    """
    Custom login view with rate limiting, logging, and Sentry integration.
    """
    def dispatch(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        username = request.POST.get('username', None)

        is_rate_limited = custom_rate_limiter(ip, username=username, limit=5, period=60, block_duration=300)
        if is_rate_limited:
            # Gracefully handle cache failures
            # Log the event
            logger.warning(f"Blocked login attempt: IP={ip}, Username={username}")
            capture_message(f"Rate limit triggered: IP={ip}, Username={username}")
            logger.error(f"Rate limiter cache failure: {e}")
            capture_exception(e)  # Log to Sentry

            is_rate_limited = False  # Allow login if cache fails

            # Add an error message to the request
            messages.error(request, "You have exceeded the allowed number of requests. Please try again later.")

            # Re-render the login page with the message
            return super().get(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user  # Get the logged-in user
        if user.is_superuser or is_team(user):  # Redirect superusers and team members
            return '/clients/'
        return f'/reports/{user.id}/'  # Redirect clients to their reports


def export_to_csv(reports, fields):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'

    writer = csv.writer(response)
    writer.writerow(fields)  # Use visible fields as headers

    for report in reports:
        row = [getattr(report, field, '') for field in fields]
        writer.writerow(row)

    return response


def export_to_excel(reports, fields):
    """
    Export the reports to an Excel file.
    """
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Reports"

    # Write headers
    sheet.append(fields)

    # Write data rows
    for report in reports:
        row = []
        for field in fields:
            value = getattr(report, field, '')
            # Check if value is a datetime object
            if isinstance(value, datetime):
                # Convert timezone-aware datetime to naive datetime
                value = value.astimezone(tz=None).replace(tzinfo=None)
            row.append(value)
        sheet.append(row)

    workbook.save(response)
    return response


def export_to_json(reports, fields):
    """
    Export the reports to a JSON file using Django's built-in serializers.
    """
    # Serialize the queryset
    data = reports.values(*fields)  # Extract only the required fields as dictionaries

    # Return a JSON response
    response = JsonResponse(list(data), safe=False)  # Convert QuerySet to a list for JSON
    response['Content-Disposition'] = 'attachment; filename="reports.json"'
    return response


@login_required
def list_clients(request):
    """View to list all clients for admins and team members."""
    if not (request.user.is_superuser or is_team(request.user)):
        return redirect('view_client_reports', client_id=request.user.id)

    Group = apps.get_model('auth', 'Group')
    try:
        client_group = Group.objects.get(name="Client")
        clients = User.objects.filter(groups=client_group)
    except Group.DoesNotExist:
        clients = []
        error = "The 'Client' group does not exist. Please create it in the admin panel."
        return render(request, "list_clients.html", {"clients": [], "error": error})

    return render(request, "list_clients.html", {"clients": clients, "active_page": "list_clients", "error": None})


@login_required
def view_client_reports(request, client_id):
    """
    View and manage reports for a specific client.
    """
    # Access control: Ensure proper permissions
    if request.user.is_superuser or is_team(request.user):
        client = get_object_or_404(User, id=client_id)
    else:
        if request.user.id != client_id:
            return redirect("view_client_reports", client_id=request.user.id)
        client = request.user

    # Fetch reports
    reports = Report.objects.filter(user=client).order_by("-creation_date")

    # Date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        try:
            reports = reports.filter(creation_date__gte=start_date)
        except ValueError:
            start_date = None

    if end_date:
        try:
            # Add one day minus a microsecond to include the entire day
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)
            reports = reports.filter(creation_date__lte=end_date_obj)
        except ValueError:
            end_date = None

    # Define date fields
    date_fields = ["creation_date", "updated_at", "bday"]

    # Sorting
    sort_field = request.GET.get('sort_field', 'id')
    sort_order = request.GET.get('sort_order', 'asc')

    if sort_field and sort_order in ["asc", "desc"]:
        sort_query = f"{'' if sort_order == 'asc' else '-'}{sort_field}"
        reports = reports.order_by(sort_query)

    # Define visible fields dynamically
    fields = [field.name for field in Report._meta.get_fields()]
    exclude_fields = ["user", "document", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_assignment", "updated_at", "description", "id"]
    fields = [field for field in fields if field not in exclude_fields]

    # Anonymize private fields for display
    anonymized_reports = [report.anonymize() for report in reports]

    # Search by specific field
    field = request.GET.get('field', None)
    search_query = request.GET.get('search_query', None)
    if field and search_query:
        try:
            reports = reports.filter(**{f"{field}__icontains": search_query})
        except Exception as e:
            logging.warning(f"Failed to filter by field {field} with query {search_query}: {e}")


    # Active Filters
    active_filters = []
    for key, value in request.GET.items():
        if key == "sort_field" and sort_order:
            try:
                verbose_name = Report._meta.get_field(sort_field).verbose_name
                active_filters.append({
                    "name": f"Sort by {verbose_name}",
                    "value": "Asc" if sort_order == "asc" else "Desc",
                    "query_params": {
                        "sort_field": None,  # Remove sort_field
                        "sort_order": None   # Remove sort_order
                    }
                })
            except Exception:
                active_filters.append({
                    "name": "Sort Field",
                    "value": "Asc" if sort_order == "asc" else "Desc",
                    "query_params": {
                        "sort_field": None,
                        "sort_order": None
                    }
                })

        elif key == "start_date" and start_date:
            active_filters.append({
                "name": "Start Date",
                "value": start_date,
                "query_params": {"start_date": None}  # Remove start_date
            })

        elif key == "end_date" and end_date:
            active_filters.append({
                "name": "End Date",
                "value": end_date,
                "query_params": {"end_date": None}  # Remove end_date
            })

        elif key in fields and value.strip():  # For field-based searches
            try:
                verbose_name = Report._meta.get_field(key).verbose_name
                active_filters.append({
                    "name": f"Search in {verbose_name}",
                    "value": f'"{value}"',
                    "query_params": {"field": None, "search_query": None}  # Remove both field and search_query
                })
            except Exception:
                active_filters.append({
                    "name": f"Search in {key.title()}",
                    "value": f'"{value}"',
                    "query_params": {"field": None, "search_query": None}
                })

    # Ensure `field` and `search_query` filters are included together
    if field and search_query:
        try:
            verbose_name = Report._meta.get_field(field).verbose_name
            active_filters.append({
                "name": f"Search in {verbose_name}",
                "value": f'"{search_query}"',
                "query_params": {"field": None, "search_query": None}
            })
        except Exception:
            active_filters.append({
                "name": f"Search in {field.title()}",
                "value": f'"{search_query}"',
                "query_params": {"field": None, "search_query": None}
            })

    # Pagination logic
    paginator = Paginator(reports, 9)  # Show 10 reports per page
    page = request.GET.get('page')

    try:
        paginated_reports = paginator.page(page)
    except PageNotAnInteger:
        paginated_reports = paginator.page(1)
    except EmptyPage:
        paginated_reports = paginator.page(paginator.num_pages)

    return render(
        request,
        "view_reports.html",
        {
            "active_page": "view_reports",
            "client": client,
            "reports": paginated_reports,
            "fields": fields,
            "date_fields": date_fields,
            "start_date": start_date,
            "end_date": end_date,
            "active_filters": active_filters,  # Pass active filters to the template
            "model": Report,  # Pass the model for verbose name lookup
            "search_query": search_query or "",  # Default to an empty string if not present
            "field": field,
        },
    )


@login_required
def export_reports(request, format):
    """
    Export reports exactly as displayed in the table.
    """
    client_id = request.GET.get("client_id")

    # Validate the client_id
    if not client_id:
        return HttpResponse("Missing client_id parameter.", status=400)

    try:
        client = get_object_or_404(User, id=int(client_id))
    except (ValueError, TypeError):
        return HttpResponse("Invalid client_id parameter.", status=400)

    # Fetch reports for the client
    reports = Report.objects.filter(user=client)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Apply date filters if provided
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            reports = reports.filter(creation_date__gte=start_date)
        except ValueError:
            return HttpResponse("Invalid start date format.", status=400)

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            reports = reports.filter(creation_date__lte=end_date)
        except ValueError:
            return HttpResponse("Invalid end date format.", status=400)
        
    # Apply sorting
    sort_field = request.GET.get('sort_field', 'id')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_field and sort_order in ["asc", "desc"]:
        sort_query = f"{'' if sort_order == 'asc' else '-'}{sort_field}"
        reports = reports.order_by(sort_query)

    # Apply search filters
    field = request.GET.get('field', None)
    search_query = request.GET.get('search_query', None)
    if field and search_query:
        try:
            reports = reports.filter(**{f"{field}__icontains": search_query})
        except Exception as e:
            logging.warning(f"Failed to filter by field {field} with query {search_query}: {e}")

    # Select only the visible fields
    fields = request.GET.get("fields", "").split(",")

    # Export logic
    if format == 'csv':
        return export_to_csv(reports, fields)
    elif format == 'excel':
        return export_to_excel(reports, fields)
    elif format == 'json':  
        return export_to_json(reports, fields)
    else:
        return HttpResponse("Invalid format specified.", status=400)



class CustomPasswordChangeView(PasswordChangeView):
    """
    Subclass the built-in PasswordChangeView to handle password changes
    with Django's PasswordChangeForm.
    """
    form_class = CustomPasswordChangeForm
    template_name = "change_password.html"
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        print("Form is valid, saving changes...")
        messages.success(self.request, "Your password was successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        # Highlight the sidebar
        context = super().get_context_data(**kwargs)
        context["active_page"] = "change_password"
        return context


# Get the webhook logger
logger = logging.getLogger('webhook')

# To integrate Leads from Zapier directly to my django BO
@csrf_exempt
def zapier_webhook(request):
    logger = logging.getLogger("webhook")

    if request.method != "POST":
        logger.warning("Invalid request method received. Must be POST. ")
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Log request headers and body for debugging
        logger.debug(f"Received headers: {request.headers}")
        logger.debug(f"Received body: {request.body.decode('utf-8')}")

        # Parse JSON payload
        payload = json.loads(request.body)
        logger.debug(f"Parsed payload: {payload}")

        # Validate critical fields
        mandatory_fields = ["user", "email", "phone", "name", "lead_validation"]
        missing_fields = [field for field in mandatory_fields if field not in payload]
        if missing_fields:
            logger.error(f"Missing mandatory fields: {missing_fields}")
            return JsonResponse( 
                {"error": "Missing mandatory fields.", "missing_fields": missing_fields},
                status=400,
            )

        # Validate user
        username = payload.get("user")
        try:
            user = User.objects.get(username=username)  # Adjust field if using `id` or `email`
        except ObjectDoesNotExist:
            logger.error(f"User with identifier '{username}' not found.")
            return JsonResponse(
                {"error": f"User with identifier '{username}' not found."},
                status=404,
            )
        
        email = payload.get("email")
        phone = payload.get("phone")
        # Check for duplicates based on email and phone
        is_email_duplicate = Report.objects.filter(email=email, user__username=username).exists()
        is_phone_duplicate = Report.objects.filter(phone=phone, user__username=username).exists()

        # Validate lead_validation and update the value
        lead_validation = payload.get("lead_validation")
        duplicate_messages = []
        if lead_validation not in [choice[0] for choice in Report.LeadValidation.choices]:
            logger.error(f"Invalid 'lead_validation' value: {payload['lead_validation']}")
            return JsonResponse(
                {"error": f"Invalid 'lead_validation' value: {payload['lead_validation']}"},
                status=400,
            )
        
        final_lead_validation = lead_validation 
        if lead_validation == "Filtered":  # Checking for duplicates
            if is_email_duplicate:
                duplicate_messages.append("Duplicate by email")
            if is_phone_duplicate:
                duplicate_messages.append("Duplicate by phone")
            if duplicate_messages:
                final_lead_validation = "Filtered,Duplicated"
        elif lead_validation == "Valid":
            if is_email_duplicate:
                duplicate_messages.append("Duplicate by email")
            if is_phone_duplicate:
                duplicate_messages.append("Duplicate by phone")
            if duplicate_messages:
                final_lead_validation = "Duplicated"
        else:
            # Default to the payload's value if no additional logic is required
            final_lead_validation = "Valid"

        
        # Dynamically map fields from the payload to the Report model
        report_data = {}
        for field in Report._meta.get_fields():
            field_name = field.name
            if field_name in payload:  # Only populate fields present in the payload
                report_data[field_name] = payload[field_name]

        # Update fields extra logics
        report_data["user"] = user
        report_data["lead_validation"] = final_lead_validation
        report_data["description"] = json.dumps(payload)  # Save the raw payload

        # Save the report
        report = Report.objects.create(**report_data)
        logger.info(f"Report created successfully: ID {report.id} for user {username}")
        # Return success response
        return JsonResponse({
            "message": "Report created successfully",
            "report_id": report.id,
            "lead_validation": final_lead_validation,
            "duplicates": duplicate_messages
        }, status=201)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}")
        return JsonResponse({"error": "Invalid JSON", "details": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)
