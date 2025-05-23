from django.shortcuts import render

# Create your views here.
from utils.decorators import role_required

# @login_required(login_url='login')
@role_required('NORMAL')
def client(request):
    return render(request,'clients/client.html')


@role_required('NORMAL')
def client_activity(request):
    return render(request,'clients/client_activity.html')

@role_required('NORMAL')
def client_plan(request):
    return render(request,'clients/client_plan.html')


@role_required('NORMAL')
def client_progress(request):
    return render(request,'clients/client_progress.html')

@role_required('NORMAL')
def client_appointment(request):
    return render(request,'clients/client_appointment.html')


@role_required('NORMAL')
def client_message(request):
    return render(request,'clients/client_message.html')

@role_required('NORMAL')
def client_meal(request):
    return render(request,'clients/client_mealtracking.html')

# @role_required('NORMAL')
# def client(request):
#     return render(request,'clients/client_form.html')