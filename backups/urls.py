from django.urls import path
from . import views

app_name = 'backups'

urlpatterns = [
    path('gestion/', views.realizar_copia_seguridad, name='generar_backup'),
    path('restaurar/', views.restaurar_backup, name='restaurar_backup'),
    path('descargar/<str:nombre_archivo>/', views.descargar_backup, name='descargar_backup'),
]