from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('appointment-list/', views.appointment_list, name='appointment_list'),
    path('home/', views.home, name='home'),
    path('create-message/', views.create_message, name='create_message'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('appointments/accept/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('appointments/reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),

    path('notifications/', views.notifications_view, name='notifications'),  # Vista de notificaciones activas
    path('notifications/close/<int:notification_id>/', views.close_notification, name='close_notification'),
    # Cerrar notificación
    path('history/', views.history_view, name='history'),
    path('answer_message/<int:notification_id>/', views.answer, name='answer'),
    path('information/', views.information_view, name='information'),


     path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),


]
