from django.db import models
from django.contrib.auth.models import User
from datetime import date
from simple_history.models import HistoricalRecords

class Report(models.Model):
    """
    Represents a lead report associated with a user. This model captures personal, financial, and additional metadata 
    for generating user reports.
    """

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Associated Client")

    # General Fields
    id_ltw = models.PositiveIntegerField(null=True, blank=True, verbose_name="LTW ID") # User-specific report ID
    class LeadValidation(models.TextChoices):# Enum for Lead Type
        VALID = 'Valid', 'Valid Lead'
        FILTERED = 'Filtered', 'Filtered Lead'
        DUPLICATED = 'Duplicated', 'Duplicated Lead'
        FILTERED_DUPLICATED = 'Filtered,Duplicated', 'Filtered and Duplicated'

    lead_validation = models.CharField(
        max_length=50,  # Increased length to accommodate combined values
        choices=LeadValidation.choices,
        default=LeadValidation.VALID,
        verbose_name="Lead Validation",
    )
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Lead Date")  # Record creation date
    api_response = models.CharField(max_length=255, null=True, blank=True, verbose_name="API Response")  # Repurposed
    description = models.TextField(null=True, blank=True, verbose_name="Raw JSON Payload")  # New field for raw JSON
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")  # Auto-updates when a record changes

    # Private Fields (Partially Obfuscated on Anonymization)
    email = models.EmailField(db_index=True, verbose_name="Email")
    phone = models.CharField(max_length=15, db_index=True, verbose_name="Phone Number")
    name = models.CharField(max_length=100, db_index=True, verbose_name="First Name")
    last_name = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Last Name")
    tax_id = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Tax ID")
    bday = models.DateField(null=True, blank=True, db_index=True, verbose_name="Birth Date")
    postal_code = models.CharField(max_length=10, db_index=True, null=True, blank=True, verbose_name="Postal Code")

    # Additional Details
    age = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Age")
    district = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="District")
    city = models.CharField(max_length=80, db_index=True, null=True, blank=True, verbose_name="City")
    nationality = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Nationality")
    marital_status = models.CharField(
        max_length=20,
        null=True,
        db_index=True,
        choices=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
        ],
        verbose_name="Marital Status",
    )
    education_level = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Education Level")
    company_name = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Company Name")
    debt_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True, verbose_name="Debt Amount")
    vehicle_type = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Vehicle Type")
    product = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Product")
    mortgage_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True, verbose_name="Mortgage Amount")
    holder_status_1 = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="First Holder Status")
    holder_status_2 = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Second Holder Status")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_index=True, verbose_name="Interest Rate")
    deadline = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Deadline (in days)")
    housing = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="House Type")
    course_name = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Course")
    energy_supplier = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Energy Supplier")

    # Enum for Language (Country Codes)
    class LanguageCode(models.TextChoices):
        ENGLISH = 'EN', 'English'
        SPANISH = 'ES', 'Spanish'
        FRENCH = 'FR', 'French'
        GERMAN = 'DE', 'German'
        DUTCH = 'NL', 'Dutch'
        PORTUGUESE = 'PT', 'Portuguese'
        POLISH = 'PL', 'Polish'
        UKRAINIAN = 'UA', 'Ukrainian'
        LITHUANIAN = 'LT', 'Lithuanian'

    language = models.CharField(
        max_length=2,
        choices=LanguageCode.choices,
        null=True,
        verbose_name="LP Language",
    )


    # Countable Fields
    number_of_holders = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Number of Holders")
    number_of_vehicles = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Number of Vehicles")
    number_of_employees = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Number of Employees")
    contract_years = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Contract Years")
    family_members = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Family Members")
    income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True, verbose_name="Family Income")
    number_of_credits = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Number of Credits")

    # Boolean Fields
    is_interested = models.BooleanField(null=True, db_index=True, verbose_name="Is Interested?")
    is_owner = models.BooleanField(null=True, db_index=True, verbose_name="Is Owner?")
    on_time_payments = models.BooleanField(null=True, db_index=True, verbose_name="Pays On Time?")
    has_credit_card = models.BooleanField(null=True, db_index=True, verbose_name="Has Credit Card?")
    has_debt = models.BooleanField(null=True, db_index=True, verbose_name="Has Debt?")

    # Marketing UTM Fields
    utm_source = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Source")
    utm_medium = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Medium")
    utm_campaign = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Campaign")
    utm_content = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Content")
    utm_term = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Term")
    utm_assignment = models.CharField(max_length=80, null=True, blank=True, db_index=True, verbose_name="Utm Assignment")

    # Documents
    document = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        verbose_name="Uploaded Document",
        help_text="Allowed formats: PDF, DOCX, PNG, JPG",
    )

    # Historical Tracking
    history = HistoricalRecords()  # Tracks all changes to this model

    # Metadata
    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        db_table = "report"
        indexes = [
            models.Index(fields=["email"], name="idx_email"),
            models.Index(fields=["phone"], name="idx_phone"),
            models.Index(fields=["postal_code"], name="idx_postal_code"),
            models.Index(fields=["city"], name="idx_city"),
        ]
        ordering = ["-creation_date"]

    def __str__(self):
        return f"{self.user} {self.LeadValidation} Lead - {self.pk} - {self.name} {self.last_name}"

    # Utility Methods
    def calculate_age(self):
        """
        Calculates the age based on the birth date (bday).
        """
        if not self.bday:
            return None
        today = date.today()
        return today.year - self.bday.year - ((today.month, today.day) < (self.bday.month, self.bday.day))
    
    def anonymize(self):
        """
        Returns a dictionary of all fields, with private fields anonymized.
        """
        def anonymize_field(value, mask_length=3):
            if value:
                return value[:mask_length] + '***'
            return None

        # Anonymize only private fields
        anonymized_data = {
            "email": anonymize_field(self.email),
            "phone": anonymize_field(self.phone),
            "name": anonymize_field(self.name),
            "last_name": anonymize_field(self.last_name),
            "tax_id": anonymize_field(self.tax_id),
            "postal_code": anonymize_field(self.postal_code, mask_length=4),
        }

        # Include all non-private fields as is
        all_fields = {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if field.name not in anonymized_data
        }

        # Combine anonymized and non-anonymized fields
        return {**all_fields, **anonymized_data}



    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate and update the age field.
        """
        self.age = self.calculate_age()  # Update the age field before saving
        '''if not self.ltw_id:  # Only assign `ltw_id` if it is not already set
            # Get the highest `ltw_id` for the same user
            last_report = Report.objects.filter(user=self.user).order_by('-ltw_id').first()
            self.ltw_id = (last_report.ltw_id + 1) if last_report and last_report.ltw_id else 1 ADD LATER TO UNSURE GREAT SPECIF CLIENT NUMBERING''' 

        super().save(*args, **kwargs)
