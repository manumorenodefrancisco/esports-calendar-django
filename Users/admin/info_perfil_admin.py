from Users.models import InfoPerfil
from django.contrib import admin

@admin.register(InfoPerfil)
class InfoPerfilAdmin(admin.ModelAdmin):
    list_display = ('user__name', 'user__email', 'user__username', 'birthdate', 'phone', 'country')
    list_filter = ('country',)
    search_fields = ('user__name','country__name')
    ordering = ('-country',)