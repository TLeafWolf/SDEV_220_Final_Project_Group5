from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Supply, AuditLog  # Make sure to import AuditLog
from .forms import SupplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse, JsonResponse
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
import json




def index(request):
    location_query = request.GET.get('location', '')
    name_query = request.GET.get('name', '')
    low_stock = request.GET.get('low_stock', False)


    supplies = Supply.objects.all()

    if low_stock:
        supplies = supplies.filter(quantity__lt=6)

    if location_query:
        supplies = supplies.filter(location__icontains=location_query)
    if name_query:
        supplies = supplies.filter(name__icontains=name_query)

 
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

    
    low_stock_items = Supply.objects.filter(quantity__lte=models.F('reorder_point'))
    low_stock_items_exist = low_stock_items.exists() 

    context = { 
        'supplies': supplies,
        'low_stock_items': low_stock_items,
        'location_query': location_query,
        'name_query': name_query,
        'low_stock_items_exist': low_stock_items_exist,
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

def export_supplies(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="supplies.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Price', 'Quantity', 'Location'])  # Header row
    for supply in Supply.objects.all():
        writer.writerow([supply.name, supply.price, supply.quantity, supply.location])
    return response

def import_supplies(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            reader = csv.reader(file.read().decode('utf-8').splitlines())
            next(reader)  
            for row in reader:
                Supply.objects.create(name=row[0], price=row[1], quantity=row[2], location=row[3])
            return redirect('index') 
    else:
        form = UploadFileForm()
    return render(request, 'inventory/import_supplies.html', {'form': form})

def audit_log(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'inventory/audit_log.html', {'logs': logs})

@login_required
def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save()

            # Create an audit log entry
            AuditLog.objects.create(
                user=request.user,  # User who made the change
                action='CREATE',  # Action type
                supply=supply,  # The supply that was created
                changes=f'Created supply: {supply.name}, {supply.price}, {supply.quantity}, {supply.location}'  # Description of the changes
            )
            messages.success(request, 'Supply added successfully!')
            return redirect('index')
    else:
        form = SupplyForm()
    return render(request, 'inventory/add_supply.html', {'form': form})

@login_required
def delete_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)

    if request.method == 'POST':
        AuditLog.objects.create(
            user=request.user,
            action='DELETE',
            supply=supply,
            changes=f'Deleted supply: {supply.name}, {supply.price}, {supply.quantity}, {supply.location}'
        )
        supply.save() #change to delete to delete entries from audit log and save for it to add that it deleted the item to the audit log
        messages.success(request, 'Supply deleted successfully!')
        return redirect('index')
    
    messages.error(request, 'Invalid request method for deletion.')
    return redirect('index')

@login_required
def edit_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
    
            old_data = f'{supply.name}, {supply.price}, {supply.quantity}, {supply.location}'
            supply = form.save()
            new_data = f'{supply.name}, {supply.price}, {supply.quantity}, {supply.location}'

            # Create an audit log entry for the update
            AuditLog.objects.create(
                user=request.user,  # User who made the change
                action='UPDATE',  # Action type
                supply=supply,  # The supply that was updated
                changes=f'Updated supply: From {old_data} to {new_data}'  # Description of what was changed
            )
            messages.success(request, 'Supply updated successfully!')
            return redirect('index')
    else:
        form = SupplyForm(instance=supply)
    return render(request, 'inventory/edit_supply.html', {'form': form})


@csrf_exempt 
def update_supply(request, supply_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        price = data.get('price')
        quantity = data.get('quantity')
        location = data.get('location')

        
        supply = get_object_or_404(Supply, name=supply_name)

        changes = []
        if price is not None and price != str(supply.price):
            changes.append(f"Price changed from ${supply.price} to ${price}")
            supply.price = price
        if quantity is not None and quantity != str(supply.quantity):
            changes.append(f"Quantity changed from {supply.quantity} to {quantity}")
            supply.quantity = quantity 
        if location is not None and location != supply.location:
            changes.append(f"Location changed from '{supply.location}' to '{location}'")
            supply.location = location

        
        supply.save()

     
        if changes:
            AuditLog.objects.create(
                action='Update',
                user=request.user,  
                supply=supply,
                changes='; '.join(changes)
            )

        return JsonResponse({'status': 'success', 'message': 'Supply updated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('index')
