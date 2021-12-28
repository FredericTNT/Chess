from datetime import datetime, date
import models.config as tb
from models.tournoi import Tournoi, Tour
from models.joueur import Joueur
from models.serialdb import serial_joueurs, unserial_joueurs, serial_tournoi, unserial_tournoi
from models.menu import Menu, LigneMenu
from models.serialdb import serial_menu, unserial_menu
from views.listestournoi import matchs_tournoi, tours_tournoi, joueurs_tournoi, resultats_tournoi
from views.listeschess import acteurs_tournois, chess_tournois
from views.chessinput import saisie_tournoi, select_tournoi, select_joueur, joueurs_inscrits
from views.chessinput import saisie_resultats, modifier_elo, Color


def menu_general(nb_joueurs, nb_tours, auto=False):
    """Séquencement du menu général"""
    menu = Menu("Tournoi d'échecs Menu général")
    menu.ajouter_ligne(LigneMenu("1", "Créer un nouveau tournoi", True))
    menu.ajouter_ligne(LigneMenu("2", "Sélectionner un tournoi", True))
    menu.ajouter_ligne(LigneMenu("3", "Liste de tous les tournois", True))
    menu.ajouter_ligne(LigneMenu("4", "Liste de tous les acteurs (par ordre alphabétique)", True))
    menu.ajouter_ligne(LigneMenu("5", "Liste de tous les acteurs (par classement elo)", True))
    menu.ajouter_ligne(LigneMenu("6", "Modifier le classement elo d'un joueur", True))
    menu.ajouter_ligne(LigneMenu("9", "Quitter l'application", True))
    while menu.choix != "9":
        print(menu)
        menu.choix_ligne()
        match menu.choix:
            case "1":
                arg_tournoi = saisie_tournoi()
                tournoi = Tournoi(arg_tournoi[0], arg_tournoi[1], date.today(), nb_tour=nb_tours,
                                  compteur_temps=arg_tournoi[2], description=arg_tournoi[3])
                liste_joueurs = []
                menu_tournoi(tournoi, liste_joueurs, nb_joueurs, auto)
                menu.etat = f"Le tournoi {tournoi.nom} de {tournoi.lieu} est sauvegardé !"
            case "2":
                clef_tournoi = select_tournoi(tb.TOURNOIS)
                if clef_tournoi:
                    tournoi = unserial_tournoi(clef_tournoi)
                    liste_joueurs = unserial_joueurs(clef_tournoi)
                    menu_tournoi(tournoi, liste_joueurs, nb_joueurs, auto)
                    menu.etat = f"Le tournoi {tournoi.nom} de {tournoi.lieu} est sauvegardé !"
                else:
                    menu.etat = f"Aucun tournoi n'est enregistré, veuillez créer un tournoi !"
            case "3":
                print(chess_tournois(tb.TOURNOIS))
            case "4":
                print(acteurs_tournois(tb.JOUEURS, "alpha"))
            case "5":
                print(acteurs_tournois(tb.JOUEURS, "elo"))
            case "6":
                print(f"{Color.SAUTLIGNE}{Color.GREEN}-------- Modification du classement elo d'un joueur "
                      f"--------{Color.END}")
                selection_joueur = select_joueur(tb.JOUEURS)
                if len(selection_joueur) == 0:
                    print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Aucun résultat à votre sélection"
                          f"{Color.END}{Color.SAUTLIGNE}")
                else:
                    modifier_elo(selection_joueur[0], tb.JOUEURS)
            case "9":
                print(f"{Color.SAUTLIGNE}  Hello world")
    return


