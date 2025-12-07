from django.shortcuts import render
from .models import Producto,Categoria
# Create your views here.

def menu_restuarante(request):
    cargar_productos = Producto.objects.filter(disponible=True)
    cargar_categorias = Categoria.objects.all()

    contexto = {
        "productos" : cargar_productos,
        "categorias" : cargar_categorias
    }

    return render(request, "core/menu.html", contexto)