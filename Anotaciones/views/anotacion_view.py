from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Anotaciones.models import Anotacion
from Anotaciones.serializers import AnotacionSerializer


class AnotacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        anotaciones = Anotacion.objects.filter(usuario=request.user)
        serializer = AnotacionSerializer(anotaciones, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        serializer = AnotacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors})