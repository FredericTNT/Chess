from datetime import date
from tinydb import Query
from colored import attr


class Color:
    RESET = attr(0)
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    LIGNE = '\n'


class ViewsChess:

    def show_titre(self, titre):
        """Afficher le titre de la séquence de saisie"""
        print(f"{Color.LIGNE}{Color.GREEN}-------- {titre} --------{Color.END}{Color.LIGNE}")

    def show_choix_invalide(self):
        """Afficher un message d'erreur suite à un choix invalide"""
        print(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
              f"{Color.END}{Color.LIGNE}")

    def show_aucun_joueur(self):
        """Afficher un message d'erreur suite à une sélection vide"""
        print(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Aucun joueur sélectionné"
              f"{Color.END}{Color.LIGNE}")

    def show_doublon_joueur(self):
        """Afficher un message d'erreur suite à la saisie d'un joueur existant dans la liste des joueurs"""
        print(f"{Color.LIGNE}{Color.YELLOW}  Attention! Vous avez déjà inscrit ce joueur pour le tournoi"
              f"{Color.END}{Color.LIGNE}")

    def show_match(self, match, liste_joueurs):
        """Afficher les deux joueurs d'un match"""
        joueur_blanc = f'{liste_joueurs[match.blanc[0]].prenom.ljust(15)[0:14]} ' \
                       f'{liste_joueurs[match.blanc[0]].nom.ljust(20)[0:19]}'
        joueur_noir = f'{liste_joueurs[match.noir[0]].prenom.ljust(15)[0:14]} ' \
                      f'{liste_joueurs[match.noir[0]].nom.ljust(20)[0:19]}'
        print(f"{Color.LIGNE}    {joueur_blanc} {str(liste_joueurs[match.blanc[0]].elo).rjust(4)} elo {Color.YELLOW}"
              f"vs {Color.END}{joueur_noir} {str(liste_joueurs[match.noir[0]].elo).rjust(4)} elo{Color.LIGNE}")

    def show_elo(self, joueur, elo):
        """Afficher le classement elo d'un joueur de la table joueurs"""
        amj = joueur['date_naissance'].split('-')
        lib_date_naissance = 'né'
        if joueur['sexe'] == 'F':
            lib_date_naissance += 'e'
        print(f"{Color.LIGNE}  {joueur['prenom']} {joueur['nom']} {lib_date_naissance} le {amj[2]}-{amj[1]}-{amj[0]} "
              f"{Color.YELLOW}{elo} elo{Color.END}{Color.LIGNE}")

    def prompt_champ(self, message, controle=None):
        """Saisir et contrôler un champ"""
        prompt = f"{Color.BOLD}{message} "
        liste_controle = []
        if controle:
            for clef in controle:
                prompt += f"{Color.YELLOW}{clef}{Color.END}{Color.BOLD}/{controle[clef]} "
                liste_controle.append(clef)
        saisie_correcte = False
        while not saisie_correcte:
            champ = input(f"{prompt}? {Color.END}")
            if controle and champ not in liste_controle:
                self.show_choix_invalide()
            else:
                saisie_correcte = True
        return champ

    def saisie_date_naissance(self):
        """Saisir et contrôler une date de naissance (retour de la date au format objet date)"""
        saisie_correcte = False
        while not saisie_correcte:
            naissance = self.prompt_champ("  Date de naissance (format JJ-MM-AAAA)")
            jma = naissance.split('-')
            try:
                jour = int(jma[0])
                mois = int(jma[1])
                an = int(jma[2])
                date_naissance = date(an, mois, jour)
                if date_naissance > date.today():
                    raise ValueError
                else:
                    saisie_correcte = True
            except (ValueError, IndexError):
                print(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Votre saisie ne respecte pas le format ou le calendrier"
                      f"{Color.END}{Color.LIGNE}")
        return date_naissance

    def saisie_elo(self):
        """Saisir et contrôler le classement elo"""
        saisie_correcte = False
        while not saisie_correcte:
            elo_str = self.prompt_champ("  Classement elo (chiffre positif)")
            try:
                elo = int(elo_str)
            except ValueError:
                elo = -1
            if elo < 0:
                print(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Vous devez saisir un chiffre positif"
                      f"{Color.END}{Color.LIGNE}")
            else:
                saisie_correcte = True
        return elo

    def select_tournoi(self, tb_tournois):
        """Sélectionner un tournoi parmi les tournois enregistrés dans la table tournois"""
        liste_tournois = tb_tournois.all()
        if len(liste_tournois) == 0:
            return None
        self.show_titre("Sélection d'un tournoi")
        for tournoi in liste_tournois:
            print(f"{Color.YELLOW}  {liste_tournois.index(tournoi) + 1}.  {Color.END}"
                  f"Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}")
        print()
        saisie_correcte = False
        while not saisie_correcte:
            choix = self.prompt_champ("  Votre choix")
            try:
                indice = int(choix) - 1
            except ValueError:
                indice = -1
            if indice not in range(0, len(liste_tournois)):
                self.show_choix_invalide()
            else:
                saisie_correcte = True
        clef_tournoi = \
            liste_tournois[indice]['nom'] + liste_tournois[indice]['lieu'] + liste_tournois[indice]['date_debut']
        return clef_tournoi

    def select_joueur(self, tb_joueurs):
        """Sélectionner un joueur parmi les joueurs enregistrés dans la table joueurs"""
        query_joueurs = Query()
        poursuivre = True
        while poursuivre:
            nom = self.prompt_champ("  Nom de famille du joueur")
            listes_joueurs = tb_joueurs.search(query_joueurs.nom == nom)
            nb_selection = len(listes_joueurs)
            if nb_selection == 0:
                suite = input(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Aucun joueur identifié avec ce nom de famille"
                              f"{Color.LIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
                poursuivre = (suite == 'O')
            elif nb_selection == 1:
                poursuivre = False
            else:
                prenom = self.prompt_champ("  La sélection comporte plusieurs réponses, merci de préciser.\n  Prénom")
                listes_joueurs = tb_joueurs.search((query_joueurs.nom == nom) & (query_joueurs.prenom == prenom))
                nb_selection = len(listes_joueurs)
                if nb_selection == 0:
                    suite = input(f"{Color.LIGNE}{Color.YELLOW}  "
                                  f"Désolé! Aucun joueur identifié avec ce nom et ce prénom"
                                  f"{Color.LIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
                    poursuivre = (suite == 'O')
                elif nb_selection == 1:
                    poursuivre = False
                else:
                    print(f"{Color.BOLD}  La sélection comporte plusieurs réponses, merci de préciser.{Color.END}")
                    date_naissance = self.saisie_date_naissance()
                    listes_joueurs = tb_joueurs.search(
                        (query_joueurs.nom == nom) & (query_joueurs.prenom == prenom) &
                        (query_joueurs.date_naissance == date.isoformat(date_naissance)))
                    nb_selection = len(listes_joueurs)
                    if nb_selection == 0:
                        suite = input(f"{Color.LIGNE}{Color.YELLOW}  Désolé! Aucun joueur identifié avec "
                                      f"ce nom, ce prénom et cette date de naissance"
                                      f"{Color.LIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
                        poursuivre = (suite == 'O')
                    else:
                        poursuivre = False
        return listes_joueurs

    def choix_ligne(self, menu):
        """Saisir un choix et contrôler sa validité"""
        liste_controle = []
        for ligne in menu.liste_lignes:
            if ligne.actif:
                liste_controle.append(ligne.clef)
        saisie = self.prompt_champ("  Votre choix")
        while saisie not in liste_controle:
            self.show_choix_invalide()
            saisie = self.prompt_champ("  Votre choix")
        return saisie

    def show_menu(self, menu):
        """Générer l'affichage du menu"""
        page = Color.RESET
        page += f"{Color.LIGNE}-------- {Color.YELLOW}{menu.titre}{Color.END} --------{Color.LIGNE}"
        for ligne in menu.liste_lignes:
            if ligne.actif:
                page += f"{Color.LIGNE}{Color.YELLOW}  {ligne.clef}. {Color.END}{ligne.texte}"
            else:
                page += f"{Color.LIGNE}{Color.GREY}  {ligne.clef}. {ligne.texte}{Color.END}"
        if menu.etat:
            page += f"{Color.LIGNE}{Color.LIGNE}{Color.CYAN}  {menu.etat}{Color.END}"
        page += Color.LIGNE
        print(page)
