"""Tests de l'API REST en lecture seule (GET uniquement)."""
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Capteur


class CapteurApiLectureTests(APITestCase):
    fixtures = ["capteurs_initiaux.json"]

    def setUp(self):
        self.serre = Capteur.objects.get(nom="Temp-Serre")
        self.url_liste = "/api/capteurs/"
        self.url_serre = f"/api/capteurs/{self.serre.pk}/"

    # GET : ce que l'API doit fournir 

    def test_get_liste(self):
        rep = self.client.get(self.url_liste)
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.assertEqual(rep.data["count"], 3)
        noms = [c["nom"] for c in rep.data["results"]]
        self.assertEqual(noms, sorted(noms))

    def test_get_detail_et_libelle(self):
        rep = self.client.get(self.url_serre)
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.assertEqual(rep.data["nom"], "Temp-Serre")
        self.assertEqual(rep.data["type_capteur"], "T")
        self.assertEqual(rep.data["type_libelle"], "Température")
        self.assertEqual(rep.data["emplacement"], "Serre A")

    def test_get_detail_absent_404(self):
        rep = self.client.get("/api/capteurs/99999/")
        self.assertEqual(rep.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_recherche(self):
        rep = self.client.get(self.url_liste, {"q": "Serre"})
        self.assertEqual([c["nom"] for c in rep.data["results"]], ["Temp-Serre"])
        rep = self.client.get(self.url_liste, {"actifs_seulement": "1"})
        self.assertEqual(rep.data["count"], 2)
        rep = self.client.get(self.url_liste, {"q": "Inexistant"})
        self.assertEqual(rep.data["count"], 0)

    def test_get_format_json(self):
        rep = self.client.get(self.url_liste, {"format": "json"})
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.assertEqual(rep["Content-Type"], "application/json")

    # Écritures : l'API doit les refuser

    def test_post_refuse_405(self):
        rep = self.client.post(self.url_liste, {
            "nom": "Lum-Serre", "type_capteur": "L", "emplacement": "Serre A",
        }, format="json")
        self.assertEqual(rep.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Capteur.objects.count(), 3)

    def test_put_et_patch_refuses_405(self):
        rep = self.client.put(self.url_serre, {
            "nom": "Temp-Serre", "type_capteur": "T", "emplacement": "Serre B",
        }, format="json")
        self.assertEqual(rep.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        rep = self.client.patch(self.url_serre, {"actif": False}, format="json")
        self.assertEqual(rep.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.serre.refresh_from_db()
        self.assertEqual(self.serre.emplacement, "Serre A")
        self.assertTrue(self.serre.actif)

    def test_delete_refuse_405(self):
        rep = self.client.delete(self.url_serre)
        self.assertEqual(rep.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Capteur.objects.count(), 3)



    def test_crud_html_toujours_present(self):
        """L'API s'ajoute au CRUD HTML sans le remplacer."""
        self.assertEqual(self.client.get("/capteurs/").status_code, 200)
        self.assertEqual(self.client.get(f"/capteurs/{self.serre.pk}/").status_code, 200)