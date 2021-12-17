from datetime import date
import random
from models.joueur import Joueur


def joueurs_inscrits(nb_joueurs, tournoi):
    liste_joueurs = []
    for i in range(0, nb_joueurs):
        joueur = Joueur(f"TNT{tournoi.lieu}", f'Joueur{i}', date(2000, 7, 22), "M", random.randrange(1000, 1800, 100))
        liste_joueurs.append(joueur)
        tournoi.clefs_joueurs.append(joueur.nom + joueur.prenom + date.isoformat(joueur.date_naissance))
    return liste_joueurs


def saisie_resultats(tour, nb_match):
    for i in range(0, nb_match):
        tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    return
