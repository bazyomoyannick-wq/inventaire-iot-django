# Réponses aux questions de compréhension

## 1. Routes et opérations CRUD

| Route | CRUD | Méthode qui modifie la base |
|---|---|---|
| `capteurs:liste` | R | Aucune (GET seulement, lecture) |
| `capteurs:detail` | R | Aucune (GET seulement, lecture) |
| `capteurs:ajouter` | C | POST (GET affiche seulement un formulaire vide) |
| `capteurs:modifier` | U | POST (GET affiche le formulaire prérempli) |
| `capteurs:supprimer` | D | POST (GET affiche seulement la confirmation) |

Règle suivie : GET ne change jamais la base; seules les requêtes POST écrivent.

## 2. Form et ModelForm

`RechercheCapteurForm` hérite de `forms.Form` : je déclare moi-même ses champs (`q`, `actifs_seulement`) et il n’est relié à aucune table. Il sert seulement à lire et valider des critères de recherche, donc il n’a pas de `save()`.

`CapteurForm` hérite de `forms.ModelForm` : ses champs sont générés à partir du modèle `Capteur` (liste explicite dans `Meta.fields`). Il reprend automatiquement les règles du modèle (max_length, `unique`, `MinLengthValidator(3)`, choix T/H/P, `blank=True` de la description) et possède `save()` pour créer ou mettre à jour un objet.

## 3. is_valid() et cleaned_data

`is_valid()` lance toute la validation du formulaire lié (types, longueurs, champs obligatoires, unicité pour le ModelForm) et retourne `True` ou `False`. S’il y a des erreurs, elles sont stockées dans `form.errors` et affichées dans le gabarit.

`cleaned_data` est le dictionnaire des valeurs validées et converties en types Python (par exemple `actifs_seulement` devient `True`/`False`, pas la chaîne `"on"`). Il n’existe qu’après l’appel à `is_valid()`; c’est pour cela que dans `capteur_liste` je lis `form.cleaned_data["q"]` seulement à l’intérieur du `if form.is_valid():`.

## 4. instance dans la modification

```python
capteur = get_object_or_404(Capteur, pk=pk)
if request.method == "POST":
    form = CapteurForm(request.POST, instance=capteur)   # POST
    ...
else:
    form = CapteurForm(instance=capteur)                 # GET
```

- En GET, `instance=capteur` sert à préremplir les champs avec les valeurs actuelles.
- En POST, `instance=capteur` indique que `form.save()` doit mettre à jour cet objet (même pk). Il permet aussi à la validation d’unicité d’ignorer le capteur lui-même : on peut garder son nom sans erreur « existe déjà ».

Sans `instance` en POST, `save()` créerait une nouvelle fiche (ou échouerait sur le nom déjà utilisé) au lieu de modifier l’existante.

## 5. Confirmation, POST, CSRF et autorisation

- **Confirmation** : protège contre l’erreur humaine; le lien « Supprimer » ouvre une page qui demande de confirmer et offre « Annuler ».
- **POST** : la suppression est une action qui modifie la base; un GET peut être déclenché par un simple lien, un préchargement du navigateur ou un robot. Ma vue ne supprime que si `request.method == "POST"`.
- **CSRF** : le jeton `{% csrf_token %}` prouve que le POST vient bien d’un formulaire de mon site, pas d’un autre site qui pousserait le navigateur à envoyer la requête. Sans jeton, Django répond 403 (scénario 11).
- **Autorisation** : aucune des trois mesures ne vérifie *qui* a le droit de supprimer. Il faudrait des comptes et un contrôle comme `@login_required` ou des permissions. Ce TP reste un laboratoire local sans comptes.

## 6. Une erreur rencontrée

> **À rédiger avec ta propre erreur** (c’est la partie « explication personnelle » de la grille). Structure à suivre :

- **Erreur** : (message exact ou comportement observé)
- **Cause** :
- **Correction** : (ce que j’ai changé, dans quel fichier)
- **Preuve de résolution** : (capture, test qui passe, ou comportement observé ensuite)
