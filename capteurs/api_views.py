from rest_framework import viewsets

from .models import Capteur
from .serializers import CapteurSerializer


class CapteurViewSet(viewsets.ReadOnlyModelViewSet):
    """API REST en lecture seule (GET uniquement).

      GET /api/capteurs/        -> list      (équivalent de capteur_liste)
      GET /api/capteurs/<pk>/   -> retrieve  (équivalent de capteur_detail)

    POST, PUT, PATCH et DELETE ne sont pas fournis : DRF répond 405.

    Filtres facultatifs, mêmes règles que le formulaire de recherche :
      ?q=Serre            nom contient « Serre »
      ?actifs_seulement=1 seulement les capteurs actifs
    """

    serializer_class = CapteurSerializer

    def get_queryset(self):
        capteurs = Capteur.objects.order_by("nom")
        q = self.request.query_params.get("q", "").strip()
        if q:
            capteurs = capteurs.filter(nom__icontains=q)
        if self.request.query_params.get("actifs_seulement") in ("1", "true", "on"):
            capteurs = capteurs.filter(actif=True)
        return capteurs