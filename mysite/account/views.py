from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import Register, AdminRegister
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method=='POST':
        form=Register(request.POST)
        if form.is_valid():
            user=form.save()
            
            # Send welcome email
            subject = 'Welcome to MySite'
            message = f'Hi {user.username}, thank you for registering at MySite.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                print(f"Error sending email: {e}")

            auth_login(request,user)
            return redirect('home')
    else:
        form=Register()
    return render(request,"accounts/register.html",{"form":form})    

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegister(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AdminRegister()
    return render(request, "accounts/register.html", {"form": form, "title": "Admin Registration"})
     
def login(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next', 'home'))
    else:
        form=AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                return render(request, 'accounts/admin_login.html', {
                    'form': form, 
                    'error': 'Access Denied: You are not an Admin.'
                })
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/admin_login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')