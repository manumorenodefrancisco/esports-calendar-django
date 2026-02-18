from rest_framework import viewsets, permissions
from rest_framework.views import APIView


#class SubscriptionView(viewsets.ModelViewSet):
class SubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]