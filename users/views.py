
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .models import NewUser
from .forms import CreateUserForm
#from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    user=request.user
    context={'user':user}
    return render(request,'registration/index.html',context)
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context={}
    return render(request,'registration/login.html',context)

def register(request):
    if request.method!='POST':
        #Display blank registration form.
        form=CreateUserForm()
        print('Blank Form Request:',form)
    else:
        form=CreateUserForm(data=request.POST)
        if form.is_valid():
        
            password=form.clean_password2()
            new_user=form.save()
            username=new_user.username

            #Log the user in then redirect to the home page.
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
    context={'form':form}
    return render(request,'registration/register.html',context)
def logout_view(request):
    logout(request)
    return redirect('home')
    