# main.py — Interface console de SahelSound Records
#
# Ce fichier gère uniquement les menus et les saisies de l'utilisateur.
# Les calculs et les modifications des données sont dans label.py et analyse.py.

import label as lb

CHEMIN_CATALOGUE = "catalogue.json"


def demander_entier(message):
    """Demande un nombre entier en boucle jusqu'à ce que la saisie soit valide."""
    while True:
        valeur = input(message).strip()
        try:
            return int(valeur)
        except ValueError:
            print("Erreur : entrez un nombre entier (ex : 2024).")


# ── Menu principal ────────────────────────────────────────────────────────────

def afficher_menu_principal():
    """Affiche le menu principal."""
    print("\n      *** SahelSound Records ***\n")
    print("BIENVENUE, voici les menus principaux disponibles :")
    print("1. Consulter le catalogue")
    print("2. Ajouter un artiste")
    print("3. Ajouter un album à un artiste existant")
    print("4. Statistiques et rapport")
    print("5. Quitter l'application")


# ── Option 1 : consulter le catalogue ─────────────────────────────────────────

def menu_catalogue(catalogue):
    """Sous-menu de l'option 1 : lister, rechercher ou voir le détail."""
    print("\n*** Consulter le catalogue ***")
    print("  a. Afficher tous les artistes")
    print("  b. Rechercher un artiste")
    print("  c. Détail d'un artiste")

    choix = input("Votre choix (a, b ou c) : ").strip().lower()

    if choix == "a":
        artistes = lb.lister_artistes(catalogue)
        if not artistes:
            print("Le catalogue est vide.")
            return

        print(f"\n{'Nom':<20} | {'Genre':<20} | {'Pays':<15} | {'Albums'}")
        print("-" * 70)
        for artiste in artistes:
            print(f"{artiste['nom']:<20} | {artiste['genre']:<20} | "
                  f"{artiste['pays']:<15} | {artiste['nbr_albums']}")

    elif choix == "b":
        critere = input("Chercher par 'nom' ou par 'genre' : ").strip().lower()
        if critere not in ["nom", "genre"]:
            print("Critère invalide : tapez 'nom' ou 'genre'.")
            return

        valeur = input("Valeur recherchée (ex : Fally Ipupa) : ").strip()
        if valeur == "":
            print("La recherche ne peut pas être vide.")
            return

        resultats = lb.rechercher_artiste(catalogue, critere, valeur)
        if resultats:
            print(f"\n{'Nom':<20} | {'Genre':<20} | {'Pays'}")
            print("-" * 55)
            for artiste in resultats:
                print(f"{artiste['nom']:<20} | {artiste['genre']:<20} | "
                      f"{artiste['pays']}")
        else:
            print("Aucun artiste trouvé.")

    elif choix == "c":
        nom = input("Nom de l'artiste : ").strip()
        resultats = lb.rechercher_artiste(catalogue, "nom", nom)

        if not resultats:
            print("Artiste introuvable.")
            return

        # Si le nom tapé correspond exactement, on affiche celui-là en priorité.
        exacts = [a for a in resultats if a["nom"].lower() == nom.lower()]
        artiste = exacts[0] if exacts else resultats[0]
        print(f"\n{'Nom':<20} | {'Genre':<20} | {'Pays'}")
        print("-" * 55)
        print(f"{artiste['nom']:<20} | {artiste['genre']:<20} | {artiste['pays']}")
        print(f"\n{'Titre':<30} | {'Année':<8} | {'Streams'}")
        print("-" * 55)
        for album in artiste["albums"]:
            print(f"{album['titre']:<30} | {album['annee']:<8} | {album['streams']:,}")

    else:
        print("Choix invalide.")


# ── Option 2 : ajouter un artiste ─────────────────────────────────────────────

