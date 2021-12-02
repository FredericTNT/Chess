from datetime import date, datetime
from operator import attrgetter
import random


class Joueur:
    """Joueur"""

    def __init__(self, nom, prenom, date_naissance, sexe, elo=0):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.elo = elo

    def classement(self, nouvel_elo):
        """Modifier le classement"""
        self.elo = nouvel_elo

    def indice(self, liste_joueurs):
        """Retourner l'index du joueur dans la liste des joueurs"""
        return liste_joueurs.index(self)

    def __str__(self):
        ans = date.today().year - self.date_naissance.year
        return f'{self.prenom} {ans} ans classement {self.elo} elo'


class Tournoi:
    """Tournoi"""

    def __init__(self, nom, lieu, date_debut, compteur_temps="Blitz", description="", nb_tour=4, date_fin=None):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        if date_fin:
            self.date_fin = date_fin
        else:
            self.date_fin = date_debut
        self.nb_tour = nb_tour
        self.liste_tours = []
        self.compteur_temps = compteur_temps
        self.description = description

    def enregistrer(self, tour):
        """Enregistrement d'un tour du tournoi"""
        self.liste_tours.append(tour)

    def somme_points(self):
        """Calculer le nombre total de points par joueur"""
        joueurs_points = {}
        for tour in self.liste_tours:
            for match in tour.liste_matchs:
                if tour.nom == "Round 1":
                    joueurs_points[match.blanc[0]] = match.blanc[1]
                    joueurs_points[match.noir[0]] = match.noir[1]
                else:
                    joueurs_points[match.blanc[0]] += match.blanc[1]
                    joueurs_points[match.noir[0]] += match.noir[1]
        return joueurs_points

    def rencontres(self, indice_joueur):
        """liste des indices des joueurs rencontrés"""
        liste_indices_joueurs = []
        for tour in self.liste_tours:
            for match in tour.liste_matchs:
                if indice_joueur == match.blanc[0]:
                    liste_indices_joueurs.append(match.noir[0])
                    break
                elif indice_joueur == match.noir[0]:
                    liste_indices_joueurs.append(match.blanc[0])
                    break
        return liste_indices_joueurs


class Tour:
    """Tour"""

    def __init__(self, numero):
        self.numero = numero
        self.nom = f'Round {numero}'
        self.date_heure_debut = None
        self.date_heure_fin = None
        self.liste_matchs = []

    def organiser_premier_tour(self, liste_joueurs):
        """Tri des joueurs par ordre décroissant elo et affectation des matchs premier tour"""
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('elo'), reverse=True)
        k = int(len(joueurs_tries) / 2)
        for i in range(0, int(len(joueurs_tries)/2)):
            print(f'[{i}]  {joueurs_tries[i]}  contre  [{k}]  {joueurs_tries[k]}')
            self.liste_matchs.append(Match(joueurs_tries[i].indice(liste_joueurs), joueurs_tries[k].indice(liste_joueurs)))
            k += 1

    def position_blanc(self, suisse):
        """Première position valide d'un adversaire blanc dans la liste"""
        p_blanc = 0
        while not suisse[p_blanc].adversaire:
            p_blanc += 1
        suisse[p_blanc].adversaire = False
        return p_blanc

    def position_noir(self, p_blanc, suisse, index_max_joueur):
        """Première position valide d'un adversaire noir dans la liste et position = -1 en cas d'échec"""
        p_noir = p_blanc + 1
        while (not suisse[p_noir].adversaire) or suisse[p_noir].indice in suisse[p_blanc].rencontres:
            if p_noir < index_max_joueur:
                p_noir += 1
            else:
                print("Adversaire non trouvé")
                p_noir = -1
                break
        if p_noir >= 0:
            suisse[p_noir].adversaire = False
        return p_noir

    def match_generation(self, nb_match, p_blanc, p_noir, suisse, index_max_joueur):
        """Génération des match pour un tour"""
        if nb_match == 0:
            return True
        else:
            i = self.position_blanc(suisse)
            j = self.position_noir(i, suisse, index_max_joueur)
            if j == -1:
                suisse[i].adversaire = True
                suisse[p_blanc].adversaire = True
                suisse[p_noir].adversaire = True
                for y in suisse:
                    if suisse.index(y) > p_blanc:
                        while len(y.rencontres) > (self.numero - 1):
                            y.rencontres.pop()
                suisse[p_blanc].rencontres.append(suisse[p_noir].indice)
                for y in suisse:
                    print(suisse.index(y), y.indice, y.points, y.elo, y.rencontres, y.adversaire)
                return False
            else:
                print(nb_match - 1, i, j)
                generation = self.match_generation(nb_match - 1, i, j, suisse, index_max_joueur)
                if generation:
                    self.liste_matchs.append(Match(suisse[i].indice, suisse[j].indice))
                return generation

    def organiser_tour_suivant(self, joueurs_points, liste_joueurs, tournoi):
        """Tri des joueurs par ordre décroissant des points / elo et affectation des matchs tour suivant"""
        liste_suisse = []
        for clef in joueurs_points:
            liste_suisse.append(TriSuisse(clef, joueurs_points[clef], liste_joueurs[clef].elo, tournoi.rencontres(clef)))
        suisse_tries = sorted(liste_suisse, key=attrgetter('points', 'elo'), reverse=True)
        for y in suisse_tries:
            print(suisse_tries.index(y), y.indice, y.points, y.elo, y.rencontres, y.adversaire)
        nb_match = int(len(liste_joueurs)/2)
        generation = False
        while not generation:
            for y in suisse_tries:
                y.adversaire = True
            if len(suisse_tries[0].rencontres) == len(suisse_tries):
                print("Appairage par défaut")
                k = 1
                for i in range(0, len(suisse_tries), 2):
                    print(f'[{i}]  {suisse_tries[i]}  contre  [{k}]  {suisse_tries[k]}')
                    self.liste_matchs.append(Match(suisse_tries[i].indice, suisse_tries[k].indice))
                    k += 2
                break
            generation = self.match_generation(nb_match, 0, 0, suisse_tries, len(liste_suisse) - 1)

    def lancer(self, date_heure_debut):
        """Affectation de la date et heure de début du tour"""
        self.date_heure_debut = date_heure_debut

    def terminer(self, date_heure_fin):
        """Affectation de la date et heure de fin du tour"""
        for match in self.liste_matchs:
            print(match)
        self.date_heure_fin = date_heure_fin


