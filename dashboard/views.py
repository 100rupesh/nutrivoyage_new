from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from accounts.models import User
from utils.decorators import role_required

# @login_required(login_url='login')
@role_required('DIETICIAN')
def dashboard(request):
    print((str(request.user.role)))
    user=str(request.user)
    usr=User.objects.filter(username=user)
    print(usr)
    dietician_name=request.user.first_name
    return render(request,'dashboard/dashboard.html',{'dietician_name':dietician_name})