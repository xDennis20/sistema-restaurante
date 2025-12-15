from django.db.models import QuerySet,Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Plato,Categoria,DetallePedido,Mesa,Pedido
from django.utils import timezone
from django.contrib.admin.views.decorators import user_passes_test
# Create your views here.
def obtener_datos_mesa(mesa_id: int) -> tuple:
    mesa = get_object_or_404(Mesa, id= mesa_id)
    pedido = Pedido.objects.filter(mesa=mesa,estado="pendiente").first()
    return mesa,pedido

def filtrar_categorias_platos(platos:QuerySet, categoria_id: int):
    if categoria_id:
        return platos.filter(categoria_id= categoria_id)
    return platos
def menu_restuarante(request,mesa_id: int):
    mesa,pedido_actual = obtener_datos_mesa(mesa_id)
    cargar_platos = Plato.objects.filter(disponible=True)
    cargar_categorias = Categoria.objects.all()
    categoria_id = request.GET.get("categoria")
    if categoria_id:
        try:
            cargar_platos = filtrar_categorias_platos(cargar_platos,int(categoria_id))
        except ValueError:
            pass
    detalles_actual = pedido_actual.detallepedido_set.all() if pedido_actual else []

    contexto = {
        "mesa" : mesa,
        "productos" : cargar_platos,
        "categorias" : cargar_categorias,
        "detalles_actuales": detalles_actual,
        "pedido_actual" : pedido_actual,
    }

    return render(request, "core/menu.html", contexto)

def agregar_producto_a_mesa(request,mesa_id: int,plato_id: int):
    plato = get_object_or_404(Plato,id=plato_id)
    mesa = get_object_or_404(Mesa,id=mesa_id)

    pedido,creado = Pedido.objects.get_or_create(
        mesa = mesa,
        estado = "pendiente"
    )
    cantidad_recibida = int(request.POST.get("cantidad", 1))
    detalle_existente = DetallePedido.objects.filter(plato=plato,pedido=pedido).first()

    if detalle_existente:
        detalle_existente.cantidad += cantidad_recibida
        detalle_existente.save()
    else:
        DetallePedido.objects.create(
            pedido = pedido,
            cantidad = cantidad_recibida,
            plato = plato,
        )
    return redirect("menu",mesa_id=mesa_id)

def ver_cuenta(request, mesa_id: int):
    mesa,pedido = obtener_datos_mesa(mesa_id)
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
        pedido.estado = "pagado"
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

def eliminar_detalle(request,detalle_id: int):
    detalle = get_object_or_404(DetallePedido,id=detalle_id)
    detalle.delete()
    return redirect("menu",mesa_id=detalle.pedido.mesa.id)

def crear_mesa(request):
    ultima_mesa = Mesa.objects.order_by("numero").last()
    if ultima_mesa:
        nuevo_numero = ultima_mesa.numero + 1
    else:
        nuevo_numero = ultima_mesa.numero = 1
    Mesa.objects.create(
        numero=nuevo_numero,
        nombre=f"Mesa {nuevo_numero}"
    )
    return redirect("home")

def es_admin(user):
    return user.is_staff

@user_passes_test(es_admin)
def reporte_ventas_hoy(request):
    fecha_hoy = timezone.now().date()
    ventas_hoy = Pedido.objects.filter(estado="pagado",creado_en__date= fecha_hoy)
    print(f"DEBUG: Encontré {ventas_hoy.count()} pedidos pagados.")
    total = 0
    for venta in ventas_hoy:
        total += sum(p.subtotal for p in venta.detallepedido_set.all())

    contexto = {
        "fecha_hoy" : fecha_hoy,
        "ventas_hoy" : ventas_hoy,
        "total" : total
    }
    return render(request,"core/reporte.html", contexto)
