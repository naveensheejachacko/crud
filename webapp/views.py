
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from .models import *

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_superuser is False:
                    response=redirect('home')
                    login(request,user)
                    return response
                else:
                    response=redirect('adminn')
                    return response
            else:
                messages.info(request,'username Or Password is Incorrect!')
                return redirect('login')
        return render(request,'webapp/login.html')
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                #user=form.cleaned_data.get('username')
                #messages.success(request,'Account was created for' +user)
                response=redirect('login')
                return response
    context={'form':form}
    return render(request,'webapp/signup.html',context)
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser is False:
            return render(request,'webapp/home.html')
        else:
            return redirect('adminn')
def user_logout(request):
    logout(request)
    response=redirect('login')
    return response
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('admin_home')
                else:
                    return redirect('adminn')
            else:
                messages.info(request,'username Or Password is Incorrect!') 
                return redirect('adminn')
                
    return render(request,'webapp/admin.html')
@login_required(login_url='adminn')
def admin_home(request):
    if request.user.is_superuser:
        context={'user_details':User.objects.all()}#show user details
        return render(request,'webapp/admin_home.html',context)#show list
    else:
        return render(request,'webapp/admin.html')
def admin_logout(request):
    logout(request)
    return redirect('adminn')



    #CRUD

def users(request):
    if request.user.is_superuser:
        context={'user_details':User.objects.all()}
        return render(request,'webapp/admin_home.html',context)
    else:
        return redirect('adminn')
def user_insert(request,id=0):
    if request.user.is_superuser:
        if request.method=="GET":
            if(id==0):
                form=CreateUserForm()
            else:
                u=User.objects.get(pk=id)
                form=CreateUserForm(instance=u)
            return render(request,'webapp/user_insert.html',{'form':form})
        else:
            if id==0:
                form=CreateUserForm(request.POST)
            else:
                u=User.objects.get(pk=id)
                form=CreateUserForm(request.POST,instance=u)
            response=redirect('users')
            if form.is_valid():
                form.save()
            return response
    else:
        return redirect('adminn')
def user_delete(request,id):
    if request.user.is_superuser:
        u=User.objects.get(pk=id)
        u.delete()
        return redirect('users')
    else:
        return redirect('adminn')
def search(request):
    if request.user.is_superuser:
        query=request.GET['query']
        user_details=User.objects.filter(username__icontains=query)
        context={'user_details':user_details}
        return render(request,'webapp/search.html',context)
    else:
        return redirect('adminn')