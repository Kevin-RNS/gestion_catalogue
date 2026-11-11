# label.py — Logique métier de SahelSound Records
#
# Ce module contient toutes les fonctions qui travaillent sur les données :
# charger, sauvegarder, lister, rechercher, ajouter un artiste ou un album.
# Il ne contient aucun "print" de menu : c'est main.py qui gère l'affichage.

import json


# ── 1. Charger le catalogue ───────────────────────────────────────────────────

def charger_catalogue(chemin):
    """
    Charge et retourne la liste des artistes depuis un fichier JSON.

    Paramètre : chemin (str) — chemin vers le fichier JSON
    Retourne  : liste de dictionnaires (les artistes)
    """
    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        # On prévient main.py pour qu'il affiche un message clair.
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {chemin} n'est pas un JSON valide.")


# ── 2. Sauvegarder le catalogue ───────────────────────────────────────────────

def sauvegarder_catalogue(catalogue, chemin):
    """
    Écrit la liste des artistes dans le fichier JSON.

    Paramètres : catalogue (liste), chemin (str)
    """
    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(catalogue, fichier, ensure_ascii=False, indent=4)


# ── 3. Lister les artistes ────────────────────────────────────────────────────

def lister_artistes(catalogue):
    """
    Retourne une liste résumée de tous les artistes.
    Chaque élément contient : nom, genre, pays, nbr_albums.

    Paramètre : catalogue (liste)
    Retourne  : liste de dictionnaires résumés
    """
    resultat = []
    for artiste in catalogue:
        resultat.append({
            "nom": artiste["nom"],
            "genre": artiste["genre"],
            "pays": artiste["pays"],
            "nbr_albums": len(artiste["albums"])
        })
    return resultat


# ── 4. Rechercher un artiste ──────────────────────────────────────────────────

def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche des artistes selon un critère (id, nom ou genre).
    La recherche est insensible à la casse et accepte une partie du texte
    (ex : "fally" trouve "Fally Ipupa").

    Paramètres :
        catalogue (liste)
        critere   (str) — "id", "nom" ou "genre"
        valeur    (str) — valeur recherchée
    Retourne : liste des artistes correspondants
    Lève     : ValueError si le critère n'est pas valide
    """
    criteres_valides = ["id", "nom", "genre"]
    if critere not in criteres_valides:
        raise ValueError(f"Critère invalide. Choisir parmi : {criteres_valides}")

    resultats = []
    for artiste in catalogue:
        valeur_artiste = str(artiste.get(critere, ""))
        if valeur.lower() in valeur_artiste.lower():
            resultats.append(artiste)

    return resultats


# ── 5. Ajouter un artiste ─────────────────────────────────────────────────────

def ajouter_artiste(catalogue, nouvel_artiste):
    """
    Ajoute un artiste au catalogue après validation.
    Vérifie que les champs sont remplis et que l'identifiant est unique.

    Paramètres :
        catalogue      (liste)
        nouvel_artiste (dict) — clés requises : id, nom, genre, pays, albums
    Retourne : catalogue mis à jour
    Lève     : ValueError si un champ est vide ou si l'id existe déjà
    """
    champs_requis = ["id", "nom", "genre", "pays", "albums"]
    for champ in champs_requis:
        if champ not in nouvel_artiste or str(nouvel_artiste[champ]).strip() == "":
            raise ValueError(f"Le champ '{champ}' est manquant ou vide.")

    for artiste in catalogue:
        if str(artiste["id"]).strip().lower() == str(nouvel_artiste["id"]).strip().lower():
            raise ValueError(f"L'identifiant '{nouvel_artiste['id']}' existe déjà.")

    catalogue.append(nouvel_artiste)
    return catalogue


# ── 6. Ajouter un album ───────────────────────────────────────────────────────

def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à un artiste existant.

    Paramètres :
        catalogue  (liste)
        id_artiste (str)  — identifiant de l'artiste cible
        album      (dict) — clés requises : titre, annee, streams
    Retourne : catalogue mis à jour
    Lève     : ValueError si l'artiste est introuvable ou les champs invalides
    """
    if not str(album.get("titre", "")).strip():
        raise ValueError("Le titre de l'album est vide.")
    if not isinstance(album.get("annee"), int) or album["annee"] < 1900:
        raise ValueError("L'année doit être un entier valide (>= 1900).")
    if not isinstance(album.get("streams"), int) or album["streams"] < 0:
        raise ValueError("Le nombre de streams doit être un entier positif.")

    for artiste in catalogue:
        if str(artiste["id"]).strip().lower() == str(id_artiste).strip().lower():
            artiste.setdefault("albums", []).append(album)
            return catalogue

    raise ValueError(f"Aucun artiste avec l'identifiant '{id_artiste}'.")
