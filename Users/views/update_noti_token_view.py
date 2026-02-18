from django.views.generic import UpdateView
from rest_framework import permissions


class UpdateNotiTokenView(UpdateView):
    permission_classes = [permissions.IsAuthenticated]