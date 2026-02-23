import requests
from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.db.models import Q
from django.utils.dateparse import parse_date

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from Events.models import Evento
from Events.serializers import EventoSerializer


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    PANDASCORE_BASE = "https://api.pandascore.co"
    TOKEN = settings.PANDASCORE_TOKEN

    def get(self, request):

        self.sync_pandascore()

        query_eventos = Evento.objects.all()

        # FILTROS
        # por ID interno
        event_id = request.query_params.get('id')
        if event_id:
            try:
                evento = query_eventos.get(id=event_id)
                serializer = EventoSerializer(evento)
                return Response({"success": True, "data": serializer.data})
            except Evento.DoesNotExist:
                return Response({"success": False, "message": "Evento no encontrado"},
                                status=status.HTTP_404_NOT_FOUND)

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
        date = request.query_params.get('date')
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                query_eventos = query_eventos.filter(
                    scheduled_at__date=parsed_date
                )

        query_eventos = query_eventos.order_by('scheduled_at')[:100]

        serializer = EventoSerializer(query_eventos, many=True)

        return Response({
            "success": True,
            "data": serializer.data,
            "count": query_eventos.count()
        })

    def sync_pandascore(self):

        #limpiar matches viejos
        now = timezone.now()
        one_hour_ago = now - timedelta(minutes=60)
        Evento.objects.filter(
            status="finished",
            end_at__lt=one_hour_ago
        ).delete()

        headers = {
            "Authorization": f"Bearer {self.TOKEN}"
        }

        # RUNNING + UPCOMING
        url_matches = f"{self.PANDASCORE_BASE}/matches?filter[status]=running,not_started&sort=begin_at"
        response = requests.get(url_matches, headers=headers)
        if response.status_code == 200:
            matches = response.json()
            for match in matches:
                self.save_or_update_match(match)

        # PAST última hora
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(minutes=60)

        url_range = f"{self.PANDASCORE_BASE}/matches/past?range[end_at]={one_hour_ago.isoformat()}Z,{now.isoformat()}Z"
        response_past = requests.get(url_range, headers=headers)

        if response_past.status_code == 200:
            past_matches = response_past.json()
            for match in past_matches:
                self.save_or_update_match(match)

        # INCIDENTS
        incidents_url = f"{self.PANDASCORE_BASE}/incidents"
        response_incidents = requests.get(incidents_url, headers=headers)

        if response_incidents.status_code == 200:
            incidents = response_incidents.json()
            for incident in incidents:
                object_id = incident.get("object_id")
                type_ = incident.get("type")

                if type_ in ["add", "update"]:
                    self.traer_match_por_id(object_id)

                elif type_ == "delete":
                    Evento.objects.filter(external_id=object_id).delete()


    def traer_match_por_id(self, match_id):
        headers = {
            "Authorization": f"Bearer {self.TOKEN}"
        }

        url = f"{self.PANDASCORE_BASE}/matches/{match_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            match = response.json()
            self.save_or_update_match(match)

    def save_or_update_match(self, match):

        opponents = []
        for opp in match.get("opponents", []): #(clave, default value)
            opponent = opp.get("opponent")
            if opponent:
                opponents.append({
                    "id": opponent.get("id"),
                    "name": opponent.get("name"),
                    "image_url": opponent.get("image_url"),
                })

        streams = []
        for stream in match.get("streams_list", [])[:5]:
            streams.append(stream.get("raw_url"))

        Evento.objects.update_or_create(
            external_id=match.get("id"),
            defaults={
                "scheduled_at": match.get("scheduled_at"),
                "videogame_name": match.get("videogame", {}).get("name"),
                "league_name": match.get("league", {}).get("name"),
                "tournament_name": match.get("tournament", {}).get("name"),
                "serie_full_name": match.get("serie", {}).get("full_name"),
                "opponents": opponents,
                "match_type": match.get("match_type"),
                "number_of_games": match.get("number_of_games"),
                "status": match.get("status"),
                "results": match.get("results", []),
                "winner_id": match.get("winner_id"),
                "streams": streams,
                "end_at": match.get("end_at")
            }
        )