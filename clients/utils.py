from datetime import timedelta
from django.utils.timezone import now
from .models import DailyHealthRecord
from django.db import models



def calculate_client_summary(user):
    records = DailyHealthRecord.objects.filter(user=user).order_by('-date')
    if not records.exists():
        return None

    last_7_days = records.filter(date__gte=now().date() - timedelta(days=7))
    print("AVG",last_7_days)

    # Compute basic stats
    start_weight = records.last().weight or 0
    current_weight = records.first().weight or 0
    weight_change = round(current_weight - start_weight, 2)

    avg_calories = last_7_days.aggregate(avg=models.Avg('food_calories'))['avg'] or 0
    avg_sleep = last_7_days.aggregate(avg=models.Avg('sleep_hours'))['avg'] or 0

    # Simple compliance logic (based on meal/sleep logging frequency)
    compliance_ratio = (last_7_days.count() / 7) * 100
    if compliance_ratio >= 80:
        status = 'Active'
        color = 'green'
    elif compliance_ratio >= 40:
        status = 'Irregular'
        color = 'orange'
    else:
        status = 'Inactive'
        color = 'red'

    return {
        'user': user,
        'weight_change': weight_change,
        'avg_calories': round(avg_calories, 1),
        'avg_sleep': round(avg_sleep, 1),
        'compliance': round(compliance_ratio),
        'status': status,
        'color': color
    }
