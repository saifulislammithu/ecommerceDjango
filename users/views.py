from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    context={'user':user}
    return render(request,'users/index.html',context)
def login(request):
    context={}
    return render(request,'users/login.html',context)

def register(request):
    context={}
    return render(request,'users/register.html',context)