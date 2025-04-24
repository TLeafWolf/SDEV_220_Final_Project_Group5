# inventory/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supply
from .forms import SupplyForm
from django.contrib import messages

def index(request):
    supplies = Supply.objects.all()  # Query all Supply objects
    return render(request, 'index.html', {'supplies': supplies})  # Pass the supplies to the template

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin:index')  # Redirect to the admin index page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new supply to the database
            messages.success(request, 'Supply added successfully!')
            return redirect('index')  # Redirect to the index page after adding
    else:
        form = SupplyForm()  # Create a new form instance

    return render(request, 'add_supply.html', {'form': form})  # Pass the form to the template

def delete_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)  # Fetch the supply by name
    supply.delete()  # Delete the supply from the database
    messages.success(request, 'Supply deleted successfully!')
    return redirect('index')  # Redirect to the index page after deletion