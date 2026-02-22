"""
Descargar estas librerías:
    - djangorestframework: Herramienta principal para construir APIs robustas y navegables en Django.
    - djangorestframework-simplejwt: Proporciona autenticación mediante 'JSON Web Tokens' para asegurar tu API.
    - django-cors-headers: Maneja el intercambio de recursos de origen cruzado (CORS) para permitir que apps
            externas (front) consuman tu API. Aporta los permisos a peticiones desde otro dominio.

comando -> pip install djangorestframework djangorestframework-simplejwt django-cors-headers

    Métodos de solicitudes:
        - get -> Genérico, pero no encripta datos. Para datos en la URL -> request.query_params
        - post -> Genérico y encripta datos. Para datos en el cuerpo -> request.data
        - put -> Crear elementos y funciona a través de POST
        - patch -> Lo utilizamos para actualizar uno o varios valores, pero no todos y funciona con POST.
        - delete -> Funciona con POST lo unico que este se utiliza solo para borrar datos
"""
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import User
from Users.serializers import RegisterSerializer


class PruebaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # SELECT * FROM User WHERE is_active=True AND is_staff=True ORDER BY first_name DESC
        usuarios_staff = User.objects.filter(is_active=True, is_staff=True).order_by("first_name")

        # data = []
        # for usuario in usuarios:
        #     data.append({"username": usuario.username, "email": usuario.email})

        data = [{"username": usuario.username, "email": usuario.email} for usuario in usuarios_staff]

        return Response(
            {"success": True, "data": data}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Si queremos acceder a los elementos del body, usamos request.data
        # request.data = {'email': 'pepe@gmail.com', 'username': 'pepe_97', 'first_name'....}
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:

            # {"email": ["El correo ya existe"], "username": ["El nombre de usuario ya existe"]}
            errores = []
            for error in serializer.errors.values():
                for e in error:
                    errores.append(e)

            return Response({"success": False, "errors": errores}, status=status.HTTP_400_BAD_REQUEST)
