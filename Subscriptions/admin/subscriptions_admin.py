from Subscriptions.models import Suscripcion
from django.contrib import admin

@admin.register(Suscripcion)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('usuario__name', 'evento__nombre', 'created_at')
    list_filter = ('recordatorio_1_dia', 'recordatorio_1_hora')
    search_fields = ('usuario__name', 'evento__nombre', 'evento__videojuego')
    ordering = ('created_at',)