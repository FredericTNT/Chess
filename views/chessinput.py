from datetime import date
import random
from models.joueur import Joueur


def joueurs_inscrits(nb_joueurs):
    liste_joueurs = []
    for i in range(0, nb_joueurs):
        liste_joueurs.append(Joueur("TNT", f'Joueur{i}', date(2000, 7, 22), "M", random.randrange(1000, 1800, 100)))
    return liste_joueurs


def saisie_resultats(tour, nb_match):
    for i in range(0, nb_match):
        tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    return
