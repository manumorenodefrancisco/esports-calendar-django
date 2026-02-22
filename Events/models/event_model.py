from django.db import models

class Evento(models.Model):
    class Evento(models.Model):
        external_id = models.IntegerField(unique=True)

        scheduled_at = models.DateTimeField()

        videogame_name = models.CharField(max_length=100)

        league_name = models.CharField(max_length=150)
        tournament_name = models.CharField(max_length=150)
        serie_full_name = models.CharField(max_length=150, null=True, blank=True)

        opponents = models.JSONField(default=list, blank=True)
            #jsonfield guarda todoel json: [{ "id": 126536, "name": "KOI", "image_url": "..." },{ "id": 394, "name": "Fnatic", "image_url": "..." }]
        match_type = models.CharField(max_length=50, null=True, blank=True)
        number_of_games = models.IntegerField(null=True, blank=True)
        status = models.CharField(max_length=50)

        results = models.JSONField(default=list, blank=True)
        winner_id = models.IntegerField(null=True, blank=True)

        streams = models.JSONField(default=list, blank=True)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.videojuego}"
