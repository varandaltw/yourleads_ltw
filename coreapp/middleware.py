from django.utils.timezone import activate
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and has a timezone preference
        if request.user.is_authenticated:
            user_timezone = request.user.timezone  # Assuming a `timezone` field exists in the User model
        else:
            # Fallback to default timezone from settings
            user_timezone = settings.TIME_ZONE

        # Activate the user's timezone for the request
        activate(user_timezone)

        # Proceed with the response
        response = self.get_response(request)
        return response
    

    # change logic doenst make sense considering the user model has no timezone field. change this to help in the display of fields and stuff in the htlms
