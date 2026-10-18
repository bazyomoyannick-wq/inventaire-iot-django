from django.urls import path

from . import views

app_name = "capteurs"

urlpatterns = [
    path("", views.capteur_liste, name="liste"),
    path("<int:pk>/", views.capteur_detail, name="detail"),
    path("ajouter/", views.capteur_ajouter, name="ajouter"),
    path("<int:pk>/modifier/", views.capteur_modifier, name="modifier"),
    path("<int:pk>/supprimer/", views.capteur_supprimer, name="supprimer"),
]
