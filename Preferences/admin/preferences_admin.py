from Preferences.models import Preferencia
from django.contrib import admin

@admin.register(Preferencia)
class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_preferencia', 'valor', 'puntaje_interes', 'frecuencia', 'ultima_actualizacion')
    list_filter = ('tipo_preferencia', 'usuario')
    search_fields = ('valor', 'usuario__username')
    ordering = ('-puntaje_interes', '-frecuencia')
    readonly_fields = ('created_at', 'ultima_actualizacion')
