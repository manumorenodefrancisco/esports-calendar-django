from django.urls import path
from rest_framework.routers import DefaultRouter
from Preferences.views.preference_view import PreferenceView

urlpatterns = [path("preferences/", PreferenceView.as_view())]
