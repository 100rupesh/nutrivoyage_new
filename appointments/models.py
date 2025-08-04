from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from accounts.models import User



class Appointment(models.Model):
    FREE = 'free'
    PAID = 'paid'

    APPOINTMENT_TYPE_CHOICES = [
        (FREE, 'Free'),
        (PAID, 'Paid'),
    ]

    datetime = models.DateTimeField(auto_now_add=True)
    appointment_type = models.CharField(
        max_length=10,
        choices=APPOINTMENT_TYPE_CHOICES,
        default=FREE
    )
    notes = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': "NORMAL"})
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='appointments_created',limit_choices_to={'role': "DIETICIAN"})

    def __str__(self):
        return f"{self.patient} - {self.datetime.strftime('%Y-%m-%d %H:%M')} - {self.id}"
    


class DietPlan(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointment')
    breakfast = models.TextField()
    lunch = models.TextField()
    snacks = models.TextField()
    dinner = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    diet_no=models.IntegerField()

    def __str__(self):
        return f"Diet Plan for {self.appointment.patient} on {self.appointment.datetime.strftime('%Y-%m-%d')}"