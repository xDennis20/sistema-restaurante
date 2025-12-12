from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_safe, require_POST

from .models import Plato,Categoria,DetallePedido,Mesa,Pedido
# Create your views here.

def menu_restuarante(request,mesa_id: int):
    mesa = get_object_or_404(Mesa, id= mesa_id)
    cargar_productos = Plato.objects.filter(disponible=True)
    cargar_categorias = Categoria.objects.all()

    contexto = {
        "mesa" : mesa,
        "productos" : cargar_productos,
        "categorias" : cargar_categorias
    }

    return render(request, "core/menu.html", contexto)

def agregar_producto_a_mesa(request,mesa_id: int,plato_id: int):
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
    return redirect("menu",mesa_id=mesa_id)

def ver_cuenta(request, mesa_id: int):
    mesa = get_object_or_404(Mesa,id=mesa_id)
    pedido = Pedido.objects.filter(mesa=mesa,estado="pendiente").first()
    if pedido:
        detalles = pedido.detallepedido_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.subtotal
    else:
        detalles = []
        total = 0

    contexto = { #Conexion con HTML, es decir variables para HTML
        "mesa": mesa,
        "pedido": pedido,
        "detalles": detalles,
        "total": total
    }
    return render(request,"core/pedido.html",contexto)

@require_POST
def cobrar_mesa(request, mesa_id: int):
    mesa = get_object_or_404(Mesa,id=mesa_id)
    pedido = Pedido.objects.filter(mesa=mesa, estado="pendiente").first()
    if pedido:
        pedido.estado = "estado"
        pedido.save()
    return redirect('home')

def home(request):
    mesas = Mesa.objects.all()
    for mesa in mesas:
        pedido = Pedido.objects.filter(mesa=mesa,estado="pendiente").first()
        if pedido:
            mesa.estado = "ocupada"
            detalles = pedido.detallepedido_set.all()
            total = 0
            for detalle in detalles:
                total+=detalle.subtotal
            mesa.total_pendiente = total
        else:
            mesa.estado = "libre"
            mesa.total_pendiente = 0
    return render(request, "core/home.html", {"mesas":mesas})