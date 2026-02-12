from rest_framework import serializers

from Users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True, min_length=3)
    last_name = serializers.CharField(required=True, min_length=3)
    password1 = serializers.CharField(required=True, min_length=6)
    password2 = serializers.CharField(required=True, min_length=6)

    class Meta:
        model = User
        fields = (
            "email", "username", "first_name",
            "last_name", "password1", "password2"
        )

    def validate_email(self, value):
        # SELECT * FROM User WHERE email = value
        exist = User.objects.filter(email=value).exists()
        if exist:
            raise serializers.ValidationError("El correo ya existe")

        if any(domain in value for domain in [".ru", ".xyz"]):
            raise serializers.ValidationError("El dominio del correo no está permitido")

        return value

    def validate_username(self, value):
        # SELECT * FROM User WHERE username = value
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return value

    def validate_password1(self, value):
        tiene_numero = any(letra.isdigit() for letra in value)
        if not tiene_numero:
            raise serializers.ValidationError("Mínimo un carácter numérico")
        return value

    def validate(self, attrs):
        # attrs = {'email': 'pepe@gmail.com', 'username': 'pepe_97', 'first_name': 'Pepe', 'last_name': 'Perez'}
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Contraseñas no coinciden")
        return attrs

    def create(self, validated_data):
        # validate_data = {
            # 'email': 'pepe@gmail.com',
            # 'username': 'pepe_97',
            # 'first_name': 'Pepe',
            # 'last_name': 'Perez',
            # 'password1': 'holamundo1',
            # 'password2': 'holamundo1',
        # }
        validated_data.pop("password2")
        password = validated_data.pop("password1")
        # validate_data = {
            # 'email': 'pepe@gmail.com',
            # 'username': 'pepe_97',
            # 'first_name': 'Pepe',
            # 'last_name': 'Perez',
        # }
        # password = "holamundo1"

        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(password)
        user.save()
        return user
