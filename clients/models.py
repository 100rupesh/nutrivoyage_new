from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from datetime import date

class ClientDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile',blank=True,null=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True,limit_choices_to={'role': "DIETICIAN"})
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
    medications = models.TextField(blank=True, null=True)
    chief_complaints = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    client_type = models.CharField(max_length=10, choices=[('KVO', 'KVO'), ('Personal', 'Personal'), ('Other', 'Other')],blank=True)
    DIET_PREFERENCES = [
    ('veg', 'Vegetarian'),
    ('eggetarian', 'Eggetarian'),
    ('nonveg', 'Non-Vegetarian'),
    ('vegan', 'Vegan'),
    ('keto', 'Keto'),
    ('paleo', 'Paleo'),
]
    diet_preference = models.CharField(
        max_length=15,  # ensure it's large enough
        choices=DIET_PREFERENCES,
        default='veg',
        null=True,
        blank=True
    )

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
        return self.weight / ((height_in_meters) ** 2)

    def __str__(self):
        return f"{self.user}"
    

# from django.db import models
# from django.contrib.auth.models import User

class DailyHealthRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_health',blank=True,null=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True,limit_choices_to={'role': "DIETICIAN"})


    date = models.DateField(default=date.today)

    # Workout data
    workout_type = models.CharField(max_length=100, blank=True, null=True)
    # workout_duration = models.PositiveIntegerField(help_text="Duration in minutes", blank=True, null=True)
    workout_calories = models.PositiveIntegerField(help_text="Calories burned during workout", blank=True, null=True)

    # Sleep data
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, help_text="Hours of sleep", blank=True, null=True)

    # Weight tracking
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kilograms", blank=True, null=True)

    # Food intake
    food_calories = models.PositiveIntegerField(help_text="Calories consumed from food", blank=True, null=True)

    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'created_at')
        verbose_name = "Daily Health Record"
        verbose_name_plural = "Daily Health Records"

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    @property
    def net_calories(self):
        """Calories consumed minus burned."""
        burned = self.workout_calories or 0
        consumed = self.food_calories or 0
        return consumed - burned

