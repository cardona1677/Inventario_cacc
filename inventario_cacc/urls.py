"""
URL configuration for inventario_cacc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import (
    login_view, home, registro, admin_dashboard, logout_view,
    productos, crear_producto, editar_producto, eliminar_producto,
    categorias, crear_categoria, editar_categoria, eliminar_categoria,
    proveedores, crear_proveedor, editar_proveedor, eliminar_proveedor,
    clientes, crear_cliente, editar_cliente, eliminar_cliente,
    movimientos, crear_movimiento, eliminar_movimiento,
    agregar_carrito, ver_carrito, eliminar_del_carrito, actualizar_cantidad_carrito, vaciar_carrito, mis_pedidos, confirmar_pedido, cambiar_estado_pedido,
    pedidos_admin
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro, name='registro'),
    path('home/', home, name='home'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # Productos
    path('productos/', productos, name='productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),
    
    # Categorías
    path('categorias/', categorias, name='categorias'),
    path('categorias/crear/', crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', eliminar_categoria, name='eliminar_categoria'),
    
    # Proveedores
    path('proveedores/', proveedores, name='proveedores'),
    path('proveedores/crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', eliminar_proveedor, name='eliminar_proveedor'),
    
    # Clientes
    path('clientes/', clientes, name='clientes'),
    path('clientes/crear/', crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', eliminar_cliente, name='eliminar_cliente'),
    
    # Movimientos
    path('movimientos/', movimientos, name='movimientos'),
    path('movimientos/crear/', crear_movimiento, name='crear_movimiento'),
    path('movimientos/eliminar/<int:id>/', eliminar_movimiento, name='eliminar_movimiento'),
    
    # Carrito y Pedidos
    path('carrito/agregar/', agregar_carrito, name='agregar_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar/<int:producto_id>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),
    path('mis-pedidos/', mis_pedidos, name='mis_pedidos'),
    path('confirmar-pedido/', confirmar_pedido, name='confirmar_pedido'),
    path('pedido/cambiar-estado/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/', pedidos_admin, name='pedidos_admin'),
]
