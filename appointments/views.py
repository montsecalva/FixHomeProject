mport render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, message, User
from django.utils.timezone import now
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt  # Agrega esto para desactivar CSRF temporalmente


@login_required
def home(request):
    context = {
        'role': request.user.role if request.user.is_authenticated else None
    }
    return render(request, 'appointments/home.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, message, User

@login_required
def create_appointment(request):
    # Solo los usuarios con rol de admin pueden acceder
    if request.user.role != 'admin':
        return redirect('home')

    if request.method == 'POST':
        repair_type = request.POST['repair_type']
        date = request.POST['date']
        time = request.POST['time']
        description = request.POST['description']
        tenant_username = request.POST.get('tenant_username')

        # Validar que el usuario tenant exista
        tenant = get_object_or_404(User, username=tenant_username, role='tenant')

        # Crear la cita como pendiente
        Appointment.objects.create(
            tenant=tenant,
            admin=request.user,
            repair_type=repair_type,
            date=date,
            time=time,
            description=description,
            status='pending'
        )

        # Crear notificación para el tenant
        message.objects.create(
            content=f'Nueva cita pendiente: {repair_type} el {date} a las {time}.',
            creator_id=request.user.id,
            recipient_id=tenant.id
        )

        return redirect('notifications')  # Redirigir después de enviar el formulario

    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'tenants': User.objects.filter(role='tenant'),  # Para listar tenants en la plantilla
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
    return render(request, 'appointments/manage_appointments.html', context)


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'appointments': appointments
    }
    return render(request, 'appointments/appointment_list.html', context)


@csrf_exempt
def logout_view(request):
    if request.method in ['GET', 'POST']:  # Acepta GET y POST
        logout(request)
        return render(request, 'users/logout.html')
    return redirect('home')


@login_required
def create_message(request):
    # Verifica si el usuario tiene el rol 'tenant'
    if request.user.role != 'tenant':
        return redirect('home')  # Si no es 'tenant', redirige a la página de inicio

    # Si el método de la solicitud es POST, guarda el mensaje
    if request.method == 'POST':
        content = request.POST.get('content', '')  # Obtiene el contenido del mensaje
        image = request.FILES.get('image', None)  # Obtiene la imagen del mensaje si la hay
        creator_id = request.user.id  # Obtener el ID del usuario autenticado
        # Obtener el usuario por nombre de usuario
        user = get_object_or_404(User, username='user')
        recipient_id = user.id  # Obtener el ID del usuario
        message.objects.create(content=content, image=image, creator_id=creator_id, recipient_id=recipient_id)  # Crea el mensaje en la base de datos
        return redirect('notifications')  # Redirige al usuario a la página de notificaciones

    # Si no es POST, solo muestra el formulario
    context = {
        'role': request.user.role if request.user.is_authenticated else None,  # Pasa el rol del usuario al contexto
    }
    return render(request, 'appointments/create_message.html', context)  # Renderiza la plantilla de crear mensaje


@login_required
def notifications_view(request):
    if request.user.role == 'admin':
        # Notificaciones para el administrador
        notifications = message.objects.filter(recipient=request.user, is_active=True).order_by('-date')
        pending_appointments = None  # Admin no tiene citas pendientes propias
    elif request.user.role == 'tenant':
        # Notificaciones y citas pendientes para el tenant
        notifications = message.objects.filter(recipient=request.user, is_active=True).order_by('-date')
        pending_appointments = Appointment.objects.filter(tenant=request.user, status='pending')
    else:
        return redirect('home')

    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'notifications': notifications,
        'pending_appointments': pending_appointments,
    }
    return render(request, 'appointments/notifications.html', context)



@login_required
def answer(request, notification_id):
    if request.user.role != 'admin':
        return redirect('home')  # Redirige si no es 'admin'

    notification = get_object_or_404(message, id=notification_id)

    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image', None)
        creator_id = request.user.id  # ID del usuario admin
        recipient_id = notification.creator.id  # El destinatario será el tenant que creó el mensaje

        # Crea la respuesta
        message.objects.create(
            content=content,
            image=image,
            creator_id=creator_id,
            recipient_id=recipient_id
        )

        # Elimina el mensaje original de las notificaciones del admin
        notification.delete()

        return redirect('notifications')  # Redirige a las notificaciones después de enviar la respuesta

    # Si no es POST, solo muestra el formulario de respuesta
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'notification': notification,
    }

    return render(request, 'appointments/answer.html', context)

@login_required
def accept_appointment(request, appointment_id):
    if request.user.role != 'tenant':
        return redirect('home')

    # Cambiar el estado de la cita a 'accepted'
    appointment = get_object_or_404(Appointment, id=appointment_id, tenant=request.user)
    appointment.status = 'accepted'
    appointment.save()

    # Crear notificación para el administrador
    message.objects.create(
        content=f'El usuario {request.user.username} ha aceptado la cita: {appointment.repair_type}.',
        creator_id=request.user.id,
        recipient_id=appointment.admin.id
    )

    return redirect('notifications')

@login_required
def reject_appointment(request, appointment_id):
    if request.user.role != 'tenant':
        return redirect('home')

    # Eliminar la cita y notificar al administrador
    appointment = get_object_or_404(Appointment, id=appointment_id, tenant=request.user)
    message.objects.create(
        content=f'El usuario {request.user.username} ha rechazado la cita: {appointment.repair_type}.',
        creator_id=request.user.id,
        recipient_id=appointment.admin.id
    )
    appointment.delete()

    return redirect('notifications')

