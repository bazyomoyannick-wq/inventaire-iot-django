# Inventaire IdO — TP Django CRUD (PROG1397)

Application Django 5.2 qui gère des fiches de capteurs IdO : liste avec recherche, fiche détaillée, création, modification et suppression avec confirmation.

## Installation (Windows)

Dans le dossier du projet (celui qui contient `manage.py`) :

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Migrations

```
.venv\Scripts\python.exe manage.py migrate
```

La base `db.sqlite3` n’est pas fournie dans l’archive; cette commande la recrée.

## Préparation des trois fiches

Option 1 — fixture fournie (la plus rapide) :

```
.venv\Scripts\python.exe manage.py loaddata capteurs_initiaux
```

Option 2 — administration : créer un superutilisateur (`manage.py createsuperuser`), ouvrir http://127.0.0.1:8000/admin/ et ajouter Temp-Serre, Hum-Atelier et Press-Salle selon le tableau de l’énoncé.

## Démarrage

```
.venv\Scripts\python.exe manage.py runserver
```

Ouvrir http://127.0.0.1:8000/capteurs/ (la racine redirige aussi vers cette page).

## Routes

| Chemin | Nom de route | GET | POST |
|---|---|---|---|
| `/capteurs/` | `capteurs:liste` | Liste + recherche | — |
| `/capteurs/<pk>/` | `capteurs:detail` | Fiche | — |
| `/capteurs/ajouter/` | `capteurs:ajouter` | Formulaire vide | Création |
| `/capteurs/<pk>/modifier/` | `capteurs:modifier` | Formulaire prérempli | Mise à jour |
| `/capteurs/<pk>/supprimer/` | `capteurs:supprimer` | Confirmation | Suppression |

## Tests automatisés

Les 12 scénarios de vérification sont couverts par `capteurs/tests.py` (base de test distincte, les fiches de travail ne sont pas touchées) :

```
.venv\Scripts\python.exe manage.py test capteurs -v 2
```

## Contenu de l’archive

- `inventaire_iot/` : configuration du projet
- `capteurs/` : modèle, formulaires, vues, URL, gabarits, migrations, fixture, tests
- `OBSERVATIONS.md` : les 12 vérifications (attendu / observé / statut)
- `REPONSES.md` : réponses aux six questions
- `captures/` : liste avec recherche, fiche détaillée, formulaire invalide, confirmation de suppression
