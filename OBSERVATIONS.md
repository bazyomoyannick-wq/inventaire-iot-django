# Observations de vérification

Scénarios réalisés dans l’ordre, à partir des trois fiches initiales. La colonne « Observé » est confirmée de deux façons : manipulation dans le navigateur et tests automatisés (`manage.py test capteurs -v 2`, 13 tests réussis).

| # | Manipulation | Résultat attendu | Résultat observé | Statut |
|---|---|---|---|---|
| 1 | Afficher liste et fiches initiales | 3 capteurs; champs lisibles; navigation complète | 3 capteurs triés par nom; type affiché « Température / Humidité / Pression », actif « Oui/Non »; chaque nom mène à sa fiche, chaque fiche a « Retour à la liste » | Réussi |
| 2 | Consulter un ID absent | 404, sans modification | `/capteurs/999/` (ainsi que `/modifier/` et `/supprimer/`) retourne 404; total toujours 3 | Réussi |
| 3 | Rechercher Serre puis actifs seulement | 1 résultat, puis 2 actifs; total en base 3 | `q=Serre` → Temp-Serre seulement; case cochée → Hum-Atelier et Temp-Serre; total 3 | Réussi |
| 4 | Rechercher un nom absent | Message « Aucun capteur »; aucune écriture | Message « Aucun capteur ne correspond à la recherche. »; total 3 | Réussi |
| 5 | Créer Temp-Bureau correctement | Redirection vers sa fiche; total 4 | Redirection vers `/capteurs/<pk>/` de Temp-Bureau; total 4 | Réussi |
| 6 | Même nom; nom de 2 caractères; emplacement vide | Erreurs visibles; saisie conservée; total 4 | Erreurs sous le champ concerné (nom déjà utilisé, au moins 3 caractères, champ obligatoire); valeurs saisies toujours dans le formulaire; total 4 | Réussi |
| 7 | Modifier : emplacement et actif=False | Préremplissage; même pk; total 4 | Formulaire prérempli avec « Bureau N362 »; après enregistrement : « Bureau enseignant », Actif = Non, même pk dans l’URL; total 4 | Réussi |
| 8 | Modification invalide | Erreurs; aucune modification persistante | Erreurs affichées; après rechargement de la fiche, les anciennes valeurs valides sont toujours là | Réussi |
| 9 | Confirmation puis Annuler | Capteur présent; total 4 | Page de confirmation affichée; Annuler ramène à la fiche; total 4 | Réussi |
| 10 | Confirmer la suppression | Redirection liste; total 3; ancienne fiche 404 | Redirection vers `/capteurs/`; total 3; ancienne URL → 404 | Réussi |
| 11 | POST sans CSRF (client avec `enforce_csrf_checks=True`) | 403; aucune écriture | 403 sur ajouter, modifier et supprimer; base inchangée | Réussi (test automatisé) |
| 12 | Liste vide dans une base de test distincte | Message clair; lien Ajouter présent | « Aucun capteur dans l’inventaire pour le moment. » et bouton « Ajouter un capteur » | Réussi (test automatisé) |

Note : pour le scénario 6 et 8 dans le navigateur, les contraintes HTML (`required`, `maxlength`) bloquent certains envois; elles ont été retirées ponctuellement avec les outils de développement (F12) pour vérifier la validation côté serveur.