def menu_ajouter_artiste(catalogue):
    """Demande les informations d'un artiste, le valide puis le sauvegarde."""
    print("\n*** Ajouter un artiste ***")
    print("a. Saisie des informations")
    print("b. Vérification de l'identifiant")
    print("c. Sauvegarde dans catalogue.json")

    try:
        id_artiste = input("Identifiant (ex : ART-013) : ").strip()
        nom = input("Nom de scène : ").strip()
        genre = input("Genre musical : ").strip()
        pays = input("Pays d'origine : ").strip()

        nouvel_artiste = {
            "id": id_artiste,
            "nom": nom,
            "genre": genre,
            "pays": pays,
            "albums": []
        }

        catalogue = lb.ajouter_artiste(catalogue, nouvel_artiste)
        lb.sauvegarder_catalogue(catalogue, CHEMIN_CATALOGUE)
        print(f"Artiste '{nom}' ajouté avec succès !")

    except ValueError as erreur:
        print(f"Erreur : {erreur}")
    except OSError as erreur:
        print(f"Erreur lors de la sauvegarde : {erreur}")

    return catalogue


# ── Option 3 : ajouter un album ───────────────────────────────────────────────

def menu_ajouter_album(catalogue):
    """Demande un identifiant d'artiste et les infos d'un album."""
    print("\n*** Ajouter un album ***")
    print("a. Recherche de l'artiste par son identifiant")
    print("b. Saisie des informations de l'album")
    print("c. Mise à jour de catalogue.json")

    try:
        id_artiste = input("Identifiant de l'artiste (ex : ART-013) : ").strip()
        titre = input("Titre de l'album : ").strip()
        annee = demander_entier("Année de sortie : ")
        streams = demander_entier("Nombre de streams : ")

        nouvel_album = {"titre": titre, "annee": annee, "streams": streams}

        catalogue = lb.ajouter_album(catalogue, id_artiste, nouvel_album)
        lb.sauvegarder_catalogue(catalogue, CHEMIN_CATALOGUE)
        print(f"Album '{titre}' ajouté avec succès !")

    except ValueError as erreur:
        print(f"Erreur : {erreur}")
    except OSError as erreur:
        print(f"Erreur lors de la sauvegarde : {erreur}")

    return catalogue


# ── Option 4 : statistiques et rapport ────────────────────────────────────────

def menu_statistiques():
    """Affiche les 3 statistiques et propose l'export CSV."""
    # L'import est fait ici : les options 1 à 3 fonctionnent même si
    # pandas n'est pas encore installé.
    try:
        import analyse as al
    except ImportError:
        print("Pandas n'est pas installé.")
        print("Installez-le avec : pip install -r requirements.txt")
        return

    try:
        top = al.top5_artistes(CHEMIN_CATALOGUE)
        moyennes = al.moyennes_streams(CHEMIN_CATALOGUE)
        albums = al.albums_par_annee(CHEMIN_CATALOGUE)

        print("\n*** Top 5 des artistes par streams ***")
        print(top.to_string(index=False))

        print("\n*** Moyenne des streams par genre ***")
        print(moyennes.to_string(index=False))

        print("\n*** Nombre d'albums par année ***")
        print(albums.to_string(index=False))

        reponse = input("\nExporter le rapport en CSV ? (o/n) : ").strip().lower()
        if reponse == "o":
            print(al.export_CSV(CHEMIN_CATALOGUE))

    except (ValueError, OSError) as erreur:
        print(f"Erreur pendant l'analyse : {erreur}")


# ── Lancement de l'application ────────────────────────────────────────────────

def main():
    """Charge le catalogue puis affiche le menu en boucle."""
    try:
        catalogue = lb.charger_catalogue(CHEMIN_CATALOGUE)
    except (FileNotFoundError, ValueError) as erreur:
        print(f"Impossible de démarrer : {erreur}")
        return

    while True:
        afficher_menu_principal()
        choix = input("Votre choix (1 à 5) : ").strip()

        if choix == "1":
            menu_catalogue(catalogue)
        elif choix == "2":
            catalogue = menu_ajouter_artiste(catalogue)
        elif choix == "3":
            catalogue = menu_ajouter_album(catalogue)
        elif choix == "4":
            menu_statistiques()
        elif choix == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, entrez un chiffre entre 1 et 5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAu revoir !")
