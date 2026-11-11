import json
import pandas as pd

def convert_dataframe(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        catalogue = json.load(fichier)
    # Doucle pour aplatir la liste des albums 
    donnees = []
    for artiste in catalogue:
        for album in artiste["albums"]:
            donnees.append({
                "nom"    : artiste["nom"],
                "genre"  : artiste["genre"],
                "pays"   : artiste["pays"],
                "titre"  : album["titre"],
                "annee"  : album["annee"],
                "streams": album["streams"]
            })
    return pd.DataFrame(donnees)


def top5_artistes(chemin):
    df = convert_dataframe(chemin)
    resultats = (df.groupby("nom")["streams"].sum().sort_values(ascending=False).head(5))
    resultats.columns = ["Artistes", "Total streams"]
    return resultats

def moyennes_streams(chemin):
    df = convert_dataframe(chemin)
    moyennes = (df.groupby("genre")["streams"].mean().round(0).astype(int).sort_values(ascending=False))
    moyennes.columns = ["Genres", "Moyennes streams"]
    return moyennes

def filtre_albums(chemin):
    df = convert_dataframe(chemin)
    resultats = (df.groupby("annee")["titre"].count().reset_index())
    resultats.columns = ["Année", "Nb albums"]
    return resultats
 
 # je ne suis pas encore sur que cette fonction. 
def export_CSV (chemin):
    top = top5_artistes(chemin)
    moyennes = moyennes_streams(chemin)
    albums = filtre_albums(chemin)

    with open("rapport.csv", "w", encoding="utf-8-sig") as f:

        f.write("\nTop 5 des artistes par streams\n")
        top.to_csv(f, index=False)

        f.write("\nMoyennes des streams par genres\n")
        moyennes.to_csv(f, index=False)

        f.write("\nalbums par annee\n")
        albums.to_csv(f, index=False)
    return "Le fichier rapport.csv a été créé avec succès."


# et je n'est pas encore commenté complètement les fonction.