from django.db import models
from Users.models.users_model import User
from Events.models.event_model import Evento

class Suscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    recordatorio_1_dia = models.BooleanField(default=False)
    recordatorio_1_hora = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')
        #esto sirve para no guardar mas de 1 fila con mismo usuario y evento, no duplicados

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}"
