"""Tests de l'API REST (Django REST framework)."""
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Capteur


class CapteurApiTests(APITestCase):
    fixtures = ["capteurs_initiaux.json"]

    def setUp(self):
        self.serre = Capteur.objects.get(nom="Temp-Serre")
        self.url_liste = "/api/capteurs/"
        self.url_serre = f"/api/capteurs/{self.serre.pk}/"

    def test_api_liste(self):
        rep = self.client.get(self.url_liste)
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.assertEqual(rep.data["count"], 3)
        noms = [c["nom"] for c in rep.data["results"]]
        self.assertEqual(noms, sorted(noms))

    def test_api_detail_et_libelle(self):
        rep = self.client.get(self.url_serre)
        self.assertEqual(rep.data["nom"], "Temp-Serre")
        self.assertEqual(rep.data["type_capteur"], "T")
        self.assertEqual(rep.data["type_libelle"], "Température")

    def test_api_detail_absent_404(self):
        rep = self.client.get("/api/capteurs/99999/")
        self.assertEqual(rep.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_recherche(self):
        rep = self.client.get(self.url_liste, {"q": "Serre"})
        self.assertEqual([c["nom"] for c in rep.data["results"]], ["Temp-Serre"])
        rep = self.client.get(self.url_liste, {"actifs_seulement": "1"})
        self.assertEqual(rep.data["count"], 2)

    def test_api_creation(self):
        rep = self.client.post(self.url_liste, {
            "nom": "Lum-Serre", "type_capteur": "L", "emplacement": "Serre A",
        }, format="json")
        self.assertEqual(rep.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Capteur.objects.count(), 4)

    def test_api_creation_invalide(self):
        cas = [
            {"nom": "Temp-Serre", "type_capteur": "T", "emplacement": "X"},
            {"nom": "AB", "type_capteur": "T", "emplacement": "X"},
            {"nom": "Temp-Z", "type_capteur": "Z", "emplacement": "X"},
            {"nom": "Temp-Vide", "type_capteur": "T", "emplacement": ""},
        ]
        for donnees in cas:
            rep = self.client.post(self.url_liste, donnees, format="json")
            self.assertEqual(rep.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Capteur.objects.count(), 3)

    def test_api_modification_partielle(self):
        rep = self.client.patch(self.url_serre, {"actif": False}, format="json")
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.serre.refresh_from_db()
        self.assertFalse(self.serre.actif)
        self.assertEqual(self.serre.emplacement, "Serre A")

    def test_api_modification_complete(self):
        rep = self.client.put(self.url_serre, {
            "nom": "Temp-Serre", "type_capteur": "T",
            "emplacement": "Serre B", "actif": True, "description": "Deplace",
        }, format="json")
        self.assertEqual(rep.status_code, status.HTTP_200_OK)
        self.serre.refresh_from_db()
        self.assertEqual(self.serre.emplacement, "Serre B")

    def test_api_suppression(self):
        rep = self.client.delete(self.url_serre)
        self.assertEqual(rep.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Capteur.objects.count(), 2)
        self.assertEqual(self.client.get(self.url_serre).status_code, 404)

    def test_crud_html_toujours_present(self):
        self.assertEqual(self.client.get("/capteurs/").status_code, 200)
        self.assertEqual(self.client.get(f"/capteurs/{self.serre.pk}/").status_code, 200)
