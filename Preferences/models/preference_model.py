from datetime import timezone

from django.db import models
from Users.models.users_model import User

class Preferencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    videojuego = models.CharField(max_length=100)
    tipo_evento = models.CharField(max_length=100, null=True, blank=True)

    puntaje_interes = models.FloatField(default=0)
    total_suscripciones = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.videojuego}"
