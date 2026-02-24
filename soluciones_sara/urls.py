from django.contrib import admin
from django.urls import path , include
#from mi_app.views.administrador import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('mi_app.urls', 'mi_app'), namespace='mi_app')),
    path('login/', include(('login.urls', 'login'), namespace='login')),
    path('admin/', admin.site.urls),
    path('registro/', include('registro.urls', namespace='registro')),     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)