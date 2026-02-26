from rest_framework import serializers
from Subscriptions.models.subscription_model import Suscripcion
from Events.serializers.event_serializer import EventoSerializer

class SuscripcionSerializer(serializers.ModelSerializer):

    evento = EventoSerializer(read_only=True)
    evento_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Suscripcion
        fields = [
            "id",
            "evento",
            "evento_id",
            "recordatorio_1_dia",
            "recordatorio_1_hora",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        evento_id = validated_data.pop("evento_id") # evento_id no es un campo del modelo, lo borramos
        usuario = self.context["user"]

        return Suscripcion.objects.create(
            usuario=usuario, evento_id=evento_id, **validated_data
        )
