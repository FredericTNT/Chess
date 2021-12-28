from datetime import date
from tinydb import Query
import random


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


def saisie_tournoi():
    """Saisir et contrôler les données d'un tournoi"""
    print(f"{Color.GREEN}{Color.SAUTLIGNE}-------- Enregistrement du tournoi --------{Color.END}")
    confirme = False
    while not confirme:
        nom = input(f"{Color.SAUTLIGNE}{Color.BOLD}  Nom du tournoi ? {Color.END}")
        lieu = input(f"{Color.BOLD}  Lieu du tournoi ? {Color.END}")
        saisie_correcte = False
        while not saisie_correcte:
            temps = input(f"{Color.BOLD}  Mode de contrôle du temps ({Color.END}"
                          f"{Color.YELLOW}B{Color.END}{Color.BOLD}/Bullet, "
                          f"{Color.YELLOW}Z{Color.END}{Color.BOLD}/Blitz ou "
                          f"{Color.YELLOW}R{Color.END}{Color.BOLD}/Coup Rapide) ? {Color.END}")
            if temps not in ('B', 'Z', 'R'):
                print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                      f"{Color.END}{Color.SAUTLIGNE}")
            else:
                saisie_correcte = True
        if temps == 'B':
            compteur_temps = 'Bullet'
        elif temps == 'Z':
            compteur_temps = 'Blitz'
        else:
            compteur_temps = 'Coup rapide'
        description = input(f"{Color.BOLD}  Commentaires du directeur du tournoi ? {Color.END}")
        print("")
        saisie_correcte = False
        while not saisie_correcte:
            choix = input(f"{Color.BOLD}  Confirmez-vous la saisie ({Color.END}"
                          f"{Color.YELLOW}O{Color.END}{Color.BOLD}/Oui, "
                          f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Non) ? {Color.END}")
            if choix not in ('O', 'N'):
                print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                      f"{Color.END}{Color.SAUTLIGNE}")
            else:
                saisie_correcte = True
        confirme = (choix == 'O')
    return nom, lieu, compteur_temps, description


def select_tournoi(tb_tournois):
    """Sélectionner un tournoi parmi les tournois enregistrés dans la table tournois"""
    liste_tournois = tb_tournois.all()
    if len(liste_tournois) == 0:
        return None
    print(f"{Color.GREEN}{Color.SAUTLIGNE}-------- Sélection d'un tournoi --------{Color.END}{Color.SAUTLIGNE}")
    for tournoi in liste_tournois:
        print(f"{Color.YELLOW}  {liste_tournois.index(tournoi) + 1}.  {Color.END}"
              f"Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}")
    print()
    saisie_correcte = False
    while not saisie_correcte:
        choix = input(Color.BOLD + "  Votre choix ? " + Color.END)
        try:
            indice = int(choix) - 1
        except ValueError:
            indice = -1
        if indice not in range(0, len(liste_tournois)):
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                  f"{Color.END}{Color.SAUTLIGNE}")
        else:
            saisie_correcte = True
    clef_tournoi = liste_tournois[indice]['nom'] + liste_tournois[indice]['lieu'] + liste_tournois[indice]['date_debut']
    return clef_tournoi


def saisie_date_naissance():
    """Saisir et contrôler une date de naissance (retour de la date au format objet date)"""
    saisie_correcte = False
    while not saisie_correcte:
        naissance = input(f"{Color.BOLD}  Date de naissance (format JJ-MM-AAAA) ? {Color.END}")
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
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  "
                  f"Désolé! Votre saisie ne respecte pas le format ou le calendrier"
                  f"{Color.END}{Color.SAUTLIGNE}")
    return date_naissance


def saisie_elo():
    """Saisir et contrôler le classement elo"""
    saisie_correcte = False
    while not saisie_correcte:
        elo_str = input(f"{Color.BOLD}  Classement elo (chiffre positif) ? {Color.END}")
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


