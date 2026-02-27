import requests
import json
from decouple import config

class FCMService:
    def __init__(self):
        self.server_key = config('FCM_SERVER_KEY', '')
        self.fcm_url = 'https://fcm.googleapis.com/fcm/send'
        
    def enviarNotificacion(self, token, titulo, mensaje, data=None):
        """
        Envía notificación push a un dispositivo específico
        
        Args:
            token (str): Token FCM del dispositivo
            titulo (str): Título de la notificación
            mensaje (str): Contenido de la notificación
            data (dict): Datos adicionales (opcional)
        
        Returns:
            dict: Respuesta de FCM
        """
        if not self.server_key:
            return {'error': 'FCM_SERVER_KEY no configurado'}
            
        headers = {
            'Authorization': f'key={self.server_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'to': token,
            'notification': {
                'title': titulo,
                'body': mensaje,
                'sound': 'default'
            },
            'priority': 'high'
        }
        
        if data:
            payload['data'] = data
            
        try:
            response = requests.post(
                self.fcm_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'error': f'Error {response.status_code}',
                    'message': response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {'error': f'Error de conexión: {str(e)}'}
    
    def enviarNotificacionMultiple(self, tokens, titulo, mensaje, data=None):
        """
        Envía notificación a múltiples dispositivos
        
        Args:
            tokens (list): Lista de tokens FCM
            titulo (str): Título de la notificación
            mensaje (str): Contenido de la notificación
            data (dict): Datos adicionales (opcional)
        """
        if not self.server_key:
            return {'error': 'FCM_SERVER_KEY no configurado'}
            
        headers = {
            'Authorization': f'key={self.server_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'registration_ids': tokens,
            'notification': {
                'title': titulo,
                'body': mensaje,
                'sound': 'default'
            },
            'priority': 'high'
        }
        
        if data:
            payload['data'] = data
            
        try:
            response = requests.post(
                self.fcm_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'error': f'Error {response.status_code}',
                    'message': response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {'error': f'Error de conexión: {str(e)}'}

# Instancia global
fcm_service = FCMService()
