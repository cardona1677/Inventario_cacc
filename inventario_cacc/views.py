from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *

#region login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Usar get_or_create para evitar el error DoesNotExist
            perfil, created = Perfil.objects.get_or_create(
                user=user,
                defaults={'rol': 2}  # Si se crea, asignar rol de cliente por defecto
            )

            if perfil.rol == 1:
                return redirect("admin_dashboard")  # Vista admin
            else:
                return redirect("home")  # Vista cliente

        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("login")

    return render(request, "auth/login.html")

def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return redirect("registro")

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)

        # Crear Perfil asignando rol por defecto (cliente)
        Perfil.objects.create(user=user, rol=2)

        messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "auth/registro.html")

#endregion


#region productos
@login_required
def productos(request):
    productos = Producto.objects.all().select_related('categoria', 'proveedor')
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'proveedores': proveedores,
    }
    return render(request, 'Productos/productos.html', context)

@login_required
def crear_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        categoria_id = request.POST.get("categoria")
        proveedor_id = request.POST.get("proveedor")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        descripcion = request.POST.get("descripcion")

        try:
            Producto.objects.create(
                nombre=nombre,
                categoria_id=categoria_id if categoria_id else None,
                proveedor_id=proveedor_id if proveedor_id else None,
                precio=precio,
                stock=stock,
                descripcion=descripcion
            )
            messages.success(request, "Producto creado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al crear el producto: {str(e)}")
        
        return redirect("productos")

@login_required
def eliminar_producto(request, id):
    if request.method == "POST":
        try:
            producto = Producto.objects.get(id=id)
            producto.delete()
            messages.success(request, "Producto eliminado exitosamente.")
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el producto: {str(e)}")
    
    return redirect("productos")

@login_required
def editar_producto(request, id):
    if request.method == "POST":
        try:
            producto = Producto.objects.get(id=id)
            producto.nombre = request.POST.get("nombre")
            producto.categoria_id = request.POST.get("categoria") if request.POST.get("categoria") else None
            producto.proveedor_id = request.POST.get("proveedor") if request.POST.get("proveedor") else None
            producto.precio = request.POST.get("precio")
            producto.stock = request.POST.get("stock")
            producto.descripcion = request.POST.get("descripcion")
            producto.save()
            messages.success(request, "Producto actualizado exitosamente.")
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el producto: {str(e)}")
    
    return redirect("productos")

#endregion


#region categorias
@login_required
def categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'Categorias/categorias.html', context)

@login_required
def crear_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        
        try:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, "Categoría creada exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al crear la categoría: {str(e)}")
    
    return redirect("categorias")

@login_required
def eliminar_categoria(request, id):
    if request.method == "POST":
        try:
            categoria = Categoria.objects.get(id=id)
            categoria.delete()
            messages.success(request, "Categoría eliminada exitosamente.")
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar la categoría: {str(e)}")
    
    return redirect("categorias")

@login_required
def editar_categoria(request, id):
    if request.method == "POST":
        try:
            categoria = Categoria.objects.get(id=id)
            categoria.nombre = request.POST.get("nombre")
            categoria.descripcion = request.POST.get("descripcion")
            categoria.save()
            messages.success(request, "Categoría actualizada exitosamente.")
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría no existe.")
        except Exception as e:
            messages.error(request, f"Error al actualizar la categoría: {str(e)}")
    
    return redirect("categorias")

@login_required
def proveedores(request):
    proveedores = Proveedor.objects.all()
    context = {'proveedores': proveedores}
    return render(request, 'Proveedores/proveedores.html', context)

@login_required
def crear_proveedor(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")
        
        try:
            Proveedor.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                direccion=direccion
            )
            messages.success(request, "Proveedor creado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al crear el proveedor: {str(e)}")
    
    return redirect("proveedores")

@login_required
def eliminar_proveedor(request, id):
    if request.method == "POST":
        try:
            proveedor = Proveedor.objects.get(id=id)
            proveedor.delete()
            messages.success(request, "Proveedor eliminado exitosamente.")
        except Proveedor.DoesNotExist:
            messages.error(request, "El proveedor no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el proveedor: {str(e)}")
    
    return redirect("proveedores")

