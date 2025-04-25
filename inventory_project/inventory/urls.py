

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    path('low-stock/', views.low_stock_supplies, name='low_stock_supplies'),
    path('add-supply/', views.add_supply, name='add_supply'),
    path('delete-supply/<str:supply_name>/', views.delete_supply, name='delete_supply'),
    path('edit-supply/<str:supply_name>/', views.edit_supply, name='edit_supply'),
]
