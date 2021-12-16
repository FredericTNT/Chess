from operator import attrgetter


class Tournoi:
    """Tournoi"""

    def __init__(self, nom, lieu, date_debut, date_fin=None, nb_tour=4, liste_tours=None,
                 compteur_temps="Blitz", description=""):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        if date_fin:
            self.date_fin = date_fin
        else:
            self.date_fin = date_debut
        self.nb_tour = nb_tour
        if liste_tours:
            self.liste_tours = liste_tours
        else:
            self.liste_tours = []
        self.compteur_temps = compteur_temps
        self.description = description

    def enregistrer_tour(self, tour):
        """Enregistrement d'un tour du tournoi"""
        if tour in self.liste_tours:
            self.liste_tours[self.liste_tours.index(tour)].numero = tour.numero
            self.liste_tours[self.liste_tours.index(tour)].nom = tour.nom
            self.liste_tours[self.liste_tours.index(tour)].date_heure_debut = tour.date_heure_debut
            self.liste_tours[self.liste_tours.index(tour)].date_heure_fin = tour.date_heure_fin
            self.liste_tours[self.liste_tours.index(tour)].liste_matchs = tour.liste_matchs
        else:
            self.liste_tours.append(tour)

    def somme_points(self):
        """Calculer le nombre total de points par joueur"""
        joueurs_points = {}
        for tour in self.liste_tours:
            for match in tour.liste_matchs:
                if tour.numero == 1:
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

    def __init__(self, numero, nom=None, date_heure_debut=None, date_heure_fin=None, liste_matchs=None):
        self.numero = numero
        if nom:
            self.nom = nom
        else:
            self.nom = f'Round {numero}'
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin
        if liste_matchs:
            self.liste_matchs = liste_matchs
        else:
            self.liste_matchs = []

    def organiser_premier_tour(self, liste_joueurs):
        """Tri des joueurs par ordre décroissant elo et affectation des matchs premier tour"""
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('elo'), reverse=True)
        k = int(len(joueurs_tries) / 2)
        for i in range(0, int(len(joueurs_tries)/2)):
            self.liste_matchs.append(Match(joueurs_tries[i].indice(liste_joueurs),
                                           joueurs_tries[k].indice(liste_joueurs)))
            k += 1
        return

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
                p_noir = -1
                break
        if p_noir >= 0:
            suisse[p_noir].adversaire = False
        return p_noir

    def match_generation(self, nb_match, p_blanc, p_noir, suisse, index_max_joueur):
        """Génération des matchs pour un tour"""
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
                return False
            else:
                generation = self.match_generation(nb_match - 1, i, j, suisse, index_max_joueur)
                if generation:
                    self.liste_matchs.append(Match(suisse[i].indice, suisse[j].indice))
                return generation

    def organiser_tour_suivant(self, joueurs_points, liste_joueurs, tournoi):
        """Tri des joueurs par ordre décroissant des points / elo et affectation des matchs tour suivant"""
        liste_suisse = []
        for clef in joueurs_points:
            liste_suisse.append(TriSuisse(clef, joueurs_points[clef], liste_joueurs[clef].elo,
                                          tournoi.rencontres(clef)))
        suisse_tries = sorted(liste_suisse, key=attrgetter('points', 'elo'), reverse=True)
        nb_match = int(len(liste_joueurs)/2)
        generation = False
        while not generation:
            for y in suisse_tries:
                y.adversaire = True
            if len(suisse_tries[0].rencontres) == len(suisse_tries):
                k = 1
                for i in range(0, len(suisse_tries), 2):
                    self.liste_matchs.append(Match(suisse_tries[i].indice, suisse_tries[k].indice))
                    k += 2
                break
            generation = self.match_generation(nb_match, 0, 0, suisse_tries, len(liste_suisse) - 1)
        return

    def lancer(self, date_heure_debut):
        """Affectation de la date et heure de début du tour"""
        self.date_heure_debut = date_heure_debut

    def terminer(self, date_heure_fin):
        """Affectation de la date et heure de fin du tour"""
        self.date_heure_fin = date_heure_fin

    def __str__(self):
        """Générer l'affichage du tour"""
        page = f"\n-------- Tour {self.nom} --------\n"
        for match in self.liste_matchs:
            page += f"\n  Joueur {match.blanc[0]} (R) {match.blanc[1]} " \
                    f"contre Joueur {match.noir[0]} (R) {match.noir[1]}"
        page += "\n"
        return page


class Match:
    """Match"""

    def __init__(self, joueur_blanc, joueur_noir, resultat_blanc=0.0, resultat_noir=0.0):
        self.blanc = [joueur_blanc, resultat_blanc]
        self.noir = [joueur_noir, resultat_noir]

    def resultat(self, statut):
        """Affectation des points en fonction du résultat du match"""
        if statut == "G":
            self.blanc[1] = 1.0
        elif statut == "P":
            self.noir[1] = 1.0
        else:
            self.blanc[1] = 0.5
            self.noir[1] = 0.5


class TriSuisse:
    """Objet pour le tri et la recherche d'adversaire tournoi système Suisse"""

    def __init__(self, indice, points, elo, rencontres):
        self.indice = indice
        self.points = points
        self.elo = elo
        self.rencontres = rencontres
        self.adversaire = True
