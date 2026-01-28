from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import Register

def register(request):
    if request.method=='POST':
        form=Register(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('home')
    else:
        form=Register()
    return render(request,"accounts/register.html",{"form":form})    
    
def login(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next', 'home'))
    else:
        form=AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')