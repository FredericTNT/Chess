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

    def doublon(self, liste_joueurs):
        """Vérifier si le joueur existe dans la liste des joueurs (même nom, prénom et date de naissance)"""
        for j in liste_joueurs:
            if self.nom == j.nom and self.prenom == j.prenom and self.date_naissance == j.date_naissance:
                return True
        return False

    def __str__(self):
        return f'{self.prenom} {self.nom} classement {self.elo} elo'
