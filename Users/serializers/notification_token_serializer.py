from rest_framework import serializers
from Users.models.users_model import User


class NotificationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["notification_token"]

    def update(self, instance, validated_data):
        instance.notification_token = validated_data.get("notification_token")
        instance.save()
        return instance
