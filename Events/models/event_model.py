from django.db import models

class Evento(models.Model):
    external_id = models.CharField(max_length=100, unique=True) #de la api pandascore
    nombre = models.CharField(max_length=200)
    videojuego = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=100) #tipo de videojuego

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)

    color = models.CharField(max_length=20, default="#2196F3")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.videojuego}"
