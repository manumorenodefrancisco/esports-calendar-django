from Preferences.models import Preferencia
from django.contrib import admin

@admin.register(Preferencia)
class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('usuario__username', 'videojuego', 'tipo_evento', 'puntaje_interes', 'total_suscripciones', 'ultima_actualizacion')
    list_filter = ('videojuego', 'tipo_evento', 'puntaje_interes')
    search_fields = ('usuario__username', 'videojuego', 'puntaje_interes')
    ordering = ('created_at',)