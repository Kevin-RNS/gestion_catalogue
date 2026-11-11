# analyse.py — Statistiques du catalogue avec Pandas
#
# Chaque fonction lit catalogue.json et renvoie un DataFrame prêt à afficher
# ou à exporter. Un DataFrame est un tableau : chaque ligne = un album.

import json
import pandas as pd

COLONNES = ["nom", "genre", "pays", "titre", "annee", "streams"]


# ── Fonction utilitaire : construire le DataFrame ─────────────────────────────

def convert_dataframe(chemin):
    """
    Charge le JSON et le convertit en DataFrame Pandas aplati.
    Un artiste qui a 3 albums donne 3 lignes.

    Colonnes : nom, genre, pays, titre, annee, streams
    """
    with open(chemin, "r", encoding="utf-8") as fichier:
        catalogue = json.load(fichier)

    donnees = []
    for artiste in catalogue:
        for album in artiste["albums"]:
            donnees.append({
                "nom": artiste["nom"],
                "genre": artiste["genre"],
                "pays": artiste["pays"],
                "titre": album["titre"],
                "annee": album["annee"],
                "streams": album["streams"]
            })

    # On précise les colonnes : comme ça le DataFrame reste correct même
    # si le catalogue est vide.
    return pd.DataFrame(donnees, columns=COLONNES)


# ── 1. Top 5 des artistes par streams ─────────────────────────────────────────

def top5_artistes(chemin):
    """
    Retourne les 5 artistes avec le plus grand total de streams.

    Retourne : DataFrame avec les colonnes "Artiste" et "Total streams"
    """
    df = convert_dataframe(chemin)

    if df.empty:
        return pd.DataFrame(columns=["Artiste", "Total streams"])

    # groupby + sum donne une Series : reset_index() la transforme en
    # DataFrame avec 2 colonnes, puis on les renomme.
    resultats = (df.groupby("nom")["streams"]
                   .sum()
                   .sort_values(ascending=False)
                   .head(5)
                   .reset_index())
    resultats.columns = ["Artiste", "Total streams"]
    return resultats


# ── 2. Moyenne des streams par genre ──────────────────────────────────────────

def moyennes_streams(chemin):
    """
    Retourne la moyenne des streams pour chaque genre musical.

    Retourne : DataFrame avec les colonnes "Genre" et "Moyenne streams"
    """
    df = convert_dataframe(chemin)

    if df.empty:
        return pd.DataFrame(columns=["Genre", "Moyenne streams"])

    moyennes = (df.groupby("genre")["streams"]
                  .mean()
                  .round(0)
                  .astype(int)
                  .sort_values(ascending=False)
                  .reset_index())
    moyennes.columns = ["Genre", "Moyenne streams"]
    return moyennes


# ── 3. Nombre d'albums par année ──────────────────────────────────────────────

def albums_par_annee(chemin):
    """
    Compte combien d'albums sont sortis chaque année.

    Retourne : DataFrame avec les colonnes "Année" et "Nb albums"
    """
    df = convert_dataframe(chemin)

    if df.empty:
        return pd.DataFrame(columns=["Année", "Nb albums"])

    resultats = (df.groupby("annee")["titre"]
                   .count()
                   .reset_index())
    resultats.columns = ["Année", "Nb albums"]
    return resultats


# ── 4. Exporter le rapport CSV ────────────────────────────────────────────────

def export_CSV(chemin):
    """
    Génère un rapport texte/CSV (rapport.csv) avec les 3 statistiques,
    séparées par des titres de section.

    Retourne : message de confirmation
    """
    top = top5_artistes(chemin)
    moyennes = moyennes_streams(chemin)
    albums = albums_par_annee(chemin)

    with open("rapport.csv", "w", encoding="utf-8-sig") as fichier:
        fichier.write("TOP 5 DES ARTISTES PAR STREAMS\n")
        top.to_csv(fichier, index=False)

        fichier.write("\nMOYENNE DES STREAMS PAR GENRE\n")
        moyennes.to_csv(fichier, index=False)

        fichier.write("\nALBUMS PAR ANNEE\n")
        albums.to_csv(fichier, index=False)

    return "Le fichier rapport.csv a été créé avec succès."
