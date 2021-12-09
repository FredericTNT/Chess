from datetime import date, datetime
import random
from echecs.menu import Menu, LigneMenu, Color
from echecs.joueur import Joueur
from echecs.tournoi import Tournoi, Tour

NB_TOURS = 4
NB_JOUEURS = 8


def joueurs_inscrits(nb_joueurs):
    liste_joueurs = []
    for i in range(0, nb_joueurs):
        liste_joueurs.append(Joueur("TNT", f'Joueur{i}', date(2000, 7, 22), "M", random.randrange(1000, 1800, 100)))
    return liste_joueurs


def saisie_resultats(tour, nb_match):
    for i in range(0, nb_match):
        tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    return


def menu_tournoi(tournoi):
    menu = Menu(f'Tournoi de {tournoi.lieu} le {tournoi.date_debut}')
    menu.ajouter_ligne(LigneMenu("1", "Inscrire les joueurs", True))
    menu.ajouter_ligne(LigneMenu("2", "Générer les matchs du tour 1", False))
    menu.ajouter_ligne(LigneMenu("3", "Saisir les résultats du tour 1", False))
    menu.ajouter_ligne(LigneMenu("4", "Modifier le classement elo d'un joueur", False))
    menu.ajouter_ligne(LigneMenu("5", "Liste de tous les joueurs du tournoi (par ordre alphabétique)", False))
    menu.ajouter_ligne(LigneMenu("6", "Liste de tous les joueurs du tournoi (par classement)", False))
    menu.ajouter_ligne(LigneMenu("7", "Liste de tous les matchs du tournoi", False))
    menu.ajouter_ligne(LigneMenu("8", "Liste de tous les tours du tournoi", False))
    menu.ajouter_ligne(LigneMenu("9", "Retour au menu général", True))
    while menu.choix != "9":
        print(menu)
        menu.choix_ligne()
        match menu.choix:
            case "1":
                liste_joueurs = joueurs_inscrits(NB_JOUEURS)
                menu.liste_lignes[menu.indice("1")].actif = False
                menu.liste_lignes[menu.indice("2")].actif = True
            case "2":
                nb_tour = len(tournoi.liste_tours) + 1
                tour = Tour(nb_tour)
                tour.lancer(datetime.today())
                menu.liste_lignes[menu.indice("2")].actif = False
                menu.liste_lignes[menu.indice("3")].actif = True
                if tour.numero == 1:
                    tour.organiser_premier_tour(liste_joueurs)
                    tournoi.enregistrer_tour(tour)
                elif tour.numero <= tournoi.nb_tour:
                    tour.organiser_tour_suivant(tournoi.somme_points(), liste_joueurs, tournoi)
                    tournoi.enregistrer_tour(tour)
            case "3":
                saisie_resultats(tour, int(NB_JOUEURS / 2))
                tour.terminer(datetime.today())
                tournoi.enregistrer_tour(tour)
                menu.liste_lignes[menu.indice("3")].actif = False
                if nb_tour < tournoi.nb_tour:
                    menu.liste_lignes[menu.indice("2")].actif = True
                    menu.liste_lignes[menu.indice("2")].texte = f"Générer les matchs du tour {nb_tour + 1}"
                    menu.liste_lignes[menu.indice("3")].texte = f"Saisir les résultats du tour {nb_tour + 1}"
            case "4" | "5" | "6" | "7" | "8" | "9":
                pass
    return


def main():
    menu_general = Menu("Tournoi d'échecs Menu général")
    menu_general.ajouter_ligne(LigneMenu("1", "Créer un nouveau tournoi", True))
    menu_general.ajouter_ligne(LigneMenu("2", "Sélectionner un tournoi", False))
    menu_general.ajouter_ligne(LigneMenu("3", "Liste de tous les tournois", False))
    menu_general.ajouter_ligne(LigneMenu("4", "Liste de tous les acteurs (par ordre alphabétique)", False))
    menu_general.ajouter_ligne(LigneMenu("5", "Liste de tous les acteurs (par classement)", False))
    menu_general.ajouter_ligne(LigneMenu("9", "Quitter l'application", True))
    while menu_general.choix != "9":
        print(menu_general)
        menu_general.choix_ligne()
        match menu_general.choix:
            case "1":
                tournoi = Tournoi("Chess", "Versailles", date.today(), nb_tour=NB_TOURS)
                menu_tournoi(tournoi)
            case "2" | "3" | "4" | "5":
                pass
            case "9":
                print(Color.CYAN + Color.SAUTLIGNE + "  Hello world" + Color.END)
    return


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
