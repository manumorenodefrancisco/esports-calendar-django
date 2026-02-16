from django.conf import settings
from django.db import models

class PaisesChoices(models.TextChoices):
    SPAIN = "ES", "ESPAÑA"
    FRANCE = "FR", "FRANCIA"
    GERMANY = "DE", "ALEMANIA"
    UNITED_KINGDOM = "UK", "REINO UNIDO"
    ITALY = "IT", "ITALIA"
    PORTUGAL = "PT", "PORTUGAL"

    USA = "US", "ESTADOS UNIDOS"
    CANADA = "CA", "CANADÁ"
    BRAZIL = "BR", "BRASIL"
    MEXICO = "MX", "MÉXICO"
    ARGENTINA = "AR", "ARGENTINA"

    JAPAN = "JP", "JAPÓN"
    CHINA = "CN", "CHINA"
    AUSTRALIA = "AU", "AUSTRALIA"

class InfoPerfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="info_perfil"
    )
    #email, nombre y demás se mostrara en el perfil accediendo desde este user -> serializers.EmailField(source='user.email')
    #avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Foto de perfil")
    #biografia

    birthday = models.DateField(verbose_name="Fecha de nacimiento", help_text="(Obligatorio)")
    phone = models.CharField(max_length=11, verbose_name="Teléfono", help_text="(Opcional)", null=True, blank=True)

    #city = models.ForeignKey("CiudadModel", on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=3, choices=PaisesChoices.choices, default=PaisesChoices.SPAIN,
                               verbose_name="País", help_text="(Obligatorio)")

    class Meta:
        db_table = "info_perfil"
        verbose_name = "Info perfil"
        verbose_name_plural = "Datos del perfil"
        ordering = ("-country",)

    def __str__(self):
        return f"{self.user.first_name," ", self.user.last_name} ({self.country})"
