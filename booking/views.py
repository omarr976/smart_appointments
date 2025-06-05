from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Appointment
from .forms import AppointmentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def about_us(request):
    return render(request, 'booking/about_us.html')

@login_required(login_url='login')
def my_account(request):
    return render(request, 'booking/my_account.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib import messages

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.delete()
    messages.success(request, 'Your appointment has been cancelled.')
    return redirect('my_appointments')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')  # ✅ Fix: redirect after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'booking/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Please fill in all fields.')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'booking/register.html')

def home(request):
    services = Service.objects.all()
    return render(request, 'booking/home.html', {'services': services})

@login_required
def book_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = service
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully.')
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'booking/book_appointment.html', {'service': service, 'form': form})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})
