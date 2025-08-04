from django.shortcuts import render,redirect,get_object_or_404
from .models import ClientDetails
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages

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


@role_required('DIETICIAN')
def create_client(request):
    if request.method == 'POST':
        # Fetch the logged-in user
        user = request.user
        f=request.POST.get('first_name')
        g=request.POST.get('gender')
        print("First Name:\t",f)
        print("Gender Name:\t",g)
        username=request.POST.get('username')
        password=str(123456)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('create_client')  # Redirect back to the form page


        user_name = User.objects.create_user(username=username, password=password)


        # Create a new ClientDetails object
        client = ClientDetails.objects.create(
            user=user_name,
            created_by=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            dob=request.POST.get('date_of_birth') or None,
            contact_no=request.POST.get('contact_no'),
            email_id=request.POST.get('email_id'),
            location=request.POST.get('location'),
            height=request.POST.get('height') or None,
            weight=request.POST.get('weight') or None,
            gender=request.POST.get('gender'),
            client_type=request.POST.get('client_type') or '',
            medical_condition=request.POST.get('medical_condition'),
            notes=request.POST.get('notes'),
            diet_preference=request.POST.get('diet_type'),
            medications=request.POST.get('medications'),
            chief_complaints=request.POST.get('chief_complaints'),
        )
        return redirect('client_list')  # Redirect to a success page or dashboard

    return render(request, 'clients/client_form.html')

@role_required('DIETICIAN')
def client_list(request):
    data=ClientDetails.objects.filter(created_by=request.user).order_by('-date_of_creation')
    print("-----",data)
    return render(request,'clients/client_list.html',context={'users':data})

@role_required('DIETICIAN')
def client_detail_view(request, client_id):
    # Retrieve the user object or return 404 if not found
    client = get_object_or_404(ClientDetails, id=client_id)
    context = {
        'user': client,
    }
    return render(request, 'clients/client_detail.html', context)



def update_client(request, client_id):
    client = get_object_or_404(ClientDetails, id=client_id)

    if request.method == 'POST':
        client.first_name = request.POST.get('first_name', '')
        client.last_name = request.POST.get('last_name', '')
        client.dob = request.POST.get('date_of_birth') or None
        client.contact_no = request.POST.get('contact_no', '')
        client.email_id = request.POST.get('email_id', '')
        client.location = request.POST.get('location', '')
        client.height = request.POST.get('height') or None
        client.weight = request.POST.get('weight') or None
        client.gender = request.POST.get('gender', '')
        client.client_type = request.POST.get('client_type') or ''
        client.medical_condition = request.POST.get('medical_condition', '')
        client.notes = request.POST.get('notes', '')
        client.medications = request.POST.get('medications', '')
        client.chief_complaints = request.POST.get('chief_complaints', '')

        client.save()
        return redirect('client_detail', client_id=client.id)  # Replace with your success view name

    return render(request, 'clients/client_edit.html', {'client': client})