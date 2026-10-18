from django.shortcuts import get_object_or_404, redirect, render

from .forms import CapteurForm, RechercheCapteurForm
from .models import Capteur


def capteur_liste(request):
    """R (liste) : GET seulement. Affiche les capteurs triés par nom + la recherche."""
    capteurs = Capteur.objects.order_by("nom")

    if request.GET:
        # Des paramètres sont présents : on lie le formulaire aux données reçues.
        form = RechercheCapteurForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                capteurs = capteurs.filter(nom__icontains=q)
            if form.cleaned_data["actifs_seulement"]:
                capteurs = capteurs.filter(actif=True)
        else:
            # Saisie invalide : erreurs affichées, aucun résultat.
            capteurs = Capteur.objects.none()
    else:
        form = RechercheCapteurForm()

    return render(request, "capteurs/capteur_liste.html", {
        "capteurs": capteurs,
        "form": form,
        "recherche_active": bool(request.GET),
    })


def capteur_detail(request, pk):
    """R (fiche) : GET seulement. 404 si le pk n'existe pas."""
    capteur = get_object_or_404(Capteur, pk=pk)
    return render(request, "capteurs/capteur_detail.html", {"capteur": capteur})


def capteur_ajouter(request):
    """C : GET = formulaire vide; POST = validation puis création."""
    if request.method == "POST":
        form = CapteurForm(request.POST)
        if form.is_valid():
            capteur = form.save()
            return redirect("capteurs:detail", pk=capteur.pk)
        # Invalide : on renvoie le MÊME formulaire lié (valeurs + erreurs).
    else:
        form = CapteurForm()

    return render(request, "capteurs/capteur_form.html", {
        "form": form,
        "titre": "Ajouter un capteur",
        "annuler_url": None,
    })


def capteur_modifier(request, pk):
    """U : GET = formulaire prérempli (instance); POST = données + instance."""
    capteur = get_object_or_404(Capteur, pk=pk)

    if request.method == "POST":
        # instance=capteur : save() met à jour CET objet au lieu d'en créer un nouveau.
        form = CapteurForm(request.POST, instance=capteur)
        if form.is_valid():
            form.save()
            return redirect("capteurs:detail", pk=capteur.pk)
    else:
        form = CapteurForm(instance=capteur)

    return render(request, "capteurs/capteur_form.html", {
        "form": form,
        "titre": f"Modifier le capteur {capteur.nom}",
        "capteur": capteur,
    })


def capteur_supprimer(request, pk):
    """D : GET = page de confirmation (aucune écriture); POST = suppression."""
    capteur = get_object_or_404(Capteur, pk=pk)

    if request.method == "POST":
        capteur.delete()
        return redirect("capteurs:liste")

    return render(request, "capteurs/capteur_confirmer_suppression.html", {
        "capteur": capteur,
    })
