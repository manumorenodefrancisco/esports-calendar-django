from django.urls import path
from Events.views.event_view import EventView
from Events.views.sync_view import SyncView

urlpatterns = [
    path("events/", EventView.as_view()),
    path("events/sync/", SyncView.as_view())
]
