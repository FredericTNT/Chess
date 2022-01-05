class Menu:
    """Menu d'une application"""

    def __init__(self, titre):
        self.titre = titre
        self.liste_lignes = []
        self.choix = "0"
        self.etat = None

    def ajouter_ligne(self, ligne_menu):
        """Ajouter une nouvelle ligne dans le menu"""
        self.liste_lignes.append(ligne_menu)

    def indice(self, clef):
        """Retourner l'index de la ligne dans la liste des lignes"""
        index = -1
        for ligne in self.liste_lignes:
            if ligne.clef == clef:
                index = self.liste_lignes.index(ligne)
                break
        return index


class LigneMenu:
    """Ligne d'un menu"""

    def __init__(self, clef, texte, actif):
        self.clef = clef
        self.texte = texte
        self.actif = actif
