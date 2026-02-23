from rest_framework import serializers
from Preferences.models.preference_model import Preferencia


class PreferenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferencia
        fields = [
            "id",
            "tipo_preferencia",
            "valor",
            "valor_id",
            "puntaje_interes",
            "frecuencia",
            "total_suscripciones_usuario",
            "ultima_actualizacion",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "puntaje_interes",
            "frecuencia",
            "total_suscripciones_usuario",
            "ultima_actualizacion",
            "created_at"
        ]
