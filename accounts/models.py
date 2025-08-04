from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import ClientDetails

class User(AbstractUser):
    # Role choices
    ROLE_CHOICES = [
        ('NORMAL', 'Normal User'),
        ('DIETICIAN', 'Dietician'),
        ('MANAGER', 'Manager'),
        ('SENIOR_MANAGER', 'Senior Manager'),
        ('ADMIN', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='NORMAL')

    # Hierarchical relationships
    dietician = models.ForeignKey('self', null=True, blank=True, related_name='users', on_delete=models.SET_NULL)
    manager = models.ForeignKey('self', null=True, blank=True, related_name='dieticians', on_delete=models.SET_NULL)
    senior_manager = models.ForeignKey('self', null=True, blank=True, related_name='managers', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_dietician(self):
        return self.role == 'DIETICIAN'
    
    def is_admin(self):
        return self.role == 'ADMIN'
    def is_client(self):
        return self.role == 'NORMAL'


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role=="NORMAL":
#         ClientDetails.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    c_details=ClientDetails.objects.filter(user=instance)
    print("C",c_details)

    if c_details:
        profile=instance.client_profile
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.save() 


