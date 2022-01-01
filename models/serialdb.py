from datetime import date, datetime
from tinydb import Query
from models.joueur import Joueur
from models.tournoi import Tournoi, Tour, Match
from models.menu import LigneMenu
import models.config as tb


def serial_joueurs(liste_joueurs):
    """Serialisation de la liste des joueurs et insertion dans la table joueurs"""
    query_joueurs = Query()
    for joueur in liste_joueurs:
        tb.JOUEURS.remove((query_joueurs.nom == joueur.nom) & (query_joueurs.prenom == joueur.prenom) &
                          (query_joueurs.date_naissance == date.isoformat(joueur.date_naissance)))
        serialized_joueur = {
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_naissance': date.isoformat(joueur.date_naissance),
            'sexe': joueur.sexe,
            'elo': joueur.elo
        }
        tb.JOUEURS.insert(serialized_joueur)
    return


def unserial_joueurs(clef_tournoi):
    """Reloaded de la liste des joueurs à partir de la table joueurs"""
    liste_joueurs = []
    for clefjoueur in tb.CLEFSJOUEURS:
        if clefjoueur['clef'] == clef_tournoi:
            for item in tb.JOUEURS:
                if clefjoueur['clef_joueur'] == item['nom'] + item['prenom'] + item['date_naissance']:
                    joueur = Joueur(
                        item['nom'],
                        item['prenom'],
                        date.fromisoformat(item['date_naissance']),
                        item['sexe'],
                        item['elo']
                    )
                    liste_joueurs.append(joueur)
    return liste_joueurs


def update_elo(joueur, elo):
    """Mise à jour du classement elo d'un joueur dans la table joueurs"""
    query_joueurs = Query()
    tb.JOUEURS.update({'elo': elo}, (query_joueurs.nom == joueur['nom']) & (query_joueurs.prenom == joueur['prenom'])
                      & (query_joueurs.date_naissance == joueur['date_naissance']))


def serial_clefsjoueurs(tournoi):
    """Serialisation de la liste des clefs des joueurs et insertion dans la table clefsjoueurs"""
    query_matchs = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tb.CLEFSJOUEURS.remove(query_matchs.clef == clef_tournoi)
    for clefjoueur in tournoi.clefs_joueurs:
        serialized_clefjoueur = {
            'clef': clef_tournoi,
            'clef_joueur': clefjoueur
        }
        tb.CLEFSJOUEURS.insert(serialized_clefjoueur)
    return


def unserial_clefsjoueurs(clef_tournoi):
    """Reloaded de la liste des clefs des joueurs à partir de la table clefsjoueurs"""
    clefs_joueurs = []
    for item in tb.CLEFSJOUEURS:
        if item['clef'] == clef_tournoi:
            clefs_joueurs.append(item['clef_joueur'])
    return clefs_joueurs


def serial_matchs(tournoi):
    """Serialisation de la liste des matchs et insertion dans la table matchs"""
    query_matchs = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tb.MATCHS.remove(query_matchs.clef == clef_tournoi)
    for tour in tournoi.liste_tours:
        for match in tour.liste_matchs:
            serialized_match = {
                'clef': clef_tournoi,
                'tour': tour.numero,
                'blanc_indice': match.blanc[0],
                'blanc_resultat': match.blanc[1],
                'noir_indice': match.noir[0],
                'noir_resultat': match.noir[1]
            }
            tb.MATCHS.insert(serialized_match)
    return


def unserial_matchs(clef_tournoi, tour_numero):
    """Reloaded de la liste des matchs à partir de la table matchs"""
    liste_matchs = []
    for item in tb.MATCHS:
        if item['clef'] == clef_tournoi and item['tour'] == tour_numero:
            match = Match(
                item['blanc_indice'],
                item['noir_indice'],
                item['blanc_resultat'],
                item['noir_resultat']
            )
            liste_matchs.append(match)
    return liste_matchs


def serial_tours(tournoi):
    """Serialisation de la liste des tours et insertion dans la table tours"""
    query_tours = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tb.TOURS.remove(query_tours.clef == clef_tournoi)
    for tour in tournoi.liste_tours:
        serialized_tour = {
            'clef': clef_tournoi,
            'numero': tour.numero,
            'nom': tour.nom,
            'date_heure_debut': datetime.isoformat(tour.date_heure_debut),
        }
        if tour.date_heure_fin:
            serialized_tour['date_heure_fin'] = datetime.isoformat(tour.date_heure_fin)
        else:
            serialized_tour['date_heure_fin'] = None
        tb.TOURS.insert(serialized_tour)
    return


def unserial_tours(clef_tournoi):
    """Reloaded de la liste des tours à partir de la table tours"""
    liste_tours = []
    for item in tb.TOURS:
        if item['clef'] == clef_tournoi:
            if item['date_heure_fin']:
                fin = datetime.fromisoformat(item['date_heure_fin'])
            else:
                fin = None
            liste_matchs = unserial_matchs(clef_tournoi, item['numero'])
            tour = Tour(
                item['numero'],
                item['nom'],
                datetime.fromisoformat(item['date_heure_debut']),
                fin,
                liste_matchs
            )
            liste_tours.append(tour)
    return liste_tours


def serial_tournoi(tournoi):
    """Serialisation du tournoi et insertion dans la table tournois"""
    query_tournois = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tb.TOURNOIS.remove(query_tournois.clef == clef_tournoi)
    serialized_tournoi = {
        'clef': clef_tournoi,
        'nom': tournoi.nom,
        'lieu': tournoi.lieu,
        'date_debut': date.isoformat(tournoi.date_debut),
        'date_fin': date.isoformat(tournoi.date_fin),
        'nb_tour': tournoi.nb_tour,
        'compteur_temps': tournoi.compteur_temps,
        'description': tournoi.description
    }
    tb.TOURNOIS.insert(serialized_tournoi)
    serial_tours(tournoi)
    serial_matchs(tournoi)
    serial_clefsjoueurs(tournoi)


def unserial_tournoi(clef_tournoi):
    """Reloaded du tournoi à partir de la table tournois"""
    tournoi = None
    for item in tb.TOURNOIS:
        if item['clef'] == clef_tournoi:
            liste_tours = unserial_tours(clef_tournoi)
            clefs_joueurs = unserial_clefsjoueurs(clef_tournoi)
            tournoi = Tournoi(
                item['nom'],
                item['lieu'],
                date.fromisoformat(item['date_debut']),
                date.fromisoformat(item['date_fin']),
                item['nb_tour'],
                liste_tours,
                item['compteur_temps'],
                item['description'],
                clefs_joueurs
            )
    return tournoi


def serial_menu(liste_lignes, clef_tournoi):
    """Serialisation des lignes du menu et insertion dans la table menus"""
    query_menus = Query()
    tb.MENUS.remove(query_menus.cleftournoi == clef_tournoi)
    for ligne in liste_lignes:
        serialized_menu = {
            'cleftournoi': clef_tournoi,
            'clef': ligne.clef,
            'texte': ligne.texte,
            'actif': ligne.actif
        }
        tb.MENUS.insert(serialized_menu)
    return


def unserial_menu(clef_tournoi):
    """Reloaded des lignes du menu à partir de la table menus"""
    liste_lignes = []
    for item in tb.MENUS:
        if item['cleftournoi'] == clef_tournoi:
            ligne = LigneMenu(
                item['clef'],
                item['texte'],
                item['actif']
            )
            liste_lignes.append(ligne)
    return liste_lignes
