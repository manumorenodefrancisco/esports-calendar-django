from rest_framework import serializers
from Events.models.event_model import Evento


class EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evento
        fields = [
            "id",
            "external_id",
            "nombre",
            "videojuego",
            "tipo_evento",
            "fecha_inicio",
            "fecha_fin",
            "color",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]
