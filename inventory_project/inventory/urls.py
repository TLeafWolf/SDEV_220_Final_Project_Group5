# inventory/urls.py

from django.urls import path
from .views import custom_login, index

urlpatterns = [
    path('', index, name='index'),
    path('login/', custom_login, name='login'),
]
