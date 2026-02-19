from rest_framework import serializers
from Users.models import User


class NotificationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['notification_token']
    
    def validate_notification_token(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El token de notificación no puede estar vacío")

        return value.strip()
