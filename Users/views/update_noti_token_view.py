from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.models import User
from Users.serializers import NotificationTokenSerializer


# {"notification_token": "token_del_dispositivo"}
class UpdateNotiTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        if 'notification_token' not in data:
            return Response({
                "success": False,
                "message": "Falta el campo notification_token"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = data['notification_token']
        
        if user.notification_token == token:
            return Response({
                "success": True,
                "message": "El token recibido es el mismo que ya había"
            }, status=status.HTTP_200_OK)
        
        # select * from Users excepto a ti mismo que tengan tu token (por si el dispositivo cambió de dueño)
        usuario_anterior = User.objects.filter(notification_token=token).exclude(id=user.id).first()
        if usuario_anterior:
            usuario_anterior.notification_token = None
            usuario_anterior.save()
        
        serializer = NotificationTokenSerializer(user, data={'notification_token': token}, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Token de notificación guardado correctamente"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Error al validar el token",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return self.post(request)
