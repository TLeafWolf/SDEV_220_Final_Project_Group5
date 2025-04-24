# inventory/urls.py

from django.urls import path
from .views import custom_login, index, add_supply

urlpatterns = [
    path('', index, name='index'),
    path('login/', custom_login, name='login'),
    path('add_supply/', add_supply, name='add_supply'),
]
