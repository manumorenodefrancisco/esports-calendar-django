from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from Events.models import Evento
from Events.serializers import EventoSerializer


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Obtener lista de eventos con filtros opcionales.
        
        Filtros disponibles (query params):
        - search: buscar por nombre de evento               ej -> /api/events/?search=championship
        - videojuego: filtrar por videojuego específico     ej -> /api/events/?videojuego=League%20of%20Legends
        - tipo_evento: filtrar por tipo de evento           ej -> /api/events/?tipo_evento=Tournament
        - id: obtener un evento específico por ID           ej -> /api/events/?id=123
        """
        queryset = Evento.objects.all()
        
        # Filtro por ID específico
        event_id = request.query_params.get('id')
        if event_id:
            try:
                evento = queryset.get(id=event_id)
                serializer = EventoSerializer(evento)
                return Response({
                    "success": True,
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Evento.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Evento no encontrado"
                }, status=status.HTTP_404_NOT_FOUND)
        
        # Filtros:
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        
        videojuego = request.query_params.get('videojuego')
        if videojuego:
            queryset = queryset.filter(videojuego__icontains=videojuego)
        
        tipo_evento = request.query_params.get('tipo_evento')
        if tipo_evento:
            queryset = queryset.filter(tipo_evento__icontains=tipo_evento)
        
        # Ordenar fecha más recientes primero
        queryset = queryset.order_by('-fecha_inicio')
        
        if not any([search, videojuego, tipo_evento]):
            queryset = queryset[:50]  # Máximo 50 eventos si no hay filtros
        
        serializer = EventoSerializer(queryset, many=True)
        
        return Response({
            "success": True,
            "data": serializer.data,
            "count": len(serializer.data)
        }, status=status.HTTP_200_OK)
