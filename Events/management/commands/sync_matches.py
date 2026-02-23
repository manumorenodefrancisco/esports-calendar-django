from django.core.management.base import BaseCommand
from Events.views import EventView

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        view = EventView()
        view.sync_pandascore()
