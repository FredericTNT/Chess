from models.serialdb import serial_joueurs, serial_tournoi
from views.listestournoi import matchs_tournoi, tours_tournoi, joueurs_tournoi
from models.menu import Menu, LigneMenu
from views.chessinput import joueurs_inscrits, saisie_resultats
from models.tournoi import Tournoi, Tour
from datetime import datetime, date


def menu_general(NB_JOUEURS, NB_TOURS, joueurs_table, tournois_table, tours_table, matchs_table):
    menu = Menu("Tournoi d'échecs Menu général")
    menu.ajouter_ligne(LigneMenu("1", "Créer un nouveau tournoi", True))
    menu.ajouter_ligne(LigneMenu("2", "Sélectionner un tournoi", False))
    menu.ajouter_ligne(LigneMenu("3", "Liste de tous les tournois", False))
    menu.ajouter_ligne(LigneMenu("4", "Liste de tous les acteurs (par ordre alphabétique)", False))
    menu.ajouter_ligne(LigneMenu("5", "Liste de tous les acteurs (par classement)", False))
    menu.ajouter_ligne(LigneMenu("9", "Quitter l'application", True))
    while menu.choix != "9":
        print(menu)
        menu.choix_ligne()
        match menu.choix:
            case "1":
                tournoi = Tournoi("Chess", "Versailles", date.today(), nb_tour=NB_TOURS)
                menu_tournoi(tournoi, NB_JOUEURS, NB_TOURS, joueurs_table, tournois_table, tours_table, matchs_table)
                menu.etat = f"Le tournoi {tournoi.nom} a été sauvegardé !"
            case "2" | "3" | "4" | "5":
                pass
            case "9":
                print("\n  Hello world")
    return


def menu_tournoi(tournoi, NB_JOUEURS, NB_TOURS, joueurs_table, tournois_table, tours_table, matchs_table):
    menu = Menu(f'Tournoi {tournoi.nom} de {tournoi.lieu} le {tournoi.date_debut}')
    menu.ajouter_ligne(LigneMenu("1", "Inscrire les joueurs", True))
    menu.ajouter_ligne(LigneMenu("2", "Générer les matchs du tour 1", False))
    menu.ajouter_ligne(LigneMenu("3", "Saisir les résultats du tour 1", False))
    menu.ajouter_ligne(LigneMenu("4", "Modifier le classement elo d'un joueur", False))
    menu.ajouter_ligne(LigneMenu("5", "Liste de tous les joueurs du tournoi (par ordre alphabétique)", False))
    menu.ajouter_ligne(LigneMenu("6", "Liste de tous les joueurs du tournoi (par classement elo)", False))
    menu.ajouter_ligne(LigneMenu("7", "Liste de tous les matchs du tournoi", False))
    menu.ajouter_ligne(LigneMenu("8", "Liste de tous les tours du tournoi", False))
    menu.ajouter_ligne(LigneMenu("9", "Retour au menu général", True))
    liste_joueurs = []
    while menu.choix != "9":
        print(menu)
        menu.choix_ligne()
        match menu.choix:
            case "1":
                liste_joueurs = joueurs_inscrits(NB_JOUEURS)
                serial_joueurs(liste_joueurs, tournoi, joueurs_table)
                menu.etat = "Les joueurs sont prêts !"
                menu.liste_lignes[menu.indice("1")].actif = False
                menu.liste_lignes[menu.indice("2")].actif = True
                menu.liste_lignes[menu.indice("5")].actif = True
                menu.liste_lignes[menu.indice("6")].actif = True
            case "2":
                nb_tour = len(tournoi.liste_tours) + 1
                tour = Tour(nb_tour)
                tour.lancer(datetime.today())
                menu.liste_lignes[menu.indice("2")].actif = False
                menu.liste_lignes[menu.indice("3")].actif = True
                if tour.numero == 1:
                    tour.organiser_premier_tour(liste_joueurs)
                    menu.liste_lignes[menu.indice("7")].actif = True
                    menu.liste_lignes[menu.indice("8")].actif = True
                else:
                    tour.organiser_tour_suivant(tournoi.somme_points(), liste_joueurs, tournoi)
                tournoi.enregistrer_tour(tour)
                menu.etat = f"Les matchs du {tour.nom} sont générés !"
            case "3":
                saisie_resultats(tour, int(NB_JOUEURS / 2))
                tour.terminer(datetime.today())
                tournoi.enregistrer_tour(tour)
                menu.liste_lignes[menu.indice("3")].actif = False
                menu.etat = f"Les résultats du {tour.nom} sont saisis !"
                if nb_tour < tournoi.nb_tour:
                    menu.liste_lignes[menu.indice("2")].actif = True
                    menu.liste_lignes[menu.indice("2")].texte = f"Générer les matchs du tour {nb_tour + 1}"
                    menu.liste_lignes[menu.indice("3")].texte = f"Saisir les résultats du tour {nb_tour + 1}"
            case "4":
                pass
            case "5":
                print(joueurs_tournoi(liste_joueurs, tournoi.lieu, "alpha"))
            case "6":
                print(joueurs_tournoi(liste_joueurs, tournoi.lieu, "elo"))
            case "7":
                print(matchs_tournoi(tournoi, liste_joueurs))
            case "8":
                print(tours_tournoi(tournoi))
            case "9":
                serial_tournoi(tournoi, tournois_table, tours_table, matchs_table)
    return
