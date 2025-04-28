

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page
    path('login/', views.custom_login, name='login'),  # Login page
    path('low-stock/', views.low_stock_supplies, name='low_stock_supplies'),  # Low stock supplies page
    path('audit-log/', views.audit_log, name='audit_log'),  # URL for audit logs
    path('add-supply/', views.add_supply, name='add_supply'),  # Add supply page
    path('delete-supply/<str:supply_name>/', views.delete_supply, name='delete_supply'),  # Delete supply
    path('edit-supply/<str:supply_name>/', views.edit_supply, name='edit_supply'),  # Edit supply
    path('export/', views.export_supplies, name='export_supplies'),  # Export supplies
    path('import/', views.import_supplies, name='import_supplies'),  # Import supplies
    
]
