from django.shortcuts import render, get_object_or_404, redirect
from .models import Plato,Categoria,DetallePedido,Mesa,Pedido
# Create your views here.

def menu_restuarante(request):
    cargar_productos = Plato.objects.filter(disponible=True)
    cargar_categorias = Categoria.objects.all()

    contexto = {
        "productos" : cargar_productos,
        "categorias" : cargar_categorias
    }

    return render(request, "core/menu.html", contexto)

def agregar_producto_a_mesa(request,plato_id: int,mesa_id: int):
    plato = get_object_or_404(Plato,id=plato_id)
    mesa = get_object_or_404(Mesa,id=mesa_id)

    pedido,creado = Pedido.objects.get_or_create(
        mesa = mesa,
        estado = "pendiente"
    )

    DetallePedido.objects.get_or_create(
        pedido = pedido,
        cantidad = 1,
        plato = plato,
    )
    return redirect("menu")