from rest_framework import viewsets

from .models import Capteur
from .serializers import CapteurSerializer


class CapteurViewSet(viewsets.ModelViewSet):
    """API REST : liste, detail, creation, modification, suppression."""

    serializer_class = CapteurSerializer

    def get_queryset(self):
        capteurs = Capteur.objects.order_by("nom")
        q = self.request.query_params.get("q", "").strip()
        if q:
            capteurs = capteurs.filter(nom__icontains=q)
        if self.request.query_params.get("actifs_seulement") in ("1", "true", "on"):
            capteurs = capteurs.filter(actif=True)
        return capteurs
