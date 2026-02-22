from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils.dateparse import parse_date

from Events.models import Evento
from Events.serializers import EventoSerializer


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query_eventos = Evento.objects.all()

        # FILTROS:
        # por ID interno
        event_id = request.query_params.get('id')
        if event_id:
            try:
                evento = query_eventos.get(id=event_id)
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

        # por external_id
        external_id = request.query_params.get('external_id')
        if external_id:
            query_eventos = query_eventos.filter(external_id=external_id)

        # Búsqueda general
        search = request.query_params.get('search')
        if search:
            query_eventos = query_eventos.filter(
                Q(league_name__icontains=search) |
                Q(tournament_name__icontains=search) |
                Q(serie_full_name__icontains=search) |
                Q(videogame_name__icontains=search)
            )

        # Filtro por videojuego
        videogame = request.query_params.get('videogame')
        if videogame:
            query_eventos = query_eventos.filter(
                videogame_name__icontains=videogame
            )

        # por estado (running, not_started, finished)
        status_param = request.query_params.get('status')
        if status_param:
            query_eventos = query_eventos.filter(status=status_param)

        # por día concreto para calendario
        date = request.query_params.get('date')#YYYY-MM-DD
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                query_eventos = query_eventos.filter(
                    scheduled_at__date=parsed_date
                )

        query_eventos = query_eventos.order_by('scheduled_at')

        if not any([search, videogame, status_param, date, external_id]):
            query_eventos = query_eventos[:50]

        serializer = EventoSerializer(query_eventos, many=True)

        return Response({
            "success": True,
            "data": serializer.data,
            "count": query_eventos.count()
        }, status=status.HTTP_200_OK)
