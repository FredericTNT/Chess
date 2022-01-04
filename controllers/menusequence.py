from datetime import datetime, date
import random
import models.config as tb
from models.tournoi import Tournoi, Tour
from models.joueur import Joueur
from models.serialdb import serial_joueurs, unserial_joueurs, update_elo, serial_tournoi, unserial_tournoi
from models.menu import Menu, LigneMenu
from models.serialdb import serial_menu, unserial_menu
from views.listestournoi import matchs_tournoi, tours_tournoi, joueurs_tournoi, resultats_tournoi
from views.listeschess import chess_tournois, acteurs_tournois
from views.chessinput import select_tournoi, select_joueur
from views.chessinput import Color, show_titre, show_choix_invalide, show_doublon_joueur, show_match, show_elo
from views.chessinput import prompt_champ, saisie_date_naissance, saisie_elo


def get_tournoi(nb_tours):
    """Enregistrer un tournoi"""
    confirme = False
    while not confirme:
        nom = prompt_champ("  Nom du tournoi")
        lieu = prompt_champ("  Lieu du tournoi")
        controle_temps = {'B': 'Bullet', 'Z': 'Blitz', 'R': 'Coup Rapide'}
        compteur_temps = controle_temps[prompt_champ("  Contrôle du temps", controle_temps)]
        description = prompt_champ("  Commentaires du directeur du tournoi")
        confirme = (prompt_champ("\n  Confirmez-vous la saisie", {'O': 'Oui', 'N': 'Non'}) == 'O')
    return Tournoi(nom, lieu, date.today(), nb_tour=nb_tours, compteur_temps=compteur_temps, description=description)


def get_joueur(liste_joueurs):
    """Enregistrer un joueur"""
    joueur_inscrit = False
    while not joueur_inscrit:
        nom = prompt_champ("  Nom de famille")
        prenom = prompt_champ("  Prénom")
        date_naissance = saisie_date_naissance()
        sexe = prompt_champ("  Sexe", {'M': 'Masculin', 'F': 'Féminin'})
        elo = saisie_elo()
        joueur = Joueur(nom, prenom, date_naissance, sexe, elo)
        if joueur.doublon(liste_joueurs):
            show_doublon_joueur()
        else:
            joueur_inscrit = True
            print()
    return joueur


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
                show_titre("Enregistrement du tournoi")
                tournoi = get_tournoi(nb_tours)
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
                    menu.etat = "Aucun tournoi n'est enregistré, veuillez créer un tournoi !"
            case "3":
                print(chess_tournois(tb.TOURNOIS))
            case "4":
                print(acteurs_tournois(tb.JOUEURS, "alpha"))
            case "5":
                print(acteurs_tournois(tb.JOUEURS, "elo"))
            case "6":
                show_titre("Modification du classement elo d'un joueur")
                selection_joueur = select_joueur(tb.JOUEURS)
                if len(selection_joueur) == 0:
                    show_choix_invalide()
                else:
                    show_elo(selection_joueur[0], selection_joueur[0]['elo'])
                    elo = saisie_elo()
                    update_elo(selection_joueur[0], elo)
                    show_elo(selection_joueur[0], elo)
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
                show_titre(f"Inscription des joueurs du tournoi {tournoi.nom} de {tournoi.lieu}")
                for i in range(0, nb_joueurs):
                    if auto:
                        joueur = Joueur(f"TNT{tournoi.lieu}", f'Joueur{i}', date(2000, 7, 22), "M",
                                        random.randrange(1000, 1800, 100))
                    else:
                        joueur = get_joueur(liste_joueurs)
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
                if auto:
                    for i in range(0, int(nb_joueurs / 2)):
                        tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
                else:
                    show_titre(f"Saisie des résultats des matchs du tour {tour.numero}")
                    for match in tour.liste_matchs:
                        show_match(match, liste_joueurs)
                        saisie = prompt_champ(f"  Résultat du match {tour.liste_matchs.index(match) + 1}",
                                              {'G': 'Gagné', 'P': 'Perdu', 'N': 'Nul'})
                        match.resultat(saisie)
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
