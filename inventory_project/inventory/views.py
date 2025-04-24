# inventory/views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

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

