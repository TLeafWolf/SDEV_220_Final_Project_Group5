# inventory/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Supply 

def index(request):
    supplies = Supply.objects.all()  # Query all Supply objects
    return render(request, 'index.html', {'supplies': supplies})  # Pass the supplies to the template

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin:index')  # Redirect to the admin index page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

