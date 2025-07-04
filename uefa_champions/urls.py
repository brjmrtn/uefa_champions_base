# uefa_champions/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import login_usuario, logout_usuario, registro_usuario


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Autenticación
    path('usuarios/login/',    login_usuario,  name='login'),
    path('usuarios/logout/',   logout_usuario, name='logout'),
    path('usuarios/registro/', registro_usuario, name='registro'),

    # Resto de la aplicación
    path('', include('core.urls')),  # aquí está tu view 'home' con name='home'
]
