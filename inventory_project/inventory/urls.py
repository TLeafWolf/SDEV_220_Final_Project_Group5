from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.custom_login, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('low-stock/', views.low_stock_supplies, name='low_stock_supplies'), 
    path('audit-log/', views.audit_log, name='audit_log'),  
    path('add-supply/', views.add_supply, name='add_supply'),  
    path('delete-supply/<str:supply_name>/', views.delete_supply, name='delete_supply'),  
    path('edit-supply/<str:supply_name>/', views.edit_supply, name='edit_supply'),  
    path('export/', views.export_supplies, name='export_supplies'), 
    path('import/', views.import_supplies, name='import_supplies'),  
    path('update_supply/<str:supply_name>/', views.update_supply, name='update_supply'),
    
]
