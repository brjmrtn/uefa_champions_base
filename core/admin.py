from django.contrib import admin
from .models import Fase, Partido, Prediccion, PerfilUsuario, PrediccionBonus

@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre', 'desbloqueada')
    list_editable = ('desbloqueada',)
    ordering = ('orden',)

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('fase', 'equipo_local', 'equipo_visitante', 'fecha', 'goles_local', 'goles_visitante')
    list_filter  = ('fase',)
    ordering     = ('fecha',)

@admin.register(Prediccion)
class PrediccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'partido', 'goles_local', 'goles_visitante', 'fecha_prediccion')
    list_filter  = ('usuario', 'partido__fase')

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'validado')
    list_editable = ('validado',)

@admin.register(PrediccionBonus)
class PrediccionBonusAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campeon', 'goleador', 'mvp')
    list_filter  = ('usuario',)
