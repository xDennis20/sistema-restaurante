"""
URL configuration for SistemaRestaurante project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core.views import menu_restuarante,agregar_producto_a_mesa,ver_cuenta,cobrar_mesa,home,eliminar_detalle,reporte_ventas_hoy

urlpatterns = [
    path('admin/', admin.site.urls),
    # 1. Portada de la web el home
    path('',home,name='home'),
    # 2. Menu del restauraunte
    path('menu/<int:mesa_id>/', menu_restuarante, name= 'menu'),
    # 3. Acciones que hace la web
    path('agregar/<int:mesa_id>/<int:plato_id>/', agregar_producto_a_mesa, name= 'agregar_plato'),
    path('mesa/<int:mesa_id>', ver_cuenta, name= 'cuenta'),
    path('cobrar/<int:mesa_id>',cobrar_mesa, name = 'cobrar'),
    path('eliminar_detalle/<int:detalle_id>',eliminar_detalle, name= "eliminar_detalle"),
    path('reporte/',reporte_ventas_hoy, name="reporte"),
    path('accounts/', include('django.contrib.auth.urls'))
]
