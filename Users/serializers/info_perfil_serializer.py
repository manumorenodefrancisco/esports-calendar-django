from rest_framework import serializers

from Users.models import InfoPerfil, User


class GetPerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = InfoPerfil
        fields = ("email", "username", "birthday", "phone", "country")


class UpdatePerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, min_length=6)
    birthday = serializers.DateField(required=False)
    phone = serializers.CharField(required=False, max_length=11)
    country = serializers.CharField(required=False, max_length=3)

    class Meta:
        model = InfoPerfil
        fields = ("email", "username", "password", "birthday", "phone", "country")

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("El correo ya existe")
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return value

    def update(self, instance, validated_data):
        user = instance.user
        
        if "email" in validated_data:
            user.email = validated_data.pop("email")
        
        if "username" in validated_data:
            user.username = validated_data.pop("username")
        
        if "password" in validated_data:
            password = validated_data.pop("password")
            user.set_password(password)
        
        user.save()

        if "birthday" in validated_data:
            instance.birthday = validated_data["birthday"]
        
        if "phone" in validated_data:
            instance.phone = validated_data["phone"]
        
        if "country" in validated_data:
            instance.country = validated_data["country"]
        
        instance.save()
        return instance