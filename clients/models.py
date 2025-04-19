from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from datetime import date

class ClientDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(blank=True,null=True)  # Date of Birth
    contact_no = models.CharField(max_length=15,blank=True,null=True)
    email_id = models.EmailField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    date_of_creation = models.DateField(auto_now_add=True,blank=True,null=True)  # Automatically set to the current date when the record is created
    notes = models.TextField(blank=True, null=True)
    height = models.FloatField(blank=True,null=True)  # Height in cm (or meters depending on your preference)
    weight = models.FloatField(blank=True,null=True)  # Weight in kg
    medical_condition = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    client_type = models.CharField(max_length=10, choices=[('KVO', 'KVO'), ('Personal', 'Personal'), ('Other', 'Other')],blank=True)

    @property
    def age(self):
        """Compute and return the age based on date of birth."""
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    @property
    def bmi(self):
        """Compute and return the BMI based on height and weight."""
        # Assuming height is in cm and weight is in kg, BMI = weight (kg) / (height (m) ^ 2)
        height_in_meters = self.height / 100  # Convert cm to meters
        return self.weight / (height_in_meters ** 2)

    def __str__(self):
        return f"{self.user}"
