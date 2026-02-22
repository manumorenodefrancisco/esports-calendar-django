from django.contrib import admin
from Events.models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'external_id',
        'videogame_name',
        'league_name',
        'scheduled_at',
        'status',
        'winner_id'
    )

    list_filter = (
        'videogame_name',
        'status',
        'match_type',
        'scheduled_at'
    )

    search_fields = (
        'external_id',
        'league_name',
        'tournament_name',
        'serie_full_name'
    )

    ordering = ('-scheduled_at',)

    fieldsets = (
        ('Información General', {
            'fields': ('external_id', 'status', 'scheduled_at', 'videogame_name')
        }),
        ('Detalles de la Competición', {
            'fields': ('league_name', 'tournament_name', 'serie_full_name')
        }),
        ('Datos del Match', {
            'fields': ('match_type', 'number_of_games', 'opponents', 'results', 'winner_id')
        }),
        ('Multimedia', {
            'fields': ('streams',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Esto lo oculta por defecto
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    # Para que los JSONFields se vean un poco más limpios
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        #widgets....
        return form
