
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import TODO
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo_a/home.html')


def signupUser(request):
    if request.method == 'GET':
        return render(request,'todo_a/signupUser.html',{ 'form': UserCreationForm()})
    else:
        if  request.POST['password1'] ==  request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request,'todo_a/signupUser.html',{ 'form': UserCreationForm(),'error':'The username already taken, please  try again'})

        else:
            return render(request,'todo_a/signupUser.html',{ 'form': UserCreationForm(),'error':'The Password didnt match'})

def loginUser(request):
        if request.method == 'GET':
            return render(request,'todo_a/loginUser.html',{ 'form': AuthenticationForm()})
        else:
            user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
            if user is None:
                return render(request,'todo_a/loginUser.html',{ 'form': AuthenticationForm(),'error':'username or password is wrong'})
            else:
                login(request,user)
                return redirect('currenttodo')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
        if request.method == 'GET':
            return render(request,'todo_a/createtodo.html',{ 'form':TodoForm()})
        else:
            try:
                form = TodoForm(request.POST)
                newtodo = form.save(commit=False)
                newtodo.user = request.user
                newtodo.save()
                return redirect('currenttodo')
            except ValueError:
                return render(request,'todo_a/createtodo.html',{ 'form':TodoForm(),'error':'Bad Data'})

@login_required
def currenttodo(request):
    todos = TODO.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo_a/currenttodo.html',{'todos':todos})

@login_required
def completedtodo(request):
    todos = TODO.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo_a/completedtodo.html',{'todos':todos})






@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(TODO,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,'todo_a/todoview.html',{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todo_a/todoview.html',{'todo':todo,'form':form,'error':'Bad Data'})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(TODO,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(TODO,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')
