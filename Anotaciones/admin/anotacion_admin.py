from django.contrib import admin
from Anotaciones.models import Anotacion

@admin.register(Anotacion)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'titulo', 'descripcion', 'fecha_hora', 'created_at')