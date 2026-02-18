from rest_framework import serializers
from Preferences.models.preference_model import Preferencia


class PreferenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferencia
        fields = [
            "id",
            "videojuego",
            "tipo_evento",
            "puntaje_interes",
            "total_suscripciones",
            "ultima_actualizacion"
        ]
        read_only_fields = [
            "id",
            "puntaje_interes",
            "total_suscripciones",
            "ultima_actualizacion"
        ]
