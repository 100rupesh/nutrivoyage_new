from django.shortcuts import render

# Create your views here.
from utils.decorators import role_required

# @login_required(login_url='login')
@role_required('DIETICIAN')
def client(request):
    return render(request,'clients/client_form.html')