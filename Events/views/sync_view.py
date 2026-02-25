from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .event_view import EventView


class SyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            event_view = EventView()
            event_view.sync_pandascore()
            return Response({"success": True, "message": "Sincronización completada"})
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
