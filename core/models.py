from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    descripcion = models.TextField(blank=True,null = True, verbose_name="Descripicion")
    disponible = models.BooleanField(default=True,verbose_name= "Disponible?")

    def __str__(self):
        return f"{self.nombre}: {self.precio}"