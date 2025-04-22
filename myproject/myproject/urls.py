"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory_app.views import inventory_view, add_item, update_item, delete_item

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inventory_view, name='inventory_view'),  # Main inventory view
    path('add/', add_item, name='add_item'),          # URL for adding a new item
    path('update/<int:item_id>/', update_item, name='update_item'),  # URL for updating an item
    path('delete/<int:item_id>/', delete_item, name='delete_item'),  # URL for deleting an item
]
