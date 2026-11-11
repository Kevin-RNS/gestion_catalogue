import json
## 1
def charger_catalogue(chemin):
    try:
        with open(chemin, 'r',encoding="utf-8") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        print("Fichier introuvable :", chemin)
    except json.JSONDecodeError:
        print("Erreur de format JSON dans le fichier")
    return None

## 2
def sauvegarder_catalogue(data, chemin):
    try:
        with open(chemin, 'w',encoding="utf-8") as fichier:
            json.dump(data, fichier, ensure_ascii=False, indent=4)
    except TypeError:
        print("Les données ne sont pas sérialisables en JSON")
    except IOError:
        print("Erreur lors de l'écriture du fichier")
    
## 3
def lister_artistes(catalogue):
    resultat = []
    for artiste in catalogue:
        resume = {
            "nom": artiste["nom"],
            "pays": artiste["pays"],
            "genre": artiste["genre"],
            "nbr_albums": len(artiste["albums"])
        }
        resultat.append(resume)

    return resultat


## 4
def rechercher_artiste(catalogue, critere, valeur):
    resultats = []
    
    for artiste in catalogue:
        if critere in ["id","nom", "genre"]:
            if critere in artiste and valeur.lower() in artiste[critere].lower():
                resultats.append(artiste)
    return resultats


## 5

def ajouter_artiste(catalogue, artiste):
    try:
        # Vérifier les champs obligatoires
        champs_requis = ["id", "nom", "genre", "pays", "albums"]
        
        for champ in champs_requis:
            if champ not in artiste:
                raise ValueError(f"Champ manquant : {champ}")

        #  Vérifier si l'id existe déjà .
        for a in catalogue:
            if a["id"] == artiste["id"]:
                raise ValueError("Cet id existe déjà")

        # Ajouter l'artiste
        catalogue.append(artiste)

        return "Artiste ajouté avec succès"

    except ValueError as e:
        return f"Erreur : {e}"

    except Exception as e:
        return f"Erreur inattendue : {e}"

## 6
def ajouter_album(catalogue, id_artiste, album):
    try:
        # Vérifier que l'album contient les champs nécessaires
        champs_requis = ["titre", "annee", "streams"]
        
        for champ in champs_requis:
            if champ not in album:
                raise ValueError(f"Champ manquant dans l'album : {champ}")

        # 2. Chercher l'artiste
        for artiste in catalogue:
            if artiste["id"] == id_artiste:
                
                # 3. Vérifier si la clé albums existe
                if "albums" not in artiste:
                    artiste["albums"] = []

                # 4. Ajouter l'album
                artiste["albums"].append(album)
                
                return "Album ajouté avec succès"

        # Si l'artiste n'est pas trouvé
        raise ValueError("Artiste introuvable")

    except ValueError as e:
        return f"Erreur : {e}"

    except Exception as e:
        return f"Erreur inattendue : {e}"
    


