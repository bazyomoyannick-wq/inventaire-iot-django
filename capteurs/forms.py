from django import forms

from .models import Capteur


class RechercheCapteurForm(forms.Form):
    """Formulaire de recherche (forms.Form) : il ne crée ni ne modifie aucun objet."""

    q = forms.CharField(
        label="Nom contient",
        max_length=40,
        required=False,
    )
    actifs_seulement = forms.BooleanField(
        label="Actifs seulement",
        required=False,
    )


class CapteurForm(forms.ModelForm):
    """Formulaire lié au modèle : sert à la création et à la modification."""

    class Meta:
        model = Capteur
        fields = ["nom", "type_capteur", "emplacement", "actif", "description"]
        labels = {
            "nom": "Nom",
            "type_capteur": "Type",
            "emplacement": "Emplacement",
            "actif": "Actif",
            "description": "Description",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
