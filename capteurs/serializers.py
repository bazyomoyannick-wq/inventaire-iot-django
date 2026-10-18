from rest_framework import serializers

from .models import Capteur


class CapteurSerializer(serializers.ModelSerializer):
    """Equivalent API du CapteurForm : Capteur <-> JSON + validation."""

    type_libelle = serializers.CharField(source="get_type_capteur_display", read_only=True)

    class Meta:
        model = Capteur
        fields = ["id", "nom", "type_capteur", "type_libelle", "emplacement", "actif", "description"]
        read_only_fields = ["id"]
