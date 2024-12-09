from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.contrib.auth import logout
@login_required
def home(request):
    # Crear un diccionario de contexto que contiene el rol del usuario autenticado
    context = {
        'role': request.user.role if request.user.is_authenticated else None  # Si el usuario está autenticado, añade su rol al contexto
    }
    # Renderiza la plantilla 'appointments/home.html' con el contexto proporcionado
    return render(request, 'appointments/home.html', context)

@login_required
def notifications(request):
    # Lógica para obtener las notificaciones del usuario
    notifications = [] # Aquí podrías añadir lógica para obtener las notificaciones
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'notifications': notifications
    }

    return render(request, 'appointments/notifications.html', context)


@login_required
def create_appointment(request):
    if request.user.role != 'tenant':
        return redirect('home')

    if request.method == 'POST':
        repair_type = request.POST['repair_type']
        date = request.POST['date']
        time = request.POST['time']
        description = request.POST['description']
        Appointment.objects.create(
            tenant=request.user,
            repair_type=repair_type,
            date=date,
            time=time,
            description=description
        )
        context = {
            'role': request.user.role if request.user.is_authenticated else None,
        }

    return render(request, 'appointments/create_appointment.html', context)

@login_required
def manage_appointments(request):
    if request.user.role != 'admin':
        return redirect('home')

    appointments = Appointment.objects.all()
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'appointments': appointments
    }
    return render(request, 'appointments/manage_appointments.html',context)

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(tenant=request.user)
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'appointments': appointments
    }
    return render(request, 'appointments/appointment_list.html', context)


from django.views.decorators.csrf import csrf_exempt  # Agrega esto para desactivar CSRF temporalmente

@csrf_exempt
def logout_view(request):
    if request.method in ['GET', 'POST']:  # Acepta GET y POST
        logout(request)
        return render(request, 'users/logout.html')
    return redirect('home')
