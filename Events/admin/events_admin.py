from Events.models import Evento
from django.contrib import admin

@admin.register(Evento)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('external_id','nombre', 'videojuego', 'tipo_evento', 'fecha_inicio', 'fecha_fin', 'color', 'created_at')
    list_filter = ('nombre', 'videojuego', 'tipo_evento','fecha_inicio','created_at',)
    #list_display = [field.name for field in Evento._meta.get_fields() if not field.many_to_many]
    search_fields = ('nombre', 'videojuego')
    ordering = ('fecha_inicio',)