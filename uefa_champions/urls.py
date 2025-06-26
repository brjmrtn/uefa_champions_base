# uefa_champions/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import login_usuario, logout_usuario, registro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),

    # Registro / Login / Logout
    path('usuarios/registro/', registro_usuario, name='registro'),
    path('usuarios/login/',    login_usuario,    name='login'),
    path('usuarios/logout/',   logout_usuario,   name='logout'),

    # Resto de URLs de la app users (si hubiera más)
    path('usuarios/', include('users.urls')),

    # Tu app core
    path('', include('core.urls')),
]
