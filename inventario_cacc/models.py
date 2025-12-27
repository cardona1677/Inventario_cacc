from django.db import models
from django.contrib.auth.models import User


# =========================
# TABLA CATEGORÍA
# =========================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre


# =========================
# TABLA PROVEEDOR
# =========================
class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre


# =========================
# TABLA PRODUCTO
# =========================
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        db_column='categoria_id'
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        db_column='proveedor_id'
    )
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre


# =========================
# TABLA CLIENTE
# =========================
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.nombre
    

class Perfil(models.Model):
    ROLES = (
        (1, "Administrador"),
        (2, "Cliente"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.IntegerField(choices=ROLES, default=2)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
    

# =========================
# TABLA PEDIDO
# =========================
class Pedido(models.Model):
    id = models.BigAutoField(primary_key=True)
    ESTADO_CHOICES = (
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'Procesando'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='usuario_id'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    direccion_entrega = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


# =========================
# TABLA DETALLE PEDIDO
# =========================
class DetallePedido(models.Model):
    id = models.BigAutoField(primary_key=True)
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='pedido_id'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        db_column='producto_id'
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedido'

    def __str__(self):
        return f"Detalle Pedido #{self.pedido.id} - {self.producto.nombre if self.producto else 'N/A'}"
    

class MovimientoInventario(models.Model):

    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='producto_id'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        db_column='usuario_id'
    )
    cliente = models.ForeignKey(
        Cliente,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column='cliente_id'
    )
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='pedido_id'
    )
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'movimiento_inventario'

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
    
    @property
    def pedido_relacionado(self):
        return self.pedido
