from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Notifications.services import FCMService

class RegisterTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({"success": False, "errors": ["Token requerido"]})
        
        if not hasattr(request.user, 'fcm_tokens'):
            request.user.fcm_tokens = []
        
        if token not in request.user.fcm_tokens:
            request.user.fcm_tokens.append(token)
        
        return Response({
            "success": True, 
            "data": {"tokens_count": len(request.user.fcm_tokens)}
        })

class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'fcm_tokens') or not request.user.fcm_tokens:
            return Response({"success": False, "errors": ["No tienes tokens registrados"]})
        
        titulo = request.data.get('title', 'Notificación')
        mensaje = request.data.get('message', 'Mensaje de prueba')
        data = request.data.get('data', {})
        
        resultados = []
        for token in request.user.fcm_tokens:
            resultado = FCMService.enviarNotificacion(token, titulo, mensaje, data)
            resultados.append(resultado)
        
        return Response({
            "success": True,
            "data": {"results": resultados}
        })

class SendNotificationToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        from Users.models import User
        
        try:
            usuario_destino = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"success": False, "errors": ["Usuario no encontrado"]})
        
        if not hasattr(usuario_destino, 'fcm_tokens') or not usuario_destino.fcm_tokens:
            return Response({"success": False, "errors": ["El usuario no tiene tokens registrados"]})
        
        titulo = request.data.get('title', 'Notificación')
        mensaje = request.data.get('message', 'Mensaje del sistema')
        data = request.data.get('data', {})
        
        resultados = []
        for token in usuario_destino.fcm_tokens:
            resultado = FCMService.enviarNotificacion(token, titulo, mensaje, data)
            resultados.append(resultado)
        
        return Response({
            "success": True,
            "data": {"results": resultados}
        })
