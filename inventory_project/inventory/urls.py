from django.urls import path
from . import views
from django.contrib import admin

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
    path('admin/', admin.site.urls),
    path('custom-admin/', views.admin_settings, name='admin_settings'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),  
    path('manage_groups/', views.manage_groups, name='manage_groups'),  
    path('select_user/', views.select_user, name='select_user'), 
    path('update_user/', views.update_user, name='update_user'),  

    
]
