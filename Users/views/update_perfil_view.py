from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import InfoPerfil
from Users.serializers import UpdatePerfilSerializer, GetPerfilSerializer


class UpdatePerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = InfoPerfil.objects.get(user=request.user)
        except InfoPerfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GetPerfilSerializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            perfil = InfoPerfil.objects.get(user=request.user)
        except InfoPerfil.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePerfilSerializer(perfil, data=request.data, partial=True, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)

        errores = []
        for error in serializer.errors.values():
            for e in error:
                errores.append(e)

        return Response({"success": False, "errors": errores}, status=status.HTTP_400_BAD_REQUEST)
