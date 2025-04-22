from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem
from .forms import InventoryItemForm

def inventory_view(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory_app/inventory_view.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_view')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory_app/add_item.html', {'form': form})

def update_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()  # This updates the item in the SQLite database
            return redirect('inventory_view')  # Redirect to the inventory list after updating
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory_app/update_item.html', {'form': form, 'item': item})

def delete_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    return redirect('inventory_view')