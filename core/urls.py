from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predicciones/', views.predicciones_disponibles, name='predicciones'),
    path('admin/validar-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('clasificacion/', views.clasificacion, name='clasificacion'),
    path('resultados/', views.resultados_en_vivo, name='resultados'),
    path('admin/panel/', views.panel_admin, name='panel_admin'),
    path('bonus/', views.prediccion_bonus, name='bonus'),
    path('admin/exportar-ranking/', views.exportar_ranking_csv, name='exportar_ranking'),
    path('admin/exportar-predicciones/', views.exportar_predicciones_csv, name='exportar_predicciones'),

]
