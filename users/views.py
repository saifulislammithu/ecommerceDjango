from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponseRedirect

from django.contrib.auth import login,logout,authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    user=request.user
    context={'user':user}
    return render(request,'registration/index.html',context)
def login_view(request):
    
    return render(request,'users/login.html')

def register(request):
    if request.method!='POST':
        #Display blank registration form.
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #Log the user in then redirect to the home page.
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return redirect('home')
    context={'form':form}
    return render(request,'registration/register.html',context)
def logout_view(request):
    logout(request)
    return redirect('home')
    