from rest_framework import viewsets

from .models import Capteur
from .serializers import CapteurSerializer


# API REST en lecture seule (GET uniquement) :
#   GET /api/capteurs/        -> liste
#   GET /api/capteurs/<pk>/   -> détail
# POST, PUT, PATCH et DELETE sont refusés (405).
# Filtres : ?q=Serre et ?actifs_seulement=1
class CapteurViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CapteurSerializer

    def get_queryset(self):
        capteurs = Capteur.objects.order_by("nom")
        q = self.request.query_params.get("q", "").strip()
        if q:
            capteurs = capteurs.filter(nom__icontains=q)
        if self.request.query_params.get("actifs_seulement") in ("1", "true", "on"):
            capteurs = capteurs.filter(actif=True)
        return capteurs