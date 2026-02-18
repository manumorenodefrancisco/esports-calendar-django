from django.urls import path
from Events.views.event_view import EventView

#router = DefaultRouter()
#router.register(r'events', EventView, basename='events')

urlpatterns = [path("events/", EventView.as_view())]#router.urls
