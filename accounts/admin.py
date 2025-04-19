from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    # list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'is_staff']
    # list_filter = ['is_staff', 'is_active', 'date_of_birth']
    # search_fields = ['username', 'email']
    # ordering = ['username']

    # You can add any additional fieldsets or forms as needed
    list_filter = ['is_staff', 'is_active']
    
    # Add the custom fields to the admin search fields
    search_fields = ['username', 'email']
    
    # Fieldsets define the fields in the change form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'dietician','manager','senior_manager')}),
    )

    # The form to use for adding a new user (so it includes the custom fields)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'dietician','manager','senior_manager')}),
    )

admin.site.register(User, CustomUserAdmin)
