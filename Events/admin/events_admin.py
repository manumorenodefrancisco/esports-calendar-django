from django.contrib import admin
from Events.models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'videogame_name', 'league_name', 'scheduled_at', 'status', 'winner_id')
    list_filter = ('videogame_name', 'status', 'match_type', 'scheduled_at')
    search_fields = ('external_id', 'league_name', 'tournament_name', 'serie_full_name')
    ordering = ('-scheduled_at',)
