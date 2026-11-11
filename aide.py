# label.py — Module de logique métier pour SahelSound Records

import json


# ── 1. Charger le catalogue ───────────────────────────────────────────────────

def charger_catalogue(chemin):
    """
    Charge et retourne la liste des artistes depuis un fichier JSON.

    Paramètre : chemin (str) — chemin vers le fichier JSON
    Retourne  : liste de dictionnaires (les artistes)
    """
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")


# ── 2. Sauvegarder le catalogue ───────────────────────────────────────────────

def sauvegarder_catalogue(catalogue, chemin):
    """
    Écrit la liste des artistes dans le fichier JSON.

    Paramètres : catalogue (liste), chemin (str)
    """
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(catalogue, f, ensure_ascii=False, indent=2)


# ── 3. Lister les artistes ────────────────────────────────────────────────────

def lister_artistes(catalogue):
    """
    Retourne une liste résumée de tous les artistes.
    Chaque élément contient : nom, genre, pays, nb_albums.

    Paramètre : catalogue (liste)
    Retourne  : liste de dictionnaires résumés
    """
    resultat = []
    for artiste in catalogue:
        resultat.append({
            "nom"      : artiste["nom"],
            "genre"    : artiste["genre"],
            "pays"     : artiste["pays"],
            "nb_albums": len(artiste["albums"])
        })
    return resultat
catalogue = charger_catalogue('catalogue.json')
print(lister_artistes(catalogue))
# ── 4. Rechercher un artiste ──────────────────────────────────────────────────

def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche des artistes selon un critère (nom, genre ou id).
    La recherche est insensible à la casse.

    Paramètres :
        catalogue (liste)
        critere   (str) — "nom", "genre" ou "id"
        valeur    (str) — valeur recherchée
    Retourne : liste des artistes correspondants
    """
    criteres_valides = ["nom", "genre", "id"]
    if critere not in criteres_valides:
        raise ValueError(f"Critère invalide. Choisir parmi : {criteres_valides}")

    resultats = []
    for artiste in catalogue:
        valeur_artiste = artiste.get(critere, "")
        if valeur.lower() in valeur_artiste.lower():
            resultats.append(artiste)

    return resultats


# ── 5. Ajouter un artiste ─────────────────────────────────────────────────────

def ajouter_artiste(catalogue, nouvel_artiste):
    """
    Ajoute un artiste au catalogue après validation.
    Vérifie que l'identifiant n'existe pas déjà.

    Paramètres :
        catalogue      (liste)
        nouvel_artiste (dict) — clés requises : id, nom, genre, pays, albums
    Retourne : catalogue mis à jour
    Lève     : ValueError si l'id existe déjà ou si des champs manquent
    """
    # Vérifier que les champs obligatoires sont présents
    champs_requis = ["id", "nom", "genre", "pays", "albums"]
    for champ in champs_requis:
        if champ not in nouvel_artiste or not str(nouvel_artiste[champ]).strip():
            raise ValueError(f"Le champ '{champ}' est manquant ou vide.")

    # Vérifier que l'id n'existe pas déjà
    for artiste in catalogue:
        if artiste["id"] == nouvel_artiste["id"]:
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
    # Valider les champs de l'album
    if not album.get("titre", "").strip():
        raise ValueError("Le titre de l'album est vide.")
    if not isinstance(album.get("annee"), int) or album["annee"] < 1900:
        raise ValueError("L'année doit être un entier valide (>= 1900).")
    if not isinstance(album.get("streams"), int) or album["streams"] < 0:
        raise ValueError("Le nombre de streams doit être un entier positif.")

    # Chercher l'artiste et ajouter l'album
    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            artiste["albums"].append(album)
            return catalogue

    raise ValueError(f"Aucun artiste avec l'identifiant '{id_artiste}'.")
## 4
def rechercher_artiste(catalogue, critere, valeur):
    resultats = []

    for artiste in catalogue:
        if critere in artiste:
            if artiste[critere].lower() == valeur.lower():
                resultats.append(artiste)

    return resultats
