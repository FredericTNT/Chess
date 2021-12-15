from models.joueur import Joueur
from models.tournoi import Tournoi, Tour, Match
from datetime import date, datetime
from tinydb import Query


def serial_joueurs(liste_joueurs, tournoi, joueurs_table):
    """Serialisation de la liste des joueurs et insertion dans la table joueurs"""
    query_joueurs = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    joueurs_table.remove(query_joueurs.clef == clef_tournoi)
    for joueur in liste_joueurs:
        serialized_joueur = {
            'clef': clef_tournoi,
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_naissance': date.isoformat(joueur.date_naissance),
            'sexe': joueur.sexe,
            'elo': joueur.elo
        }
        joueurs_table.insert(serialized_joueur)
    return


def unserial_joueurs(tournoi, joueurs_table):
    """Reloaded de la liste des joueurs à partir de la table joueurs"""
    liste_joueurs = []
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    for item in joueurs_table:
        if item['clef'] == clef_tournoi:
            joueur = Joueur(
                item['nom'],
                item['prenom'],
                date.fromisoformat(item['date_naissance']),
                item['sexe'],
                item['elo']
            )
            liste_joueurs.append(joueur)
    return liste_joueurs


def serial_matchs(tournoi, matchs_table):
    """Serialisation de la liste des matchs et insertion dans la table matchs"""
    query_matchs = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    matchs_table.remove(query_matchs.clef == clef_tournoi)
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
            matchs_table.insert(serialized_match)
    return


def unserial_matchs(tournoi, tour_numero, matchs_table):
    """Reloaded de la liste des matchs à partir de la table matchs"""
    liste_matchs = []
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    for item in matchs_table:
        if item['clef'] == clef_tournoi and item['tour'] == tour_numero:
            match = Match(
                item['blanc_indice'],
                item['noir_indice'],
                item['blanc_resultat'],
                item['noir_resultat']
            )
            liste_matchs.append(match)
    return liste_matchs


def serial_tours(tournoi, tours_table):
    """Serialisation de la liste des tours et insertion dans la table tours"""
    query_tours = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tours_table.remove(query_tours.clef == clef_tournoi)
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
        tours_table.insert(serialized_tour)
    return


def unserial_tours(tournoi, tours_table, matchs_table):
    """Reloaded de la liste des tours à partir de la table tours"""
    liste_tours = []
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    for item in tours_table:
        if item['clef'] == clef_tournoi:
            if item['date_heure_fin']:
                fin = datetime.fromisoformat(item['date_heure_fin'])
            else:
                fin = None
            liste_matchs = unserial_matchs(tournoi, item['numero'], matchs_table)
            tour = Tour(
                item['numero'],
                item['nom'],
                datetime.fromisoformat(item['date_heure_debut']),
                fin,
                liste_matchs
            )
            liste_tours.append(tour)
    return liste_tours


def serial_tournoi(tournoi, tournois_table, tours_table, matchs_table):
    """Serialisation du tournoi et insertion dans la table tournois"""
    query_tournois = Query()
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    tournois_table.remove(query_tournois.clef == clef_tournoi)
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
    tournois_table.insert(serialized_tournoi)
    serial_tours(tournoi, tours_table)
    serial_matchs(tournoi, matchs_table)


def unserial_tournoi(tournoi, tournois_table, tours_table, matchs_table):
    """Reloaded du tournoi à partir de la table tournois"""
    tournoi_reloaded = None
    clef_tournoi = tournoi.nom + tournoi.lieu + date.isoformat(tournoi.date_debut)
    for item in tournois_table:
        if item['clef'] == clef_tournoi:
            liste_tours = unserial_tours(tournoi, tours_table, matchs_table)
            tournoi_reloaded = Tournoi(
                item['nom'],
                item['lieu'],
                datetime.fromisoformat(item['date_debut']),
                datetime.fromisoformat(item['date_fin']),
                item['nb_tour'],
                liste_tours,
                item['compteur_temps'],
                item['description']
            )
    return tournoi_reloaded


def recherche_tournoi(table_tournois):
    for item in table_tournois:
        print(item['nom'], item['lieu'])
    return
