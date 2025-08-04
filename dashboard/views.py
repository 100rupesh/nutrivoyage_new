from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from accounts.models import User
from utils.decorators import role_required
from clients.models import ClientDetails
from appointments.models import Appointment,DietPlan
from django.utils import timezone
from datetime import timedelta

def get_appointment_single_diet_plan(app_id:list):
    count_incomplete_diet_plan=0
    for id in app_id:
        appointment_first_diet_plan=DietPlan.objects.filter(appointment=id)
        if len(appointment_first_diet_plan)<=1:
            count_incomplete_diet_plan+=1
    return count_incomplete_diet_plan

# @login_required(login_url='login')
@role_required('DIETICIAN','ADMIN')
def dashboard(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    print((str(request.user.role)))
    user=str(request.user)
    usr=User.objects.filter(username=user)
    print(usr)
    client=ClientDetails.objects.filter(created_by=request.user)
    client_count=len(client)
    
    appointment=Appointment.objects.filter(created_by=request.user,datetime__gte=thirty_days_ago)
    pending_appointments=get_appointment_single_diet_plan(appointment)
    print("APP",pending_appointments)
    # appointment_current_month=Appointment.objects.filter(datetime__gte=thirty_days_ago)
    appointment_count=len(appointment)
    dietician_name=request.user.first_name
    return render(request,'dashboard/dashboard.html',{'dietician_name':dietician_name,'client_count':client_count,'appointment_count':appointment_count,'client':client[:2],'appointment':appointment[:2],'pending_appointments':pending_appointments})