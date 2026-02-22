from rest_framework import serializers
from Events.models import Evento


class EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evento
        fields = [
            "id",
            "external_id",
            "scheduled_at",
            "videogame_name",
            "league_name",
            "tournament_name",
            "serie_full_name",
            "opponents",
            "match_type",
            "number_of_games",
            "status",
            "results",
            "winner_id",
            "streams",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
