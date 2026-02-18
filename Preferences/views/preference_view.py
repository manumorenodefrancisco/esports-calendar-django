from rest_framework import permissions
from rest_framework.views import APIView


class PreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]