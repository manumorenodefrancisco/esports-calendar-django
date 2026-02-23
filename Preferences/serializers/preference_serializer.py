from rest_framework import serializers
from Preferences.models.preference_model import Preferencia


class PreferenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferencia
        fields = [
            "id",
            "videojuego",
            "puntaje_interes",
            "total_suscripciones",
            "ultima_actualizacion",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "puntaje_interes",
            "total_suscripciones",
            "ultima_actualizacion",
            "created_at"
        ]
