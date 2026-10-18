from django.db import models
from django.core.validators import MinLengthValidator


class Capteur(models.Model):
    class Type(models.TextChoices):
        TEMPERATURE = "T", "Température"
        HUMIDITE = "H", "Humidité"
        PRESSION = "P", "Pression"
        LUMIERE = "L", "Luminosité"
        CO2 = "C", "CO₂"
        MOUVEMENT = "M", "Mouvement"
        SON = "S", "Niveau sonore"

    nom = models.CharField(
        max_length=40, unique=True,
        validators=[MinLengthValidator(3)],
    )
    type_capteur = models.CharField(max_length=1, choices=Type.choices)
    emplacement = models.CharField(max_length=60)
    actif = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom