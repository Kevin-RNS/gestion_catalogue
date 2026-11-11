import label as lb
import analyse as al

""" fonction qui affiche  les menu principale. """

def affiche_menuPrincipal():
    print("      *** SahelSound Records ***\n")
    print("BIENVENUE , voici les menu principale disponible :")
    print("1. Consulter le catalogue ")
    print("2. Ajouter un artiste ")
    print("3. Ajouter un album à un artiste existant  ")
    print("4. Statistiques et rapport  ")
    print("5. Quitter l'application ")
    
""" fonction qui effectue les action des Sous-menu de l' option  1 pour consulter le catalogue. """

def menu_1(catalogue):
    print("\n***Consulter le catalogue***")
    print("  a. Afficher tous les artistes")
    print("  b. Rechercher un artiste")
    print("  c. Détail d'un artiste")
    choix_sm1 = input("Veuillez choisir une option parmi ce disponible :\n").strip().lower()
    if choix_sm1 == "a":
        listes_art = lb.lister_artistes(catalogue)
        print(f"\n{'Nom':<25} {'genre':<20} {'Pays':<10} {'Albums':>13}")
        print("-" * 70)
        for art in listes_art:
            print(f"{art['nom']:<20} | {art['genre']:<20} | {art['pays']:<15} | {art['nbr_albums']}")

    elif choix_sm1 == "b":
        critere = input("Vous chercher par nom ou genre) : \n").strip().lower()
        valeur = input("Veuillez entrer le nom ou le genre que chercher(ex: Fally Ipupa) : \n").strip()
        resultats = lb.rechercher_artiste(catalogue, critere, valeur)
        
        if resultats:
            print(f"\n{'Nom':<25} | {'genre':<20} | {'Pays':<10}")
            print("-"*50)
            for art in resultats:
                print(f"{art['nom']:<20} | {art['genre']:<20} | {art['pays']}")
        else:
            print("Aucun artiste trouvé pour ce nom ou pour ce genre.")

    elif choix_sm1 == "c":
        nom_art = input("Veuillez entrer le nom de l'artiste (ex: Burna Boy ou Afropop) : \n").strip()
        resultats = lb.rechercher_artiste(catalogue, "nom", nom_art)
        if resultats:
            art = resultats[0]
            print(f"\n{'Nom':<20} | {'genre':<20} | {'Pays'}")
            print("-"*53)
            print(f"{art['nom']:<20} | {art['genre']:<20} | {art['pays']}\n")
            print(f"{'Titre':<30} | {'Année':<8} | {'Streams'}")
            print("-" * 55)
            for album in art["albums"]:
                print(f"{album['titre']:<30} | {album['annee']:<8} | {album['streams']:,}")
        else:
            print("Artiste introuvable.")
    else:
        print("Choix invalide.")

"""fonction qui effectue les action des Sous-menu de l' option  2 pour l' ajout d'un autre artiste """
"""
def menu_ajouter_artiste(catalogue):
    print("***Ajouter un artiste***\n")
    print("***Consulter le catalogue***\n")
    print("  a. Saisir les informations de l'artiste au clavier ")
    print("  b. Vérifier que l'identifiant n'existe pas déjà ")
    print("  c. Sauvegarder immédiatement dans catalogue.json")
    choix_sm2 = input("Veuillez choisir une option parmi ce disponible :\n").strip().lower()
    try:
        id_art  = input("Identifiant (ex: ART-013) : ").strip()
        nom     = input("Nom de scène : ").strip()
        genre   = input("Genre musical : ").strip()
        pays    = input("Pays d'origine : ").strip()

        artiste_ajouter = {
            "id": id_art,
            "nom": nom,
            "genre": genre,
            "pays": pays,
            "albums": []
        }

        catalogue = lb.ajouter_artiste(catalogue, artiste_ajouter)
        lb.sauvegarder_catalogue(catalogue, "catalogue.json")
        print(f"Artiste '{nom}' ajouté avec succès !")

    except ValueError as e:
        print(f"Erreur : {e}")

    return catalogue
"""
"""fonction qui effectue les action des Sous-menu de l' option 3 pour l' ajout d'un autre  album """ 
def menu_ajouter_album(catalogue):
    print("\n--- Ajouter un album ---")
    print("a. Rechercher l'artiste par son identifiant")
    print("b. Saisir les informations de l'album (titre, annee, streams)")
    print("c. Mettre à jour catalogue.json")
    try:
        id_artiste = input("Identifiant de l'artiste : ").strip()
        titre      = input("Titre de l'album : ").strip()
        annee      = int(input("Année de sortie : ").strip())
        streams    = int(input("Nombre de streams : ").strip())

        nouvel_album = {"titre": titre, "annee": annee, "streams": streams}

        catalogue = label.ajouter_album(catalogue, id_artiste, nouvel_album)
        label.sauvegarder_catalogue(catalogue, CHEMIN_JSON)
        print(f"Album '{titre}' ajouté avec succès !")

    except ValueError as e:
        print(f"Erreur de saisie : {e}")

    return catalogue






    
def main():
    # fonction qui charge le catalogue .json
    catalogue = lb.charger_catalogue("catalogue.json")

    while True:
# fonction pour le menu principale
        affiche_menuPrincipal()
        choix_menu = input("Veuillez choisir une option parmi ce disponible :\n")

        if choix_menu == "1":
# Sous-menu  du 1 pour consulter le catalogue.
            menu_1(catalogue)
        # elif choix == "2":
        # #     catalogue = menu_ajouter_artiste(catalogue)
        # # elif choix == "3":
        # #     catalogue = menu_ajouter_album(catalogue)
        # # elif choix == "4":
        # #     menu_statistiques()
        elif choix_menu == "5":
            print("Au revoir !")
            break
        else:
            print("Votre choix invalide, veuillez entrez un chiffre entre 1 et 5.")

main()