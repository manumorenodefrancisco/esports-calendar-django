from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.serializers import LoginSerializer


class LoginView(APIView): #viewsets.ModelViewSet
    permission_classes = [AllowAny]

    def post(self, request):
        datos = request.data
        serializer = LoginSerializer(data=datos)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        errores = []
        for error in serializer.errors.values():
            for e in error:
                errores.append(e)

        return Response({"success": False, "errors": errores}, status=status.HTTP_400_BAD_REQUEST)
