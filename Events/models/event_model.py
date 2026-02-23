from django.db import models

class Evento(models.Model):
    external_id = models.IntegerField(unique=True)
    scheduled_at = models.DateTimeField()
    match_name = models.CharField(max_length=100)

    league_name = models.CharField(max_length=150)
    tournament_name = models.CharField(max_length=150)
    serie_full_name = models.CharField(max_length=150, null=True, blank=True)

    videogame_name = models.CharField(max_length=100)
    opponents = models.JSONField(default=list, blank=True)
        #jsonfield guarda todoel json: [{ "id": 126536, "name": "KOI", "image_url": "..." },{ "id": 394, "name": "Fnatic", "image_url": "..." }]
    match_type = models.CharField(max_length=50, null=True, blank=True)#match type...
    number_of_games = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)

    results = models.JSONField(default=list, blank=True)#"results": [{ "score": 1,"team_id": 394},{"scor......} ]
    winner_id = models.IntegerField(null=True, blank=True)

    streams = models.JSONField(default=list, blank=True)#"streams_list": [{"official": true,"raw_url": "htt...ww.twitch.tv/lec"}{"offici......} ]

    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.match_name} - {self.videogame_name}"