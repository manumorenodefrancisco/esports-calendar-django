from rest_framework import permissions
from rest_framework.views import APIView


class EventView(APIView):
    permission_classes = [permissions.IsAuthenticated]