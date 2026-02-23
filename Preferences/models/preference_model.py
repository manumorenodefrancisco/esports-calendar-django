from datetime import timezone

from django.db import models
from Users.models.users_model import User

class Preferencia(models.Model):
    TIPO_PREFERENCIA_CHOICES = [
        ('videojuego', 'Videojuego'),
        ('jugador', 'Jugador/Equipo'),
        ('liga', 'Liga'),
        ('torneo', 'Torneo'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_preferencia = models.CharField(max_length=20, choices=TIPO_PREFERENCIA_CHOICES)
    valor = models.CharField(max_length=150)  # nombre del videojuego, jugador....
    valor_id = models.IntegerField(null=True, blank=True)  # ID externo si aplica (ej: player_id)
    
    puntaje_interes = models.FloatField(default=0.0) #0.0 al 10.0
    frecuencia = models.IntegerField(default=0)  # cuántas veces aparece en suscripciones
    total_suscripciones_usuario = models.IntegerField(default=0)  # total de suscripciones del usuario
    
    created_at = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['usuario', 'tipo_preferencia', 'valor']
        ordering = ['-puntaje_interes', '-frecuencia']

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_preferencia}: {self.valor}"
