from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, f"Welcome back, {user.username}!")
            return redirect('homepage')  # replace 'home' with your actual home page name
        else:
            # messages.error(request, "Invalid username or password")
            print("Invalid Username or Password !")
    
    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # or wherever you want to redirect post-logout