@login_required
def editar_proveedor(request, id):
    if request.method == "POST":
        try:
            proveedor = Proveedor.objects.get(id=id)
            proveedor.nombre = request.POST.get("nombre")
            proveedor.telefono = request.POST.get("telefono")
            proveedor.email = request.POST.get("email")
            proveedor.direccion = request.POST.get("direccion")
            proveedor.save()
            messages.success(request, "Proveedor actualizado exitosamente.")
        except Proveedor.DoesNotExist:
            messages.error(request, "El proveedor no existe.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el proveedor: {str(e)}")
    
    return redirect("proveedores")

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    total_usuarios = Perfil.objects.filter(rol=2).count()
    context = {
        'clientes': clientes,
        'total_usuarios': total_usuarios
    }
    return render(request, 'Clientes/clientes.html', context)

@login_required
def crear_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")
        
        try:
            Cliente.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                direccion=direccion
            )
            messages.success(request, "Cliente creado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al crear el cliente: {str(e)}")
    
    return redirect("clientes")

@login_required
def editar_cliente(request, id):
    if request.method == "POST":
        try:
            cliente = Cliente.objects.get(id=id)
            cliente.nombre = request.POST.get("nombre")
            cliente.telefono = request.POST.get("telefono")
            cliente.email = request.POST.get("email")
            cliente.direccion = request.POST.get("direccion")
            cliente.save()
            messages.success(request, "Cliente actualizado exitosamente.")
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente no existe.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el cliente: {str(e)}")
    
    return redirect("clientes")

@login_required
def eliminar_cliente(request, id):
    if request.method == "POST":
        try:
            cliente = Cliente.objects.get(id=id)
            cliente.delete()
            messages.success(request, "Cliente eliminado exitosamente.")
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el cliente: {str(e)}")
    
    return redirect("clientes")

@login_required
def movimientos(request):
    from django.utils import timezone
    from datetime import datetime
    
    # Obtener filtros
    tipo_filtro = request.GET.get('tipo')
    producto_filtro = request.GET.get('producto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Query inicial
    movimientos_query = MovimientoInventario.objects.all().select_related('producto', 'cliente', 'usuario')
    
    # Aplicar filtros
    if tipo_filtro:
        movimientos_query = movimientos_query.filter(tipo=tipo_filtro)
    if producto_filtro:
        movimientos_query = movimientos_query.filter(producto_id=producto_filtro)
    if fecha_desde:
        movimientos_query = movimientos_query.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        fecha_hasta_dt = fecha_hasta_dt.replace(hour=23, minute=59, second=59)
        movimientos_query = movimientos_query.filter(fecha__lte=fecha_hasta_dt)
    
    movimientos_query = movimientos_query.order_by('-fecha')
    
    # Estadísticas
    total_entradas = MovimientoInventario.objects.filter(tipo='ENTRADA').count()
    total_salidas = MovimientoInventario.objects.filter(tipo='SALIDA').count()
    movimientos_hoy = MovimientoInventario.objects.filter(fecha__date=timezone.now().date()).count()
    
    context = {
        'movimientos': movimientos_query,
        'productos': Producto.objects.all(),
        'clientes': Cliente.objects.all(),
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
        'movimientos_hoy': movimientos_hoy,
    }
    return render(request, 'Movimientos/movimientos.html', context)

@login_required
def crear_movimiento(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad"))
        cliente_id = request.POST.get("cliente")
        descripcion = request.POST.get("descripcion")
        
        try:
            producto = Producto.objects.get(id=producto_id)
            
            # Validar stock para salidas
            if tipo == 'SALIDA' and producto.stock < cantidad:
                messages.error(request, f"Stock insuficiente. Stock actual: {producto.stock}, cantidad solicitada: {cantidad}")
                return redirect("movimientos")
            
            # Crear movimiento
            MovimientoInventario.objects.create(
                producto=producto,
                tipo=tipo,
                cantidad=cantidad,
                cliente_id=cliente_id if cliente_id else None,
                usuario=request.user,
                descripcion=descripcion
            )
            
            # Actualizar stock
            if tipo == 'ENTRADA':
                producto.stock += cantidad
            else:  # SALIDA
                producto.stock -= cantidad
            producto.save()
            
            messages.success(request, f"Movimiento registrado exitosamente. Nuevo stock de {producto.nombre}: {producto.stock}")
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")
        except Exception as e:
            messages.error(request, f"Error al crear el movimiento: {str(e)}")
    
    return redirect("movimientos")

@login_required
def eliminar_movimiento(request, id):
    if request.method == "POST":
        try:
            movimiento = MovimientoInventario.objects.get(id=id)
            producto = movimiento.producto
            
            # Revertir el cambio en el stock
            if movimiento.tipo == 'ENTRADA':
                producto.stock -= movimiento.cantidad
            else:  # SALIDA
                producto.stock += movimiento.cantidad
            
            producto.save()
            movimiento.delete()
            
            messages.success(request, f"Movimiento eliminado. Stock actualizado de {producto.nombre}: {producto.stock}")
        except MovimientoInventario.DoesNotExist:
            messages.error(request, "El movimiento no existe.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el movimiento: {str(e)}")
    
    return redirect("movimientos")
#endregion


#region carrito y pedidos
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def agregar_carrito(request):
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    try:
        producto = Producto.objects.get(id=producto_id)
        
        # Validar stock
        if producto.stock < cantidad:
            return JsonResponse({
                'success': False,
                'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
            })
        
        # Obtener o crear carrito en sesión
        carrito = request.session.get('carrito', {})
        
        # Si el producto ya está en el carrito, aumentar cantidad
        if str(producto_id) in carrito:
            nueva_cantidad = carrito[str(producto_id)]['cantidad'] + cantidad
            if nueva_cantidad > producto.stock:
                return JsonResponse({
                    'success': False,
                    'error': f'Stock insuficiente. Solo hay {producto.stock} unidades disponibles.'
                })
            carrito[str(producto_id)]['cantidad'] = nueva_cantidad
        else:
            # Agregar nuevo producto al carrito
            carrito[str(producto_id)] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
            }
        
        # Guardar carrito en sesión
        request.session['carrito'] = carrito
        request.session.modified = True
        
        # Calcular total de items en carrito
        carrito_count = sum(item['cantidad'] for item in carrito.values())
        
        return JsonResponse({
            'success': True,
            'carrito_count': carrito_count
        })
        
    except Producto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Producto no encontrado'
        })

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    
    # Calcular totales
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    carrito_count = sum(item['cantidad'] for item in carrito.values())
    
    context = {
        'carrito': carrito,
        'total': total,
        'carrito_count': carrito_count,
    }
    return render(request, 'Home/carrito.html', context)

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito")
    
    return redirect('ver_carrito')

