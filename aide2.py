# analyse.py — Module d'analyse Pandas pour SahelSound Records

import json
import pandas as pd


# ── Fonction utilitaire : construire le DataFrame ─────────────────────────────

def _construire_dataframe(chemin):
    """
    Charge le JSON et le convertit en DataFrame Pandas aplati.
    Chaque ligne correspond à un album.

    Colonnes : nom, genre, pays, titre, annee, streams
    """
    with open(chemin, "r", encoding="utf-8") as f:
        catalogue = json.load(f)

    lignes = []
    for artiste in catalogue:
        for album in artiste["albums"]:
            lignes.append({
                "nom"    : artiste["nom"],
                "genre"  : artiste["genre"],
                "pays"   : artiste["pays"],
                "titre"  : album["titre"],
                "annee"  : album["annee"],
                "streams": album["streams"]
            })

    return pd.DataFrame(lignes)


# ── 1. Top 5 artistes par streams ─────────────────────────────────────────────

def top5_artistes(chemin):
    """
    Retourne les 5 artistes avec le plus grand nombre total de streams.

    Paramètre : chemin (str) — chemin vers catalogue.json
    Retourne  : DataFrame avec colonnes nom et streams
    """
    df = _construire_dataframe(chemin)

    top5 = (df.groupby("nom")["streams"]
              .sum()
              .sort_values(ascending=False)
              .head(5)
              .reset_index())

    top5.columns = ["Artiste", "Total streams"]
    return top5


# ── 2. Moyenne des streams par genre ──────────────────────────────────────────

def moyenne_streams_par_genre(chemin):
    """
    Retourne la moyenne des streams par genre musical.

    Paramètre : chemin (str)
    Retourne  : DataFrame avec colonnes genre et moyenne streams
    """
    df = _construire_dataframe(chemin)

    moyennes = (df.groupby("genre")["streams"]
                  .mean()
                  .sort_values(ascending=False)
                  .reset_index())

    moyennes.columns = ["Genre", "Moyenne streams"]
    moyennes["Moyenne streams"] = moyennes["Moyenne streams"].round(0).astype(int)
    return moyennes


# ── 3. Nombre d'albums par année ──────────────────────────────────────────────

def albums_par_annee(chemin):
    """
    Retourne le nombre d'albums sortis par année.

    Paramètre : chemin (str)
    Retourne  : DataFrame avec colonnes annee et nb_albums
    """
    df = _construire_dataframe(chemin)

    par_annee = (df.groupby("annee")["titre"]
                   .count()
                   .reset_index())

    par_annee.columns = ["Année", "Nb albums"]
    return par_annee


# ── 4. Exporter le rapport CSV ────────────────────────────────────────────────

def exporter_rapport(chemin):
    """
    Génère un rapport complet et l'exporte dans rapport.csv.
    Le fichier contient les 3 statistiques séparées par des sections.

    Paramètre : chemin (str)
    """
    top5     = top5_artistes(chemin)
    moyennes = moyenne_streams_par_genre(chemin)
    par_annee = albums_par_annee(chemin)

    with open("rapport.csv", "w", encoding="utf-8-sig") as f:

        f.write("TOP 5 ARTISTES PAR STREAMS\n")
        top5.to_csv(f, index=False)

        f.write("\nMOYENNE DES STREAMS PAR GENRE\n")
        moyennes.to_csv(f, index=False)

        f.write("\nALBUMS PAR ANNEE\n")
        par_annee.to_csv(f, index=False)