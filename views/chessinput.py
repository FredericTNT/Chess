from datetime import date
from tinydb import Query


class Color:
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
    SAUTLIGNE = '\n'


def show_titre(titre):
    """Afficher le titre de la séquence de saisie"""
    print(f"{Color.SAUTLIGNE}{Color.GREEN}-------- {titre} --------{Color.END}{Color.SAUTLIGNE}")


def show_choix_invalide():
    """Afficher un message d'erreur suite à un choix invalide"""
    print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
          f"{Color.END}{Color.SAUTLIGNE}")


def show_doublon_joueur():
    """Afficher un message d'erreur suite à la saisie d'un joueur existant dans la liste des joueurs"""
    print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Attention! Vous avez déjà inscrit ce joueur pour le tournoi"
          f"{Color.END}{Color.SAUTLIGNE}")


def show_match(match, liste_joueurs):
    """Afficher les deux joueurs d'un match"""
    joueur_blanc = f'{liste_joueurs[match.blanc[0]].prenom.ljust(15)[0:14]} ' \
                   f'{liste_joueurs[match.blanc[0]].nom.ljust(20)[0:19]}'
    joueur_noir = f'{liste_joueurs[match.noir[0]].prenom.ljust(15)[0:14]} ' \
                  f'{liste_joueurs[match.noir[0]].nom.ljust(20)[0:19]}'
    print(f"{Color.SAUTLIGNE}    {joueur_blanc} {str(liste_joueurs[match.blanc[0]].elo).rjust(4)} elo {Color.YELLOW}"
          f"vs {Color.END}{joueur_noir} {str(liste_joueurs[match.noir[0]].elo).rjust(4)} elo{Color.SAUTLIGNE}")


def show_elo(joueur, elo):
    """Afficher le classement elo d'un joueur de la table joueurs"""
    amj = joueur['date_naissance'].split('-')
    lib_date_naissance = 'né'
    if joueur['sexe'] == 'F':
        lib_date_naissance += 'e'
    print(f"{Color.SAUTLIGNE}  {joueur['prenom']} {joueur['nom']} {lib_date_naissance} le {amj[2]}-{amj[1]}-{amj[0]} "
          f"{Color.YELLOW}{elo} elo{Color.END}{Color.SAUTLIGNE}")


def prompt_champ(message, controle=None):
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
            show_choix_invalide()
        else:
            saisie_correcte = True
    return champ


def saisie_date_naissance():
    """Saisir et contrôler une date de naissance (retour de la date au format objet date)"""
    saisie_correcte = False
    while not saisie_correcte:
        naissance = prompt_champ("  Date de naissance (format JJ-MM-AAAA)")
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
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre saisie ne respecte pas le format ou le calendrier"
                  f"{Color.END}{Color.SAUTLIGNE}")
    return date_naissance


def saisie_elo():
    """Saisir et contrôler le classement elo"""
    saisie_correcte = False
    while not saisie_correcte:
        elo_str = prompt_champ("  Classement elo (chiffre positif)")
        try:
            elo = int(elo_str)
        except ValueError:
            elo = -1
        if elo < 0:
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Vous devez saisir un chiffre positif"
                  f"{Color.END}{Color.SAUTLIGNE}")
        else:
            saisie_correcte = True
    return elo


def select_tournoi(tb_tournois):
    """Sélectionner un tournoi parmi les tournois enregistrés dans la table tournois"""
    liste_tournois = tb_tournois.all()
    if len(liste_tournois) == 0:
        return None
    show_titre("Sélection d'un tournoi")
    for tournoi in liste_tournois:
        print(f"{Color.YELLOW}  {liste_tournois.index(tournoi) + 1}.  {Color.END}"
              f"Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}")
    print()
    saisie_correcte = False
    while not saisie_correcte:
        choix = prompt_champ("  Votre choix")
        try:
            indice = int(choix) - 1
        except ValueError:
            indice = -1
        if indice not in range(0, len(liste_tournois)):
            show_choix_invalide()
        else:
            saisie_correcte = True
    clef_tournoi = \
        liste_tournois[indice]['nom'] + liste_tournois[indice]['lieu'] + liste_tournois[indice]['date_debut']
    return clef_tournoi


def select_joueur(tb_joueurs):
    """Sélectionner un joueur parmi les joueurs enregistrés dans la table joueurs"""
    query_joueurs = Query()
    poursuivre = True
    while poursuivre:
        nom = prompt_champ("  Nom de famille du joueur")
        listes_joueurs = tb_joueurs.search(query_joueurs.nom == nom)
        nb_selection = len(listes_joueurs)
        if nb_selection == 0:
            suite = input(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Aucun joueur identifié avec ce nom de famille"
                          f"{Color.SAUTLIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
            poursuivre = (suite == 'O')
        elif nb_selection == 1:
            poursuivre = False
        else:
            prenom = prompt_champ("  La sélection comporte plusieurs réponses, merci de préciser.\n  Prénom")
            listes_joueurs = tb_joueurs.search((query_joueurs.nom == nom) & (query_joueurs.prenom == prenom))
            nb_selection = len(listes_joueurs)
            if nb_selection == 0:
                suite = input(f"{Color.SAUTLIGNE}{Color.YELLOW}  "
                              f"Désolé! Aucun joueur identifié avec ce nom et ce prénom"
                              f"{Color.SAUTLIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
                poursuivre = (suite == 'O')
            elif nb_selection == 1:
                poursuivre = False
            else:
                print(f"{Color.BOLD}  La sélection comporte plusieurs réponses, merci de préciser.{Color.END}")
                date_naissance = saisie_date_naissance()
                listes_joueurs = tb_joueurs.search((query_joueurs.nom == nom) & (query_joueurs.prenom == prenom) &
                                                   (query_joueurs.date_naissance == date.isoformat(date_naissance)))
                nb_selection = len(listes_joueurs)
                if nb_selection == 0:
                    suite = input(f"{Color.SAUTLIGNE}{Color.YELLOW}  "
                                  f"Désolé! Aucun joueur identifié avec ce nom, ce prénom et cette date de naissance"
                                  f"{Color.SAUTLIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
                    poursuivre = (suite == 'O')
                else:
                    poursuivre = False
    return listes_joueurs