@login_required
def actualizar_cantidad_carrito(request, producto_id):
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        
        if str(producto_id) in carrito and cantidad > 0:
            # Validar stock
            try:
                producto = Producto.objects.get(id=producto_id)
                if cantidad <= producto.stock:
                    carrito[str(producto_id)]['cantidad'] = cantidad
                    request.session['carrito'] = carrito
                    request.session.modified = True
                    messages.success(request, "Cantidad actualizada")
                else:
                    messages.error(request, f"Stock insuficiente. Solo hay {producto.stock} unidades disponibles.")
            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado")
    
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    messages.success(request, "Carrito vaciado")
    return redirect('ver_carrito')

@login_required
def mis_pedidos(request):
    from .models import Pedido
    
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related('detallepedido_set__producto').order_by('-fecha')
    
    # Estadísticas
    total_pedidos = pedidos.count()
    pedidos_pendientes = pedidos.filter(estado='PENDIENTE').count()
    pedidos_entregados = pedidos.filter(estado='ENTREGADO').count()
    
    # Contador del carrito
    carrito = request.session.get('carrito', {})
    carrito_count = sum(item['cantidad'] for item in carrito.values())
    
    context = {
        'pedidos': pedidos,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_entregados': pedidos_entregados,
        'carrito_count': carrito_count,
    }
    return render(request, 'Pedidos/pedidos.html', context)

