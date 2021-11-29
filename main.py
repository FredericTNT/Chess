from datetime import date, datetime


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

    def __str__(self):
        ans = date.today().year - self.date_naissance.year
        return f'{self.prenom} {self.nom} {ans} ans classement {self.elo} pts elo'


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
        self.round_liste = []
        self.compteur_temps = compteur_temps
        self.description = description


class Tour:
    """Tour"""

    def __init__(self, nom):
        self.nom = nom
        self.date_heure_debut = None
        self.date_heure_fin = None
        self.liste_matchs = []

    def organiser_premier_tour(self, liste_joueurs):
        """Tri des joueurs par odre décroissant elo et affectation des matchs premier tour"""
        joueurs_tries = sorted(liste_joueurs, key=lambda joueur: joueur.elo, reverse=True)
        self.liste_matchs.append(Match(joueurs_tries[0], joueurs_tries[4]))
        self.liste_matchs.append(Match(joueurs_tries[1], joueurs_tries[5]))
        self.liste_matchs.append(Match(joueurs_tries[2], joueurs_tries[6]))
        self.liste_matchs.append(Match(joueurs_tries[3], joueurs_tries[7]))

    def organiser_tour_suivant(self):
        pass

    def lancer(self, date_heure_debut):
        """Affectation de la date et heure de début du tour"""
        self.date_heure_debut = date_heure_debut

    def terminer(self, date_heure_fin):
        """Affectation de la date et heure de fin du tour"""
        self.date_heure_fin = date_heure_fin


class Match:
    """Match"""

    def __init__(self, joueur_blanc, joueur_noir):
        self.blanc = [joueur_blanc, 0]
        self.noir = [joueur_noir, 0]

    def __str__(self):
        return f'{self.blanc[0].prenom} contre {self.noir[0].prenom}'


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


def main():
    tournoi = Tournoi("Chess", "Versailles", date.today())

    tour1 = Tour("Round 1")
    tour1.organiser_premier_tour(joueurs_inscrits())
    tour1.lancer(datetime.today())
    tour1.terminer(datetime.today())

    print(f'Tournoi de {tournoi.lieu} le {tournoi.date_debut}')
    print(f'Tour {tour1.nom} {tour1.date_heure_debut} premier match {tour1.liste_matchs[0]}')
    print(f'Tour {tour1.nom} dernier match {tour1.liste_matchs[3]} {tour1.date_heure_fin}')
    return


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
