from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate

def home(request):
    return render(request,'todo_a\home.html')

def signupUser(request):
    if request.method == 'GET':
        return render(request,'todo_a\signupUser.html',{ 'form': UserCreationForm()})
    else:
        if  request.POST['password1'] ==  request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request,'todo_a\signupUser.html',{ 'form': UserCreationForm(),'error':'The username already taken, please  try again'})

        else:
            return render(request,'todo_a\signupUser.html',{ 'form': UserCreationForm(),'error':'The Password didnt match'})

def loginUser(request):
        if request.method == 'GET':
            return render(request,'todo_a\loginUser.html',{ 'form': AuthenticationForm()})
        else:
            user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
            if user is None:
                return render(request,'todo_a\loginUser.html',{ 'form': AuthenticationForm(),'error':'username or password is wrong'})
            else:
                login(request,user)
                return redirect('currenttodo')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodo(request):
    return render(request,'todo_a\currenttodo.html')
