# inventory/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supply
from .forms import SupplyForm
from django.contrib import messages

def index(request):
    supplies = Supply.objects.all()  
    return render(request, 'index.html', {'supplies': supplies})  

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin:index')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Supply added successfully!')
            return redirect('index')  
    else:
        form = SupplyForm() 

    return render(request, 'add_supply.html', {'form': form})  

def delete_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)  
    supply.delete()  
    messages.success(request, 'Supply deleted successfully!')
    return redirect('index')  

def edit_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)  
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply) 
        if form.is_valid():
            form.save() 
            messages.success(request, 'Supply updated successfully!')
            return redirect('index') 
    else:
        form = SupplyForm(instance=supply) 

    return render(request, 'edit_supply.html', {'form': form}) 
