from django.contrib import admin
from django.urls import path , include
#from mi_app.views.administrador import *
from django.conf import settings
from django.conf.urls.static import static
from mi_app import views

urlpatterns = [
    path('', include(('mi_app.urls', 'mi_app'), namespace='mi_app')),
    path('login/', include(('login.urls', 'login'), namespace='login')),
    path('admin/', admin.site.urls),
    path('registro/', include('registro.urls', namespace='registro')),    
    path('exportar-pdf/<str:modelo>/', views.exportar_pdf_universal, name='exportar_pdf_universal'),
    path('perfil/', views.perfil_view, name='perfil'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)