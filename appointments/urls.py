from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('manage-appointments/', views.manage_appointments, name='manage_appointments'),
    path('appointment-list/', views.appointment_list, name='appointment_list'),
    path('home/', views.home, name='home'),
    path('notifications/', views.notifications, name='notifications'),
     path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
