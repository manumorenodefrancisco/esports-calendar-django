from rest_framework import serializers
from Anotaciones.models import Anotacion


class AnotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotacion
        fields = ['id', 'titulo', 'descripcion', 'fecha_hora', 'created_at']