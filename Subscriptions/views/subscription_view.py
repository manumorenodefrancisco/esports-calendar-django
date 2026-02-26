from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Events.models.event_model import Evento
from Subscriptions.models.subscription_model import Suscripcion
from Subscriptions.serializers.subscription_serializer import SuscripcionSerializer


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Suscripcion.objects.filter(usuario=request.user)
        serializer = SuscripcionSerializer(subscriptions, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        evento_id = request.data.get('evento_id')
        
        if not evento_id:
            return Response({"success": False, "errors": ["El campo evento_id es obligatorio"]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist: #!exists()
            return Response({"success": False, "errors": ["El evento no existe"]}, status=status.HTTP_400_BAD_REQUEST)

        existing_subscription = Suscripcion.objects.filter(usuario=request.user, evento=evento).first()

        if existing_subscription:
            return Response({"success": False, "errors": ["Ya estás suscrito a este evento"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SuscripcionSerializer(data=request.data, context={'user': request.user})
        
        if serializer.is_valid():
            subscription = serializer.save()
            return Response({"success": True, "data": SuscripcionSerializer(subscription).data}, status=status.HTTP_200_OK)
        else:
            errores = []
            for error in serializer.errors.values():
                for e in error:
                    errores.append(e)
            return Response({"success": False, "errors": errores}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, evento_id):
        # Verificar que existe
        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return Response({"success": False, "errors": ["El evento no existe"]}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = Suscripcion.objects.get(usuario=request.user, evento=evento)
            subscription.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)

        except Suscripcion.DoesNotExist:
            return Response({"success": False, "errors": ["No estás suscrito a este evento"]}, status=status.HTTP_400_BAD_REQUEST)
