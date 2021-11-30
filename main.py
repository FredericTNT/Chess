from datetime import date, datetime
from operator import attrgetter


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
        return f'{self.prenom} {self.nom} {ans} ans classement {self.elo} elo'


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


class Tour:
    """Tour"""

    def __init__(self, nom):
        self.nom = nom
        self.date_heure_debut = None
        self.date_heure_fin = None
        self.liste_matchs = []

    def organiser_premier_tour(self, liste_joueurs):
        """Tri des joueurs par ordre décroissant elo et affectation des matchs premier tour"""
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('elo'), reverse=True)
        self.liste_matchs.append(Match(joueurs_tries[0].indice(liste_joueurs), joueurs_tries[4].indice(liste_joueurs)))
        self.liste_matchs.append(Match(joueurs_tries[1].indice(liste_joueurs), joueurs_tries[5].indice(liste_joueurs)))
        self.liste_matchs.append(Match(joueurs_tries[2].indice(liste_joueurs), joueurs_tries[6].indice(liste_joueurs)))
        self.liste_matchs.append(Match(joueurs_tries[3].indice(liste_joueurs), joueurs_tries[7].indice(liste_joueurs)))

    def organiser_tour_suivant(self, dico_joueurs_points, liste_joueurs):
        """Tri des joueurs par ordre décroissant des points / elo et affectation des matchs tour suivant"""
        liste_tri_suisse = []
        for clef in dico_joueurs_points:
            liste_tri_suisse.append(TriSuisse(clef, dico_joueurs_points[clef], liste_joueurs[clef].elo))
        joueurs_tries = sorted(liste_tri_suisse, key=attrgetter('points', 'elo'), reverse=True)
        for i in range(0, 8): print(joueurs_tries[i].indice, joueurs_tries[i].points, joueurs_tries[i].elo)
        self.liste_matchs.append(Match(joueurs_tries[0].indice, joueurs_tries[1].indice))
        self.liste_matchs.append(Match(joueurs_tries[2].indice, joueurs_tries[3].indice))
        self.liste_matchs.append(Match(joueurs_tries[4].indice, joueurs_tries[5].indice))
        self.liste_matchs.append(Match(joueurs_tries[6].indice, joueurs_tries[7].indice))

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
    """Clef pour le tri tournoi système Suisse"""

    def __init__(self, indice, points, elo):
        self.indice = indice
        self.points = points
        self.elo = elo


def joueurs_inscrits():
    joueur1 = Joueur("A", "Guillaume", date(1997, 2, 11), "M", 1200)
    joueur2 = Joueur("B", "Michel", date(1937, 12, 8), "M", 1250)
    joueur3 = Joueur("C", "Benoît", date(1962, 11, 11), "M", 1300)
    joueur4 = Joueur("D", "Antoine", date(1999, 9, 14), "M", 1350)
    joueur5 = Joueur("E", "André", date(1934, 3, 11), "M", 1000)
    joueur6 = Joueur("F", "Nicolas", date(1999, 2, 11), "M", 1250)
    joueur7 = Joueur("G", "Arthur", date(2002, 1, 6), "M", 1500)
    joueur8 = Joueur("H", "Frédéric", date(1962, 7, 22), "M", 1525)
    return joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8


def saisie_resultats(tour):
    tour.liste_matchs[0].resultat("G")
    tour.liste_matchs[1].resultat("G")
    tour.liste_matchs[2].resultat("P")
    tour.liste_matchs[3].resultat("N")
    return


def main():
    tournoi = Tournoi("Chess", "Versailles", date.today())
    print(f'Tournoi de {tournoi.lieu} le {tournoi.date_debut}')
    liste_joueurs = joueurs_inscrits()
    for i in range(0, 8): print(liste_joueurs[i])

    nb_tour = 0
    while tournoi.nb_tour > nb_tour:
        nb_tour += 1
        tour = Tour(f'Round {nb_tour}')
        if nb_tour == 1:
            tour.organiser_premier_tour(liste_joueurs)
        else:
            tour.organiser_tour_suivant(tournoi.somme_points(), liste_joueurs)
        tour.lancer(datetime.today())
        saisie_resultats(tour)
        tour.terminer(datetime.today())
        tournoi.enregistrer(tour)
        print(f'Tour {tour.nom} {tour.date_heure_debut} premier match {tour.liste_matchs[0]}')
        print(f'Tour {tour.nom} dernier match {tour.liste_matchs[3]} {tour.date_heure_fin}')
    return


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
