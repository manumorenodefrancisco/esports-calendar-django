from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        # Validar correo electrónico
        if '@' not in attrs['email']:
            raise serializers.ValidationError("Correo electrónico no tiene @")

        if any(domain in attrs["email"] for domain in [".ru", ".xyz"]):
            raise serializers.ValidationError("El dominio del correo no está permitido")

        # Validar contraseña

        tiene_numero = any(letra.isdigit() for letra in attrs["password"])
        if not tiene_numero:
            raise serializers.ValidationError("Mínimo un carácter numérico")

        # Si el usuario pasa todas las validaciones le dejamos iniciar sesión

        # Buscamos el correo (Si usuario existe)
        # SELECT * FROM User WHERE email = attrs["email"]

        # Nos retorna el primer objeto de la query o un None
        user = User.objects.filter(email=attrs["email"]).first()
        # try:
        #     user2 = User.objects.get(email=attrs["email"])
        # except User.DoesNotExist:
        #     raise serializers.ValidationError("El usuario no existe")

        # Si existe, comparamos contraseñas

        # Si coincide, iniciamos sesión

        if not user:  # Si user no es None
            raise serializers.ValidationError("El usuario no existe")

        if not user.check_password(attrs["password"]):  # Si las contraseñas no coinciden
            raise serializers.ValidationError("Usuario o contraseña incorrecto")

        # Iniciamos sesión
        refresh = RefreshToken.for_user(user)  # Diccionario
        refresh["username"] = user.username

        return {
            "success": True,
            "data": {
                "refreshToken": str(refresh),
                "token": str(refresh.access_token),
                "email": user.email,
                "username": user.username
            }
        }