class Match:
    """Match"""

    def __init__(self, joueur_blanc, joueur_noir):
        self.blanc = [joueur_blanc, 0.0]
        self.noir = [joueur_noir, 0.0]

    def resultat(self, statut):
        """Affectation des points en fonction du résultat du match"""
        if statut == "G":
            self.blanc[1] = 1.0
        elif statut == "P":
            self.noir[1] = 1.0
        else:
            self.blanc[1] = 0.5
            self.noir[1] = 0.5

    def __str__(self):
        return f'{self.blanc[0]} {self.blanc[1]} contre {self.noir[0]} {self.noir[1]}'


class TriSuisse:
    """Objet pour le tri et la recherche d'aversaire tournoi système Suisse"""

    def __init__(self, indice, points, elo, rencontres):
        self.indice = indice
        self.points = points
        self.elo = elo
        self.rencontres = rencontres
        self.adversaire = True


def joueurs_inscrits(nb_joueurs):
    liste_joueurs = []
    for i in range(0, nb_joueurs):
        liste_joueurs.append(Joueur("TNT", f'Joueur{i}', date(2000, 7, 22), "M", random.randrange(1000, 1800, 100)))
    return liste_joueurs


def saisie_resultats(tour, nb_match):
    for i in range(0, nb_match):
        tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    return


def main():
    tournoi = Tournoi("Chess", "Versailles", date.today(), nb_tour=7)
    print(f'Tournoi de {tournoi.lieu} le {tournoi.date_debut}')
    nb_joueurs = 8
    liste_joueurs = joueurs_inscrits(nb_joueurs)
    for nb_tour in range(1, tournoi.nb_tour + 1):
        tour = Tour(nb_tour)
        if tour.numero == 1:
            tour.organiser_premier_tour(liste_joueurs)
        else:
            tour.organiser_tour_suivant(tournoi.somme_points(), liste_joueurs, tournoi)
        tour.lancer(datetime.today())
        print(f'Tour {tour.nom} {tour.date_heure_debut} premier match {tour.liste_matchs[0]}')
        saisie_resultats(tour, int(nb_joueurs / 2))
        tour.terminer(datetime.today())
        tournoi.enregistrer(tour)
    return


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
