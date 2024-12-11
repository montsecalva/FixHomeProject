from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signin/', views.signin_view, name='signin'),  # Ruta para el registro
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

]