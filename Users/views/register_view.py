"""
Descargamos:
    - djangorestframework
    - djangorestframework-simplejwt
    - django-cors-headers

    comandos:
        - pip install djangorestframework
        - pip install djangorestframework-simplejwt
        - pip install django-cors-headers

    Métodos de solicitudes:
        - get -> Genérico, pero no encripta datos
        - post -> Genérico y encripta datos
        - put -> Crear elementos y funciona a través de POST
        - patch -> Lo utilizamos para actualizar uno o varios valores, pero no todos y funciona con POST.
        - delete -> Funciona con POST lo unico que este se utiliza solo para borrar datos
"""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import User
from Users.serializers import RegisterSerializer


class PruebaView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # SELECT * FROM User
        usuarios = User.objects.all()  # Con esta consulta tenemos un array de objetos de tipo usuario

        # SELECT * FROM User ORDER BY first_name ASC
        usuarios2 = User.objects.all().order_by("-first_name")

        # SELECT * FROM User WHERE is_active=True AND is_staff=True ORDER BY first_name ASC
        usuarios3 = User.objects.filter(is_active=True, is_staff=True).order_by("-first_name")

        # data = []
        # for usuario in usuarios:
        #     data.append({"email": usuario.email, "first_name": usuario.first_name, "last_name": usuario.last_name})

        data2 = [{"email": usuario.email,"first_name": usuario.first_name,"last_name": usuario.last_name} for usuario in usuarios3]

        return Response(
            {"success": True, "data": data2}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Si queremos acceder a los elementos del body, usamos request.data
        # request.data = {'email': 'pepe@gmail.com', 'username': 'pepe_97', 'first_name': 'Pepe', 'last_name': 'Perez'}
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
