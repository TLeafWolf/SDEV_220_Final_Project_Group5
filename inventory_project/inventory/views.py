# inventory/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models 
from .models import Supply
from .forms import SupplyForm
from django.contrib import messages

def index(request):
    location_query = request.GET.get('location', '')
    name_query = request.GET.get('name', '')

    # Get all supplies
    supplies = Supply.objects.all()

    # Filter supplies based on location and name queries
    if location_query:
        supplies = supplies.filter(location__icontains=location_query)
    if name_query:
        supplies = supplies.filter(name__icontains=name_query)

    # Handle return functionality
    if request.method == 'POST':
        supply_name = request.POST.get('supply_name')
        quantity_returned = int(request.POST.get('quantity', 0))
        supply = get_object_or_404(Supply, name=supply_name)

        if quantity_returned > 0:
            supply.quantity += quantity_returned
            supply.save()
            messages.success(request, f'Supply {supply_name} returned successfully! New quantity: {supply.quantity}')
        else:
            messages.error(request, 'Invalid quantity returned. Please enter a positive number.')

    # Check for low stock supplies based on the current stock levels
    low_stock_items = Supply.objects.filter(quantity__lte=models.F('reorder_point'))

    context = { 
        'supplies': supplies,
        'low_stock_items': low_stock_items,
        'location_query': location_query,
        'name_query': name_query,
    }
    return render(request, 'inventory/index.html', context)

def low_stock_supplies(request):
    low_stock_items = Supply.objects.filter(quantity__lte=models.F('reorder_point'))
    return render(request, 'inventory/low_stock.html', {'low_stock_items': low_stock_items})
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'inventory/login.html')

def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supply added successfully!')
            return redirect('index')
    else:
        form = SupplyForm()
    return render(request, 'inventory/add_supply.html', {'form': form})

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
    return render(request, 'inventory/edit_supply.html', {'form': form})

