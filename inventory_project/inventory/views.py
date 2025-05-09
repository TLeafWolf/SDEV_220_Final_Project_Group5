from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Supply, AuditLog  
from .forms import SupplyForm, UserCreationForm, UserDeletionForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
import csv
from django.http import HttpResponse, JsonResponse
from .forms import UploadFileForm, GroupForm, UserUpdateForm
from django.views.decorators.csrf import csrf_exempt
import json




def index(request):
    location_query = request.GET.get('location', '')
    name_query = request.GET.get('name', '')
    low_stock = request.GET.get('low_stock', False)
  
    sort_by = request.GET.get('sort', 'location')  
    order = request.GET.get('order', 'asc') 

    if order == 'desc':
        sort_by = '-' + sort_by 

    supplies = Supply.objects.all()

    if low_stock:
        supplies = supplies.filter(quantity__lt=6)

    if location_query:
        supplies = supplies.filter(location__icontains=location_query)

    if name_query:
        supplies = supplies.filter(name__icontains=name_query)

    supplies = supplies.order_by(sort_by)

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
    if 'added_supplies' in request.session:
        del request.session['added_supplies']
 
    context = { 
        'supplies': supplies,
        'low_stock_items': low_stock_items,
        'location_query': location_query,
        'name_query': name_query,
        'low_stock_items_exist': low_stock_items_exist,
        'sort_by': sort_by,
        'order': order,
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
    writer.writerow(['Name', 'Price', 'Quantity', 'Location'])
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
            if 'added_supplies' not in request.session:
                request.session['added_supplies'] = []

            request.session['added_supplies'].append(supply.name) 
            request.session.modified = True  

            AuditLog.objects.create(
                user=request.user, 
                action='CREATE', 
                supply=supply,
                changes=f'{supply.name}, ${supply.price:,.2f}, {supply.quantity}, {supply.location}' 
            )
            messages.success(request, 'Supply added successfully!')
            return render(request, 'inventory/add_supply.html', {'form': form})
        else:
            return render(request, 'inventory/add_supply.html', {'form': form}) 
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
            changes=f'{supply.name}, ${supply.price:,.2f}, {supply.quantity}, {supply.location}'
        )
        
        AuditLog.objects.filter(supply=supply).update(supply=None)
        
        supply.delete() 
        
        messages.success(request, 'Supply deleted successfully!')
        return redirect('index')
    
    messages.error(request, 'Invalid request method for deletion.')
    return redirect('index')

@login_required
def edit_supply(request, supply_name):
    supply = get_object_or_404(Supply, name=supply_name)
    
    if request.method == 'POST':
        old_data = f'{supply.name}, ${supply.price:,.2f}, {supply.quantity}, {supply.location}'
        
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            supply = form.save()
            new_data = f'{supply.name}, ${supply.price:,.2f}, {supply.quantity}, {supply.location}'

            AuditLog.objects.create(
                user=request.user, 
                action='UPDATE',  
                supply=supply, 
                changes=f'From {old_data} to {new_data}' 
            )
            messages.success(request, 'Supply updated successfully!')

    else:
        form = SupplyForm(instance=supply)

    return render(request, 'inventory/edit_supply.html', {'form': form})

@login_required
@csrf_exempt
def update_supply(request, supply_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        price = data.get('price')
        quantity = data.get('quantity')
        location = data.get('location')

        supply = get_object_or_404(Supply, name=supply_name)

        changes = []
        
   
        old_price = supply.price
        old_price_formatted = f"${old_price:,.2f}"
        
        if price is not None:
            new_price = float(price)
            new_price_formatted = f"${new_price:,.2f}"
            
            if new_price != old_price:
                changes.append(f"{supply.name}: Price changed from {old_price_formatted} to {new_price_formatted}")
                supply.price = new_price

        if quantity is not None and quantity != str(supply.quantity):
            changes.append(f"{supply.name}: Quantity changed from {supply.quantity} to {quantity}")
            supply.quantity = quantity 

        if location is not None and location != supply.location:
            changes.append(f"{supply.name}: Location changed from '{supply.location}' to '{location}'")
            supply.location = location

  
        if changes:
            supply.save()
            AuditLog.objects.create(
                action='UPDATE',
                user=request.user,  
                supply=supply,
                changes='; '.join(changes)
            )

        return JsonResponse({'status': 'success', 'message': 'Supply updated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('index')

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'inventory/add_user.html', {'form': form})

def delete_user(request):
    if request.method == 'POST':
        form = UserDeletionForm(request.POST)
        if form.is_valid():
            user_to_delete = form.cleaned_data['user']
            user_to_delete.delete()
            messages.success(request, f'User "{user_to_delete.username}" deleted successfully!')
            return redirect('delete_user')
    else:
        form = UserDeletionForm()
    return render(request, 'inventory/delete_user.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
def manage_groups(request):
    groups = Group.objects.all()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_groups')
    else:
        form = GroupForm()

    return render(request, 'inventory/manage_groups.html', {'groups': groups, 'form': form})

@user_passes_test(lambda u: u.is_superuser)  
def select_user(request):
    users = User.objects.all()
    return render(request, 'inventory/select_user.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def update_user(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user instance without committing to the database yet
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])  # Set the new password if provided
            user.save()  # Now save the user instance to the database

            user.groups.clear()  # Clear existing groups
            user.groups.add(form.cleaned_data['group'])  # Add the new group

            messages.success(request, 'User updated successfully.')
            return redirect('select_user')  # Redirect to the user selection page without re-logging in
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserUpdateForm(instance=user)

    current_groups = user.groups.all()

    return render(request, 'inventory/update_user.html', {
        'form': form,
        'user': user,
        'current_groups': current_groups,
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_settings(request):
    return render(request, 'inventory/admin_settings.html')
