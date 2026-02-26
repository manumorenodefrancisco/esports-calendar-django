from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
        eventos_no_suscritos = Evento.objects.exclude(suscripcion__usuario=user)

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
                    'evento_id': evento.id,
                    'match_name': evento.match_name,
                    'videogame_name': evento.videogame_name,
                    'league_name': evento.league_name,
                    'scheduled_at': evento.scheduled_at,
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

        return puntaje