def contexte_menu_tournoi(tournoi):
    """Génération contextualisée du menu tournoi"""
    menu = Menu(f'Tournoi {tournoi.nom} de {tournoi.lieu} le {tournoi.date_debut}')
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    liste_lignes = unserial_menu(clef_tournoi)
    if len(liste_lignes) == 0:
        menu.ajouter_ligne(LigneMenu("1", "Inscrire les joueurs", True))
        menu.ajouter_ligne(LigneMenu("2", "Générer les matchs du tour 1", False))
        menu.ajouter_ligne(LigneMenu("3", "Saisir les résultats du tour 1", False))
        menu.ajouter_ligne(LigneMenu("4", "Liste de tous les joueurs du tournoi (par ordre alphabétique)", False))
        menu.ajouter_ligne(LigneMenu("5", "Liste de tous les joueurs du tournoi (par classement elo)", False))
        menu.ajouter_ligne(LigneMenu("6", "Liste de tous les matchs du tournoi", False))
        menu.ajouter_ligne(LigneMenu("7", "Liste de tous les tours du tournoi", False))
        menu.ajouter_ligne(LigneMenu("8", "Classement du tournoi", False))
        menu.ajouter_ligne(LigneMenu("9", "Retour au menu général & sauvegarde du tournoi", True))
    else:
        for ligne in liste_lignes:
            menu.ajouter_ligne(LigneMenu(ligne.clef, ligne.texte, ligne.actif))
    return menu


def menu_tournoi(tournoi, liste_joueurs, nb_joueurs, auto=False):
    """Séquencement du menu tournoi"""
    menu = contexte_menu_tournoi(tournoi)
    while menu.choix != "9":
        print(menu)
        menu.choix_ligne()
        match menu.choix:
            case "1":
                arguments_joueurs = joueurs_inscrits(nb_joueurs, tournoi.lieu, tournoi.nom, auto)
                for arguments in arguments_joueurs:
                    joueur = Joueur(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4])
                    liste_joueurs.append(joueur)
                    tournoi.clefs_joueurs.append(joueur.nom + joueur.prenom + date.isoformat(joueur.date_naissance))
                menu.etat = "Les joueurs sont prêts !"
                menu.liste_lignes[menu.indice("1")].actif = False
                menu.liste_lignes[menu.indice("2")].actif = True
                menu.liste_lignes[menu.indice("4")].actif = True
                menu.liste_lignes[menu.indice("5")].actif = True
            case "2":
                nb_tour = len(tournoi.liste_tours) + 1
                tour = Tour(nb_tour)
                tour.lancer(datetime.today())
                menu.liste_lignes[menu.indice("2")].actif = False
                menu.liste_lignes[menu.indice("3")].actif = True
                if tour.numero == 1:
                    tour.organiser_premier_tour(liste_joueurs)
                    menu.liste_lignes[menu.indice("6")].actif = True
                    menu.liste_lignes[menu.indice("7")].actif = True
                else:
                    tour.organiser_tour_suivant(tournoi.somme_points(), liste_joueurs, tournoi)
                tournoi.enregistrer_tour(tour)
                menu.etat = f"Les matchs du {tour.nom} sont générés !"
            case "3":
                nb_tour = len(tournoi.liste_tours)
                tour = tournoi.liste_tours[nb_tour - 1]
                saisie_resultats(tour, liste_joueurs, int(nb_joueurs / 2), auto)
                tour.terminer(datetime.today())
                tournoi.enregistrer_tour(tour)
                menu.liste_lignes[menu.indice("8")].actif = True
                menu.liste_lignes[menu.indice("3")].actif = False
                menu.etat = f"Les résultats du {tour.nom} sont saisis !"
                if nb_tour < tournoi.nb_tour:
                    menu.liste_lignes[menu.indice("2")].actif = True
                    menu.liste_lignes[menu.indice("2")].texte = f"Générer les matchs du tour {nb_tour + 1}"
                    menu.liste_lignes[menu.indice("3")].texte = f"Saisir les résultats du tour {nb_tour + 1}"
            case "4":
                print(joueurs_tournoi(liste_joueurs, tournoi.lieu, "alpha"))
            case "5":
                print(joueurs_tournoi(liste_joueurs, tournoi.lieu, "elo"))
            case "6":
                print(matchs_tournoi(tournoi, liste_joueurs))
            case "7":
                print(tours_tournoi(tournoi))
            case "8":
                print(resultats_tournoi(tournoi, liste_joueurs))
            case "9":
                serial_tournoi(tournoi)
                serial_joueurs(liste_joueurs)
                clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
                serial_menu(menu.liste_lignes, clef_tournoi)
    return
