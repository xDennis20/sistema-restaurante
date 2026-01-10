from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Plato(models.Model):
    TALLAS = [
        ("P", "Pequeño"),
        ("M", "Mediano"),
        ("G", "Grande"),
        ("U", "Unico")
    ]
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    descripcion = models.TextField(blank=True,null=True, verbose_name="Descripicion")
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT)
    disponible = models.BooleanField(default=True,verbose_name= "Disponible?")
    talla = models.CharField(max_length=1, choices=TALLAS, default="U", verbose_name= "Tamaño")

    def __str__(self):
        return f"{self.nombre}: ${self.precio} Tamaño: {self.get_talla_display()}"

class Mesa(models.Model):
    numero = models.IntegerField(unique=True,verbose_name="Numero de mesa")
    nombre = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"Mesa {self.numero}"

class Pedido(models.Model):
    ESTADOS = [
        ("pendiente","Pendiente"),
        ("pagado","Pagado")
    ]

    mesa = models.ForeignKey(Mesa,on_delete=models.PROTECT)
    estado = models.CharField(max_length=40, choices= ESTADOS, default="pendiente")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad de plato")
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    nota = models.TextField(blank=True, null=True, verbose_name="Nota")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.plato.precio
        super().save(*args,**kwargs)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre}"