def joueurs_inscrits(nb_joueurs, lieu_tournoi, nom_tournoi, auto=False):
    """Saisir et contrôler les données de tous les joueurs d'un tournoi"""
    arguments_joueurs = []
    if auto:
        for i in range(0, nb_joueurs):
            joueur = [f"TNT{lieu_tournoi}", f'Joueur{i}', date(2000, 7, 22), "M", random.randrange(1000, 1800, 100)]
            arguments_joueurs.append(joueur)
    else:
        print(f"{Color.GREEN}{Color.SAUTLIGNE}-------- Inscription des joueurs du tournoi {nom_tournoi} "
              f"de {lieu_tournoi} --------{Color.END}")
        poursuivre = (nb_joueurs != 0)
        while poursuivre:
            nom = input(f"{Color.SAUTLIGNE}{Color.BOLD}  Nom de famille ? {Color.END}")
            prenom = input(f"{Color.BOLD}  Prénom ? {Color.END}")
            date_naissance = saisie_date_naissance()
            saisie_correcte = False
            while not saisie_correcte:
                sexe = input(f"{Color.BOLD}  Sexe ({Color.END}"
                             f"{Color.YELLOW}M{Color.END}{Color.BOLD}/Masculin, "
                             f"{Color.YELLOW}F{Color.END}{Color.BOLD}/Féminin) ? {Color.END}")
                if sexe not in ('M', 'F'):
                    print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                          f"{Color.END}{Color.SAUTLIGNE}")
                else:
                    saisie_correcte = True
            elo = saisie_elo()
            joueur = [nom, prenom, date_naissance, sexe, elo]
            arguments_joueurs.append(joueur)
            nb_joueurs += -1
            poursuivre = (nb_joueurs != 0)
    return arguments_joueurs


def select_joueur(tb_joueurs):
    """Sélectionner un joueur parmi les joueurs enregistrés dans la table joueurs"""
    query_joueurs = Query()
    poursuivre = True
    while poursuivre:
        nom = input(f"{Color.SAUTLIGNE}{Color.BOLD}  Nom de famille du joueur ? {Color.END}")
        listes_joueurs = tb_joueurs.search(query_joueurs.nom == nom)
        nb_selection = len(listes_joueurs)
        if nb_selection == 0:
            suite = input(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Aucun joueur identifié avec ce nom de famille"
                          f"{Color.SAUTLIGNE}  Voulez-vous effectuer une nouvelle saisie (O/N) ? {Color.END}")
            poursuivre = (suite == 'O')
        elif nb_selection == 1:
            poursuivre = False
        else:
            prenom = input(f"{Color.BOLD}  La sélection comporte plusieurs réponses, merci de préciser."
                           f"{Color.SAUTLIGNE}  Prénom ? {Color.END}")
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


def saisie_resultats(tour, liste_joueurs, nb_match, auto=False):
    """Saisir et contrôler les résultats de tous les matchs d'un tour du tournoi"""
    if auto:
        for i in range(0, nb_match):
            tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    else:
        print(f"{Color.GREEN}{Color.SAUTLIGNE}-------- Saisie des résultats des matchs du tour {tour.numero} "
              f"--------{Color.END}")
        for match in tour.liste_matchs:
            joueur_blanc = '{:<15} {:<20}'.format(liste_joueurs[match.blanc[0]].prenom,
                                                  liste_joueurs[match.blanc[0]].nom)
            joueur_noir = '{:<15} {:<20}'.format(liste_joueurs[match.noir[0]].prenom,
                                                 liste_joueurs[match.noir[0]].nom)
            print(f"{Color.SAUTLIGNE}    {joueur_blanc} {liste_joueurs[match.blanc[0]].elo} elo {Color.YELLOW}vs "
                  f"{Color.END}{joueur_noir} {liste_joueurs[match.noir[0]].elo} elo{Color.SAUTLIGNE}")
            saisie_correcte = False
            while not saisie_correcte:
                saisie = input(f"{Color.BOLD}  Résultat du match {tour.liste_matchs.index(match) + 1} ("
                               f"{Color.YELLOW}G{Color.END}{Color.BOLD}/Gagné, "
                               f"{Color.YELLOW}P{Color.END}{Color.BOLD}/Perdu ou "
                               f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Nul) ? {Color.END}")
                if saisie not in ('G', 'P', 'N'):
                    print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                          f"{Color.END}{Color.SAUTLIGNE}")
                else:
                    saisie_correcte = True
            match.resultat(saisie)
    return


def modifier_elo(joueur, tb_joueurs):
    ans = '{:>3}'.format(date.today().year - date.fromisoformat(joueur['date_naissance']).year)
    print(f"{Color.SAUTLIGNE}  {joueur['prenom']} {joueur['nom']} {ans} ans "
          f"{Color.YELLOW}{joueur['elo']} elo{Color.END}{Color.SAUTLIGNE}")
    elo = saisie_elo()
    query_joueurs = Query()
    tb_joueurs.update({'elo': elo}, (query_joueurs.nom == joueur['nom']) & (query_joueurs.prenom == joueur['prenom'])
                      & (query_joueurs.date_naissance == joueur['date_naissance']))
    print(f"{Color.SAUTLIGNE}  {joueur['prenom']} {joueur['nom']} {ans} ans "
          f"{Color.YELLOW}{elo} elo{Color.END}{Color.SAUTLIGNE}")
