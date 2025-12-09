from django.contrib import admin
from .models import Categoria, Plato, DetallePedido, Mesa, Pedido
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Plato)
admin.site.register(DetallePedido)
admin.site.register(Mesa)
admin.site.register(Pedido)