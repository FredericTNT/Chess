class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    SAUTLIGNE = '\n'


class Menu:
    """Menu d'une application"""

    def __init__(self, titre):
        self.titre = titre
        self.liste_lignes = []
        self.choix = "0"

    def ajouter_ligne(self, ligne_menu):
        """Ajouter une nouvelle ligne dans le menu"""
        self.liste_lignes.append(ligne_menu)

    def choix_ligne(self):
        """Saisir un choix et contrôler sa validité"""
        liste_controle = []
        for ligne in self.liste_lignes:
            if ligne.actif:
                liste_controle.append(ligne.clef)
        saisie = input(Color.BOLD + "  Votre choix ? " + Color.END)
        while saisie not in liste_controle:
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                  f"{Color.END}{Color.SAUTLIGNE}")
            saisie = input(Color.BOLD + "  Votre choix ? " + Color.END)
        self.choix = saisie

    def indice(self, clef):
        index = -1
        for ligne in self.liste_lignes:
            if ligne.clef == clef:
                index = self.liste_lignes.index(ligne)
                break
        return index

    def __str__(self):
        """Générer l'affichage du menu"""
        page = f"{Color.SAUTLIGNE}-------- {self.titre} --------{Color.SAUTLIGNE}"
        for ligne in self.liste_lignes:
            if ligne.actif:
                page += f"{Color.SAUTLIGNE}{Color.GREEN}  {ligne.clef}. {ligne.texte}{Color.END}"
            else:
                page += f"{Color.SAUTLIGNE}  {ligne.clef}. {ligne.texte}"
        page += Color.SAUTLIGNE
        return page


class LigneMenu:
    """Ligne d'un menu"""

    def __init__(self, clef, texte, actif):
        self.clef = clef
        self.texte = texte
        self.actif = actif
