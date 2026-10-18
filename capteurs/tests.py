"""Tests automatisés des 12 scénarios de vérification du TP.

Lancer :  python manage.py test capteurs -v 2
Les tests utilisent une base de test distincte, créée puis détruite par Django :
les fiches de travail de db.sqlite3 ne sont jamais touchées.
"""
from django.test import Client, TestCase
from django.urls import reverse

from .models import Capteur


class ScenariosCapteursTests(TestCase):
    fixtures = ["capteurs_initiaux.json"]

    def setUp(self):
        self.serre = Capteur.objects.get(nom="Temp-Serre")

    def creer_temp_bureau(self):
        return self.client.post(reverse("capteurs:ajouter"), {
            "nom": "Temp-Bureau",
            "type_capteur": "T",
            "emplacement": "Bureau N362",
            "actif": "on",
            "description": "",
        })

    # 1 ---------------------------------------------------------------
    def test_01_liste_et_fiches_initiales(self):
        rep = self.client.get(reverse("capteurs:liste"))
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(len(rep.context["capteurs"]), 3)
        noms = [c.nom for c in rep.context["capteurs"]]
        self.assertEqual(noms, sorted(noms))  # tri par nom
        self.assertContains(rep, "Température")
        for c in Capteur.objects.all():
            url = reverse("capteurs:detail", args=[c.pk])
            self.assertContains(rep, f'href="{url}"')
            fiche = self.client.get(url)
            self.assertContains(fiche, c.emplacement)
            self.assertContains(fiche, reverse("capteurs:liste"))
        self.assertEqual(Capteur.objects.count(), 3)

    # 2 ---------------------------------------------------------------
    def test_02_id_absent_404(self):
        pk_absent = Capteur.objects.order_by("-pk").first().pk + 100
        for nom_route in ("detail", "modifier", "supprimer"):
            rep = self.client.get(reverse(f"capteurs:{nom_route}", args=[pk_absent]))
            self.assertEqual(rep.status_code, 404)
        self.assertEqual(Capteur.objects.count(), 3)

    # 3 ---------------------------------------------------------------
    def test_03_recherche_serre_puis_actifs(self):
        rep = self.client.get(reverse("capteurs:liste"), {"q": "Serre"})
        self.assertEqual([c.nom for c in rep.context["capteurs"]], ["Temp-Serre"])
        rep = self.client.get(reverse("capteurs:liste"), {"actifs_seulement": "on"})
        self.assertEqual(len(rep.context["capteurs"]), 2)
        self.assertEqual(Capteur.objects.count(), 3)

    def test_03b_recherche_invalide_trop_longue(self):
        rep = self.client.get(reverse("capteurs:liste"), {"q": "x" * 41})
        self.assertFalse(rep.context["form"].is_valid())
        self.assertEqual(len(rep.context["capteurs"]), 0)
        self.assertContains(rep, "errorlist")

    # 4 ---------------------------------------------------------------
    def test_04_recherche_nom_absent(self):
        rep = self.client.get(reverse("capteurs:liste"), {"q": "Inexistant"})
        self.assertContains(rep, "Aucun capteur")
        self.assertEqual(Capteur.objects.count(), 3)

    # 5 ---------------------------------------------------------------
    def test_05_creer_temp_bureau(self):
        rep = self.creer_temp_bureau()
        nouveau = Capteur.objects.get(nom="Temp-Bureau")
        self.assertRedirects(rep, reverse("capteurs:detail", args=[nouveau.pk]))
        self.assertTrue(nouveau.actif)
        self.assertEqual(Capteur.objects.count(), 4)

    # 6 ---------------------------------------------------------------
    def test_06_creations_invalides(self):
        self.creer_temp_bureau()
        cas = [
            {"nom": "Temp-Bureau", "type_capteur": "T", "emplacement": "X"},  # doublon
            {"nom": "AB", "type_capteur": "T", "emplacement": "X"},           # 2 caractères
            {"nom": "Temp-Vide", "type_capteur": "T", "emplacement": ""},     # emplacement vide
        ]
        for donnees in cas:
            rep = self.client.post(reverse("capteurs:ajouter"), donnees)
            self.assertEqual(rep.status_code, 200)  # pas de redirection
            self.assertTrue(rep.context["form"].errors)
            self.assertContains(rep, f'value="{donnees["nom"]}"')  # saisie conservée
        self.assertEqual(Capteur.objects.count(), 4)

    # 7 ---------------------------------------------------------------
    def test_07_modifier_prerempli_meme_pk(self):
        self.creer_temp_bureau()
        capteur = Capteur.objects.get(nom="Temp-Bureau")
        url = reverse("capteurs:modifier", args=[capteur.pk])
        rep = self.client.get(url)
        self.assertContains(rep, 'value="Bureau N362"')  # préremplissage
        rep = self.client.post(url, {
            "nom": "Temp-Bureau", "type_capteur": "T",
            "emplacement": "Bureau enseignant", "description": "",
            # case actif absente = False
        })
        self.assertRedirects(rep, reverse("capteurs:detail", args=[capteur.pk]))
        capteur.refresh_from_db()
        self.assertEqual(capteur.emplacement, "Bureau enseignant")
        self.assertFalse(capteur.actif)
        self.assertEqual(Capteur.objects.count(), 4)

    # 8 ---------------------------------------------------------------
    def test_08_modification_invalide(self):
        url = reverse("capteurs:modifier", args=[self.serre.pk])
        rep = self.client.post(url, {
            "nom": "AB", "type_capteur": "T", "emplacement": "", "actif": "on",
        })
        self.assertEqual(rep.status_code, 200)
        self.assertTrue(rep.context["form"].errors)
        self.serre.refresh_from_db()
        self.assertEqual(self.serre.nom, "Temp-Serre")
        self.assertEqual(self.serre.emplacement, "Serre A")

    # 9 ---------------------------------------------------------------
    def test_09_confirmation_puis_annuler(self):
        self.creer_temp_bureau()
        capteur = Capteur.objects.get(nom="Temp-Bureau")
        rep = self.client.get(reverse("capteurs:supprimer", args=[capteur.pk]))
        self.assertContains(rep, "Confirmer la suppression")
        self.assertContains(rep, reverse("capteurs:detail", args=[capteur.pk]))  # Annuler
        self.assertTrue(Capteur.objects.filter(pk=capteur.pk).exists())
        self.assertEqual(Capteur.objects.count(), 4)

    # 10 --------------------------------------------------------------
    def test_10_confirmer_suppression(self):
        self.creer_temp_bureau()
        capteur = Capteur.objects.get(nom="Temp-Bureau")
        rep = self.client.post(reverse("capteurs:supprimer", args=[capteur.pk]))
        self.assertRedirects(rep, reverse("capteurs:liste"))
        self.assertEqual(Capteur.objects.count(), 3)
        rep = self.client.get(reverse("capteurs:detail", args=[capteur.pk]))
        self.assertEqual(rep.status_code, 404)

    # 11 --------------------------------------------------------------
    def test_11_post_sans_csrf_403(self):
        client_csrf = Client(enforce_csrf_checks=True)
        rep = client_csrf.post(reverse("capteurs:ajouter"), {
            "nom": "Sans-Jeton", "type_capteur": "T", "emplacement": "X",
        })
        self.assertEqual(rep.status_code, 403)
        rep = client_csrf.post(reverse("capteurs:modifier", args=[self.serre.pk]), {
            "nom": "Pirate", "type_capteur": "T", "emplacement": "X",
        })
        self.assertEqual(rep.status_code, 403)
        rep = client_csrf.post(reverse("capteurs:supprimer", args=[self.serre.pk]))
        self.assertEqual(rep.status_code, 403)
        self.serre.refresh_from_db()
        self.assertEqual(self.serre.nom, "Temp-Serre")
        self.assertEqual(Capteur.objects.count(), 3)


class ListeVideTests(TestCase):
    """12 : base de test distincte, sans fixtures."""

    def test_12_liste_vide(self):
        rep = self.client.get(reverse("capteurs:liste"))
        self.assertContains(rep, "Aucun capteur dans l’inventaire")
        self.assertContains(rep, reverse("capteurs:ajouter"))
