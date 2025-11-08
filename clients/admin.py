from django.contrib import admin

# Register your models here.
from .models import ClientDetails,DailyHealthRecord

admin.site.register(ClientDetails)

@admin.register(DailyHealthRecord)
class DailyHealthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','sleep_hours', 'weight', 'food_calories')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)
