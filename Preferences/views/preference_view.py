from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Events.models.event_model import Evento
from Subscriptions.models.subscription_model import Suscripcion
from Preferences.models.preference_model import Preferencia
from Preferences.serializers.preference_serializer import PreferenciaSerializer


class PreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtener preferencias del usuario"""
        preferencias = Preferencia.objects.filter(usuario=request.user)
        serializer = PreferenciaSerializer(preferencias, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Analizar suscripciones y generar/actualizar preferencias"""
        user = request.user
        suscripciones = Suscripcion.objects.filter(usuario=user).select_related('evento')
        
        if not suscripciones.exists():
            return Response({"success": False, "errors": ["No hay suscripciones para analizar con tu user así que no se pueden crear preferencias :)"]}, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminar preferencias anteriores para recalcular
        Preferencia.objects.filter(usuario=user).delete()
        
        # Inicializar contadores
        videojuegos_cont = {}
        jugadores_cont = {}
        ligas_cont = {}
        torneos_cont = {}
        
        total_suscripciones = suscripciones.count()
        
        # Analizar cada suscripción
        for suscripcion in suscripciones:
            evento = suscripcion.evento
            
            # Contar videojuegos
            if evento.videogame_name:
                if evento.videogame_name in videojuegos_cont:
                    videojuegos_cont[evento.videogame_name] += 1
                else:
                    videojuegos_cont[evento.videogame_name] = 1
            
            # Contar jugadores/equipos
            if evento.opponents:
                for opponent in evento.opponents:
                    if isinstance(opponent, dict) and opponent.get('name'):
                        nombre_jugador = opponent['name']
                        if nombre_jugador in jugadores_cont:
                            jugadores_cont[nombre_jugador] += 1
                        else:
                            jugadores_cont[nombre_jugador] = 1
            
            # Contar ligas
            if evento.league_name:
                if evento.league_name in ligas_cont:
                    ligas_cont[evento.league_name] += 1
                else:
                    ligas_cont[evento.league_name] = 1
            
            # Contar torneos
            if evento.tournament_name:
                if evento.tournament_name in torneos_cont:
                    torneos_cont[evento.tournament_name] += 1
                else:
                    torneos_cont[evento.tournament_name] = 1
        
        # Generar preferencias basadas en frecuencia y porcentaje
        preferencias_creadas = []
        
        # Preferencias de videojuegos (prioridad alta)
        for videojuego, count in videojuegos_cont.items():
            porcentaje = (count / total_suscripciones) * 100
            puntaje = self._calcular_puntaje_videojuego(porcentaje, count)
            
            if puntaje > 0:  # Solo guardar si hay interés mínimo
                preferencia = Preferencia.objects.create(
                    usuario=user,
                    tipo_preferencia='videojuego',
                    valor=videojuego,
                    puntaje_interes=puntaje,
                    frecuencia=count,
                    total_suscripciones_usuario=total_suscripciones
                )
                preferencias_creadas.append(preferencia)
        
        # Preferencias de jugadores/equipos (prioridad media)
        for jugador, count in jugadores_cont.items():
            if count >= 2:  # Aparece en al menos 2 suscripciones
                puntaje = self._calcular_puntaje_jugador(count, total_suscripciones)
                
                preferencia = Preferencia.objects.create(
                    usuario=user,
                    tipo_preferencia='jugador',
                    valor=jugador,
                    puntaje_interes=puntaje,
                    frecuencia=count,
                    total_suscripciones_usuario=total_suscripciones
                )
                preferencias_creadas.append(preferencia)
        
        # Preferencias de ligas (prioridad baja)
        for liga, count in ligas_cont.items():
            if count >= 3:  # Aparece en al menos 3 suscripciones
                puntaje = self._calcular_puntaje_liga(count, total_suscripciones)
                
                preferencia = Preferencia.objects.create(
                    usuario=user,
                    tipo_preferencia='liga',
                    valor=liga,
                    puntaje_interes=puntaje,
                    frecuencia=count,
                    total_suscripciones_usuario=total_suscripciones
                )
                preferencias_creadas.append(preferencia)
        
        # Serializar y devolver resultados
        serializer = PreferenciaSerializer(preferencias_creadas, many=True)
        return Response({
            "success": True, 
            "data": serializer.data,
            "message": f"Se analizaron {total_suscripciones} suscripciones y se generaron {len(preferencias_creadas)} preferencias"
        }, status=status.HTTP_200_OK)
    
    def _calcular_puntaje_videojuego(self, porcentaje, frecuencia):
        if porcentaje >= 60:
            return 10.0
        elif porcentaje >= 40:
            return 7.5
        elif porcentaje >= 25:
            return 5.0
        elif porcentaje >= 15:
            return 2.5
        else:
            return 0.0
    
    def _calcular_puntaje_jugador(self, frecuencia, total_suscripciones):
        if frecuencia >= 5:
            return 8.0
        elif frecuencia >= 3:
            return 6.0
        elif frecuencia == 2:
            return 4.0
        else:
            return 0.0
    
    def _calcular_puntaje_liga(self, frecuencia, total_suscripciones):
        porcentaje = (frecuencia / total_suscripciones) * 100
        
        if porcentaje >= 50:
            return 6.0
        elif porcentaje >= 30:
            return 4.0
        elif porcentaje >= 20:
            return 2.0
        else:
            return 0.0


class RecommendedEventsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener eventos recomendados basados en preferencias"""
        user = request.user
        
        # Obtener preferencias del usuario ordenadas por puntaje
        preferencias = Preferencia.objects.filter(usuario=user).order_by('-puntaje_interes')
        
        if not preferencias.exists():
            return Response({"success": False, "errors": ["No hay preferencias para generar recomendaciones"]}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener IDs de eventos ya suscritos
        eventos_suscritos_ids = []
        suscripciones_usuario = Suscripcion.objects.filter(usuario=user)
        for suscripcion in suscripciones_usuario:
            eventos_suscritos_ids.append(suscripcion.evento.id)
        
        # Obtener eventos no suscritos
        eventos_no_suscritos = Evento.objects.exclude(id__in=eventos_suscritos_ids)
        #id__in -> nombre del campo = id, filtro o relación a aplicar = in

        # Calcular puntaje de recomendación para cada evento
        eventos_recomendados = []
        
        for evento in eventos_no_suscritos:
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
        
        # Ordenar por puntaje de recomendación (método simple)
        for i in range(len(eventos_recomendados)):
            for j in range(i + 1, len(eventos_recomendados)):
                if eventos_recomendados[j]['puntaje_recomendacion'] > eventos_recomendados[i]['puntaje_recomendacion']:
                    eventos_recomendados[i], eventos_recomendados[j] = eventos_recomendados[j], eventos_recomendados[i]
        
        return Response({
            "success": True,
            "data": eventos_recomendados[:20],  # Limitar a 20 recomendaciones
            "message": f"Se encontraron {len(eventos_recomendados)} eventos recomendados"
        }, status=status.HTTP_200_OK)
    
    def _calcular_puntaje_recomendacion(self, evento, preferencia):
        """Calcular puntaje de recomendación para un evento basado en una preferencia"""
        puntaje = 0
        
        if preferencia.tipo_preferencia == 'videojuego' and evento.videogame_name == preferencia.valor:
            puntaje = preferencia.puntaje_interes * 0.5  # 50% del peso
        
        elif preferencia.tipo_preferencia == 'jugador' and evento.opponents:
            for opponent in evento.opponents:
                if isinstance(opponent, dict) and opponent.get('name') == preferencia.valor:
                    puntaje = preferencia.puntaje_interes * 0.3  # 30% del peso
                    break
        
        elif preferencia.tipo_preferencia == 'liga' and evento.league_name == preferencia.valor:
            puntaje = preferencia.puntaje_interes * 0.2  # 20% del peso
        
        return puntaje
