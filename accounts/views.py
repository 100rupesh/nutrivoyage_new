from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard') 
    if request.method == "POST":
        print("Inside post")
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print("USSSR",user.role)
            # messages.success(request, f"Welcome back, {user.username}!")
            if user.role=='NORMAL':
                print("NORMALLLL")
                return redirect('client')
            return redirect('homepage')  # replace 'home' with your actual home page name
              # replace 'home' with your actual home page name
        else:
            # messages.error(request, "Invalid username or password")
            messages.error(request, 'Invalid username or password.')
            print("Invalid Username or Password !")
    
    return render(request, 'accounts/login.html')



def logout_view(request):
    print("LLL")
    logout(request)
    return redirect('login')  # or wherever you want to redirect post-logout