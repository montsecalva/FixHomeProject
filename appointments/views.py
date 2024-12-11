from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, message
from django.utils.timezone import now
from .models import User
from django.contrib.auth import logout
@login_required
def home(request):
    context = {
        'role': request.user.role if request.user.is_authenticated else None
    }
    return render(request, 'appointments/home.html', context)



@login_required
def create_appointment(request):
    if request.user.role != 'admin':
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
    appointments = Appointment.objects.all()
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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, message
from django.utils.timezone import now

@login_required
def create_message(request):
    # Verifica si el usuario tiene el rol 'tenant'
    if request.user.role != 'tenant':
        return redirect('home')  # Si no es 'tenant', redirige a la página de inicio

    # Si el método de la solicitud es POST, guarda el mensaje
    if request.method == 'POST':
        content = request.POST.get('content', '')  # Obtiene el contenido del mensaje
        image = request.FILES.get('image', None)# Obtiene la imagen del mensaje si la hay
        creator_id = request.user.id  # Obtener el ID del usuario autenticado
        # Obtener el usuario por nombre de usuario
        user = get_object_or_404(User, username='user')
        recipient_id = user.id  # Obtener el ID del usuario
        message.objects.create(content=content, image=image,creator_id=creator_id,recipient_id=recipient_id)  # Crea el mensaje en la base de datos
        return redirect('notifications')  # Redirige al usuario a la página de notificaciones

    # Si no es POST, solo muestra el formulario
    context = {
        'role': request.user.role if request.user.is_authenticated else None,  # Pasa el rol del usuario al contexto
    }
    return render(request, 'appointments/create_message.html', context)  # Renderiza la plantilla de crear mensaje
@login_required
def notifications(request):
    if request.user.role != 'admin':
        return redirect('home')  # Redirige si el usuario no es 'admin'

    all_notifications = message.objects.all().order_by('-date')  # Ordena por fecha descendente
    context = {
        'role': request.user.role if request.user.is_authenticated else None,
        'notifications': all_notifications,
    }
    return render(request, 'appointments/notifications.html', context)