@login_required
def confirmar_pedido(request):
    from .models import Pedido, DetallePedido
    from django.db import transaction
    
    if request.method == "POST":
        carrito = request.session.get('carrito', {})
        
        if not carrito:
            messages.error(request, "El carrito está vacío")
            return redirect('ver_carrito')
        
        direccion_entrega = request.POST.get('direccion_entrega')
        observaciones = request.POST.get('observaciones')
        
        try:
            with transaction.atomic():
                # Calcular total
                total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
                
                # Crear pedido
                pedido = Pedido.objects.create(
                    usuario=request.user,
                    total=total,
                    direccion_entrega=direccion_entrega,
                    observaciones=observaciones,
                    estado='PENDIENTE'
                )
                
                # Crear detalles, actualizar stock y registrar movimientos
                for producto_id, item in carrito.items():
                    producto = Producto.objects.select_for_update().get(id=producto_id)
                    
                    # Validar stock
                    if producto.stock < item['cantidad']:
                        raise ValueError(f"Stock insuficiente para {producto.nombre}")
                    
                    # Crear detalle del pedido
                    subtotal = item['precio'] * item['cantidad']
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio'],
                        subtotal=subtotal
                    )
                    
                    # Actualizar stock
                    producto.stock -= item['cantidad']
                    producto.save()
                    
                    # Registrar movimiento de inventario (SALIDA)
                    MovimientoInventario.objects.create(
                        producto=producto,
                        tipo='SALIDA',
                        cantidad=item['cantidad'],
                        usuario=request.user,
                        pedido=pedido,  # Relacionar con el pedido
                        descripcion=f"Venta - Pedido #{pedido.id} - Cliente: {request.user.username}"
                    )
                
                # Vaciar carrito
                request.session['carrito'] = {}
                request.session.modified = True
                
                messages.success(request, f"¡Pedido #{pedido.id} realizado exitosamente! Te contactaremos pronto.")
                return redirect('mis_pedidos')
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('ver_carrito')
        except Exception as e:
            messages.error(request, f"Error al procesar el pedido: {str(e)}")
            return redirect('ver_carrito')
    
    return redirect('ver_carrito')

@login_required
def cambiar_estado_pedido(request, pedido_id):
    from .models import Pedido
    
    if request.method == "POST":
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            nuevo_estado = request.POST.get('nuevo_estado')
            
            estado_anterior = pedido.estado
            pedido.estado = nuevo_estado
            pedido.save()
            
            messages.success(request, f"Estado del Pedido #{pedido.id} cambiado de {estado_anterior} a {nuevo_estado}")
        except Pedido.DoesNotExist:
            messages.error(request, "El pedido no existe")
        except Exception as e:
            messages.error(request, f"Error al cambiar el estado: {str(e)}")
    
    return redirect('movimientos')

@login_required
def pedidos_admin(request):
    from .models import Pedido
    from django.utils import timezone
    from datetime import datetime
    
    # Obtener filtros
    estado_filtro = request.GET.get('estado')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Query inicial
    pedidos_query = Pedido.objects.all().prefetch_related('detallepedido_set__producto', 'usuario').order_by('-fecha')
    
    # Aplicar filtros
    if estado_filtro:
        pedidos_query = pedidos_query.filter(estado=estado_filtro)
    if fecha_desde:
        pedidos_query = pedidos_query.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        fecha_hasta_dt = fecha_hasta_dt.replace(hour=23, minute=59, second=59)
        pedidos_query = pedidos_query.filter(fecha__lte=fecha_hasta_dt)
    
    # Estadísticas
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='PENDIENTE').count()
    pedidos_proceso = Pedido.objects.filter(estado='EN_PROCESO').count()
    pedidos_entregados = Pedido.objects.filter(estado='ENTREGADO').count()
    
    context = {
        'pedidos': pedidos_query,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_proceso': pedidos_proceso,
        'pedidos_entregados': pedidos_entregados,
    }
    return render(request, 'Pedidos/pedidos_admin.html', context)
#endregion


#region home
@login_required
def home(request):
    # Obtener parámetros de búsqueda y filtros
    buscar = request.GET.get('buscar', '')
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', '')
    
    # Query inicial - solo productos con stock
    productos = Producto.objects.filter(stock__gt=0).select_related('categoria', 'proveedor')
    
    # Aplicar búsqueda
    if buscar:
        productos = productos.filter(nombre__icontains=buscar)
    
    # Aplicar filtro de categoría
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    # Aplicar ordenamiento
    if orden:
        productos = productos.order_by(orden)
    else:
        productos = productos.order_by('nombre')
    
    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()
    
    # Obtener contador del carrito
    carrito = request.session.get('carrito', {})
    carrito_count = sum(item['cantidad'] for item in carrito.values())
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'carrito_count': carrito_count,
    }
    return render(request, 'Home/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    context = {
        "total_categorias": Categoria.objects.count(),
        "total_proveedores": Proveedor.objects.count(),
        "total_productos": Producto.objects.count(),
        "total_clientes": Cliente.objects.count(),
        "total_usuarios": Perfil.objects.filter(rol=2).count(),  # Usuarios clientes del sistema
        "movimientos": MovimientoInventario.objects.order_by('-fecha')[:10],
    }
    return render(request, "Home/dashboard_admin.html", context)

#endregion