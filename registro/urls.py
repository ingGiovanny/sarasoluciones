from django.urls import path
from . import views

# AGREGA ESTA LÍNEA (Es lo que Django te está pidiendo)
app_name = 'registro' 

urlpatterns = [
    # Asegúrate de que el nombre aquí coincida con lo que usas en el HTML
    path('crear/', views.registroView.as_view(), name='registro'),
]