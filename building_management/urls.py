
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
urlpatterns = [
path('admin/', admin.site.urls),
path('users/', include('users.urls')),
path('appointments/', include('appointments.urls')),
path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('', RedirectView.as_view(url='/users/login/', permanent=False)),

]