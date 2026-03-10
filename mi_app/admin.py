from django.contrib import admin

# 1. Importas los modelos de tu base de datos
from .models import Administrador, GestionCliente, Pedido

# 2. Los registras uno por uno para que Django los dibuje en el panel
admin.site.register(Administrador)
admin.site.register(GestionCliente)
admin.site.register(Pedido)





# (Puedes agregar aquí cualquier otra tabla que tengas en models.py y quieras ver)