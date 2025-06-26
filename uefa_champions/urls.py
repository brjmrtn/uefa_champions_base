from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('users.urls')),  # rutas de login/registro
    path('', include('core.urls')),
]
