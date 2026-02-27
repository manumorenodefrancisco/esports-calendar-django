from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import fcm_service

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_token(request):
    """
    Registra el token FCM del usuario (en memoria temporal)
    """
    token = request.data.get('token')
    
    if not token:
        return Response({'error': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Guardar token en sesión del usuario (temporal)
    if not hasattr(request.user, 'fcm_tokens'):
        request.user.fcm_tokens = []
    
    if token not in request.user.fcm_tokens:
        request.user.fcm_tokens.append(token)
    
    return Response({
        'message': 'Token registrado correctamente',
        'tokens_count': len(request.user.fcm_tokens)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_notificacion(request):
    """
    Envía notificación al usuario actual
    """
    if not hasattr(request.user, 'fcm_tokens') or not request.user.fcm_tokens:
        return Response({'error': 'No tienes tokens registrados'}, status=status.HTTP_400_BAD_REQUEST)
    
    titulo = request.data.get('title', 'Notificación')
    mensaje = request.data.get('message', 'Mensaje de prueba')
    data = request.data.get('data', {})
    
    # Enviar a todos los tokens del usuario
    resultados = []
    for token in request.user.fcm_tokens:
        resultado = fcm_service.enviarNotificacion(token, titulo, mensaje, data)
        resultados.append(resultado)
    
    return Response({
        'message': 'Notificaciones enviadas',
        'results': resultados
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_notificacion_a_usuario(request, user_id):
    """
    Envía notificación a un usuario específico (para admin)
    """
    from Users.models import User
    
    try:
        usuario_destino = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    if not hasattr(usuario_destino, 'fcm_tokens') or not usuario_destino.fcm_tokens:
        return Response({'error': 'El usuario no tiene tokens registrados'}, status=status.HTTP_400_BAD_REQUEST)
    
    titulo = request.data.get('title', 'Notificación')
    mensaje = request.data.get('message', 'Mensaje del sistema')
    data = request.data.get('data', {})
    
    # Enviar a todos los tokens del usuario destino
    resultados = []
    for token in usuario_destino.fcm_tokens:
        resultado = fcm_service.enviarNotificacion(token, titulo, mensaje, data)
        resultados.append(resultado)
    
    return Response({
        'message': f'Notificaciones enviadas a {usuario_destino.username}',
        'results': resultados
    })
