from colored import attr

RESET = attr(0)
GREY = '\033[90m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'
SAUTLIGNE = '\n'


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

    def choix_ligne(self):
        """Saisir un choix et contrôler sa validité"""
        liste_controle = []
        for ligne in self.liste_lignes:
            if ligne.actif:
                liste_controle.append(ligne.clef)
        saisie = input(BOLD + "  Votre choix ? " + END)
        while saisie not in liste_controle:
            print(f"{SAUTLIGNE}{YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                  f"{END}{SAUTLIGNE}")
            saisie = input(BOLD + "  Votre choix ? " + END)
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
        page = RESET
        page += f"{SAUTLIGNE}-------- {YELLOW}{self.titre}{END} --------{SAUTLIGNE}"
        for ligne in self.liste_lignes:
            if ligne.actif:
                page += f"{SAUTLIGNE}{YELLOW}  {ligne.clef}. {END}{ligne.texte}"
            else:
                page += f"{SAUTLIGNE}{GREY}  {ligne.clef}. {ligne.texte}{END}"
        if self.etat:
            page += f"{SAUTLIGNE}{SAUTLIGNE}{CYAN}  {self.etat}{END}"
            self.etat = None
        page += SAUTLIGNE
        return page


class LigneMenu:
    """Ligne d'un menu"""

    def __init__(self, clef, texte, actif):
        self.clef = clef
        self.texte = texte
        self.actif = actif
