from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone

from Events.models.event_model import Evento
from Subscriptions.models import Suscripcion
from Preferences.models import Preferencia


class RecommendedEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        preferencias = Preferencia.objects.filter(usuario=user).order_by('-puntaje_interes')

        if not preferencias.exists():
            return Response({"success": False, "errors": ["No hay preferencias para generar recomendaciones"]},status=status.HTTP_400_BAD_REQUEST)

                # exclude = WHERE NOT, lo contrario a filter()
        eventos_no_suscritos = Evento.objects.exclude(
            suscripcion__usuario=user
        ).filter(
            scheduled_at__gte=timezone.now()
        )#eventos solo futuros

        eventos_recomendados = []
        for evento in eventos_no_suscritos:
            # para cada evento no suscrito del usuario (la gran mayoría), buscar posibles coincidencias
                        # con alguna preferencia del usuario
            puntaje_total = 0
            for preferencia in preferencias:
                puntaje = self._calcular_puntaje_recomendacion(evento, preferencia)
                puntaje_total += puntaje

            if puntaje_total > 0:
                evento_data = {
                    'id': evento.id,
                    'external_id': evento.external_id,
                    'scheduled_at': evento.scheduled_at,
                    'match_name': evento.match_name,
                    'league_name': evento.league_name,
                    'tournament_name': evento.tournament_name,
                    'serie_full_name': evento.serie_full_name,
                    'videogame_name': evento.videogame_name,
                    'opponents': evento.opponents,  # IMPORTANTE: nombres de equipos/jugadores
                    'match_type': evento.match_type,
                    'number_of_games': evento.number_of_games,
                    'status': evento.status,  # IMPORTANTE: estado del partido
                    'results': evento.results,
                    'winner_id': evento.winner_id,
                    'streams': evento.streams,
                    'end_at': evento.end_at,
                    'created_at': evento.created_at,
                    'updated_at': evento.updated_at,
                    'puntaje_recomendacion': puntaje_total
                }
                eventos_recomendados.append(evento_data)

        # Ordenar por puntaje de recomendación (esto es complejo pero ahorra hacer matrices bidimensionales)
        eventos_recomendados.sort(key=lambda x: x['puntaje_recomendacion'], reverse=True)

        return Response({
            "success": True,
            "data": eventos_recomendados[:20],  # Limitar a 20
        }, status=status.HTTP_200_OK)

    def _calcular_puntaje_recomendacion(self, evento, preferencia):

        puntaje = 0

        if preferencia.tipo_preferencia == 'videojuego' and evento.videogame_name == preferencia.valor:
            puntaje = preferencia.puntaje_interes * 0.5  # 50% del peso

        elif preferencia.tipo_preferencia == 'jugador' and evento.opponents:
            for opponent in evento.opponents:
                if isinstance(opponent, dict) and opponent.get('name') == preferencia.valor:
                    puntaje = preferencia.puntaje_interes * 0.3  # 30%
                    break

        elif preferencia.tipo_preferencia == 'liga' and evento.league_name == preferencia.valor:
            puntaje = preferencia.puntaje_interes * 0.2

        elif preferencia.tipo_preferencia == 'torneo' and evento.tournament_name == preferencia.valor:
            puntaje = preferencia.puntaje_interes * 0.2

        return puntaje
