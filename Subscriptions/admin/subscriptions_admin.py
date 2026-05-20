from Subscriptions.models import Suscripcion
from django.contrib import admin

@admin.register(Suscripcion)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('usuario__username', 'created_at')# 'evento__match_name',
    list_filter = ('recordatorio_1_hora', 'recordatorio_5_minutos')
    search_fields = ('usuario__username', 'evento__match_name', 'evento__videogame_name')
    ordering = ('created_at',)