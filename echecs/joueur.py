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
        return f'{self.prenom} classement {self.elo} elo'
