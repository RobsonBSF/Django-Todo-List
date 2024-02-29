from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = username, email = email, password = password)
        if user:
            login(request, user)
            return redirect('lists')
        else:
            return redirect('login')

def register_page(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username).first()
        if user:
            return redirect('register')
        else:
            user = User.objects.create_user(username = username, email = email, password = password)
            authenticate(username = username, email = email, password = password)
            login(request, user)
            return redirect('home')

def logout_link(request):
    logout(request)
    return redirect('login')
    
@login_required(login_url='login')
def lists(request):
    tasks = Task.objects.filter(user_id = request.user.id)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_id = request.user.id
            task.save()
            return redirect('lists')

    context = {'tasks':tasks, 'form':form}
    return render(request, 'lists.html', context)

@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('lists')

    context = {'form':form, 'task':task}

    return render(request, 'update.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('lists')

    context = {'item':item}
    return render(request, 'delete.html', context)