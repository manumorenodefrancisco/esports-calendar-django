import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from decouple import config
import os

class FCMService:
    def __init__(self):
        # Inicializar Firebase Admin SDK si no está inicializado
        if not firebase_admin._apps:
            cred_path = config('FIREBASE_CREDENTIALS_PATH', default='serviceAccountKey.json')
            full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), cred_path)

            try:
                cred = credentials.Certificate(full_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Error inicializando Firebase: {e}")

    def enviarNotificacion(self, token, titulo, mensaje, data=None):
        #Envía notificación push usando Firebase Admin SDK V1
        """
                Args:
                    token (str): Token FCM del dispositivo
                    titulo (str): Título de la notificación
                    mensaje (str): Contenido de la notificación
                    data (dict): Datos adicionales (opcional)
                Returns:
                    dict: Respuesta de FCM
                """
        try:
            # Crear el mensaje
            message = messaging.Message(
                notification=messaging.Notification(
                    title=titulo,
                    body=mensaje,
                ),
                token=token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default'
                    )
                )
            )

            # Añadir datos adicionales si existen
            if data:
                message.data = data

            # Enviar el mensaje
            result = messaging.send(message)

            return {
                'success': True,
                'message_id': result
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def enviarNotificacionMultiple(self, tokens, titulo, mensaje, data=None):
        #Arg tokens (list): Lista de tokens FCM en lugar de Token FCM del dispositivo

        try:
            # Crear mensaje multicast
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=titulo,
                    body=mensaje,
                ),
                tokens=tokens,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default'
                    )
                )
            )

            # Añadir datos adicionales si existen
            if data:
                message.data = data

            # Enviar el mensaje
            result = messaging.send_multicast(message)

            return {
                'success': True,
                'success_count': result.success_count,
                'failure_count': result.failure_count,
                'responses': result.responses
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Instancia global
fcm_service = FCMService()
