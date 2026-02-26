from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Subscriptions.models import Suscripcion
from Preferences.models import Preferencia
from Preferences.serializers import PreferenciaSerializer


class PreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        preferencias = Preferencia.objects.filter(usuario=request.user)
        serializer = PreferenciaSerializer(preferencias, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request): # genera automaticamente preferencias tras analizar las suscripciones
        user = request.user
        suscripciones = Suscripcion.objects.filter(usuario=user).select_related('evento') #-> por cada suscripción, traer su Evento entero
        
        if not suscripciones.exists():
            return Response({"success": False, "errors": ["No hay suscripciones para analizar con tu user así que no se pueden crear preferencias :)"]}, status=status.HTTP_400_BAD_REQUEST)
        
        Preferencia.objects.filter(usuario=user).delete()
        
        # contadores
        videojuegos_cont = {}
        jugadores_cont = {}
        ligas_cont = {}
        torneos_cont = {}
        
        total_suscripciones = suscripciones.count()
        
        for suscripcion in suscripciones:
            #CONTADORES
            evento = suscripcion.evento

            if evento.videogame_name:
                if evento.videogame_name in videojuegos_cont:
                    videojuegos_cont[evento.videogame_name] += 1
                else:
                    videojuegos_cont[evento.videogame_name] = 1
            
            if evento.opponents:
                for opponent in evento.opponents:
                    if isinstance(opponent, dict) and opponent.get('name'):
                        nombre_jugador = opponent['name']
                        if nombre_jugador in jugadores_cont:
                            jugadores_cont[nombre_jugador] += 1
                        else:
                            jugadores_cont[nombre_jugador] = 1
            
            if evento.league_name:
                if evento.league_name in ligas_cont:
                    ligas_cont[evento.league_name] += 1
                else:
                    ligas_cont[evento.league_name] = 1
            
            if evento.tournament_name:
                if evento.tournament_name in torneos_cont:
                    torneos_cont[evento.tournament_name] += 1
                else:
                    torneos_cont[evento.tournament_name] = 1
        
        # Generar preferencias basadas en frecuencia y porcentaje
        preferencias_creadas = []
        
        for videojuego, count in videojuegos_cont.items():
            porcentaje = (count / total_suscripciones) * 100
            puntaje = self._calcular_puntaje_videojuego(porcentaje, count)
            
            if puntaje > 0:
                preferencia = Preferencia.objects.create(
                    usuario=user,
                    tipo_preferencia='videojuego',
                    valor=videojuego,
                    puntaje_interes=puntaje,
                    frecuencia=count,
                    total_suscripciones_usuario=total_suscripciones
                )
                preferencias_creadas.append(preferencia)
        
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


