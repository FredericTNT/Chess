from operator import attrgetter, itemgetter
from datetime import date
from views.chessinput import Color


def matchs_tournoi(tournoi, liste_joueurs):
    """Liste des matchs d'un tournoi"""
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Liste des matchs du tournoi de {tournoi.lieu} " \
           f"--------{Color.END}{Color.SAUTLIGNE}"
    for tour in tournoi.liste_tours:
        page += f"{Color.SAUTLIGNE}  Tour {tour.numero} {Color.YELLOW}{tour.nom}{Color.END}"
        for match in tour.liste_matchs:
            joueur_blanc = f'{liste_joueurs[match.blanc[0]].prenom.ljust(15)[0:14]} ' \
                           f'{liste_joueurs[match.blanc[0]].nom.ljust(20)[0:19]}'
            joueur_noir = f'{liste_joueurs[match.noir[0]].prenom.ljust(15)[0:14]} ' \
                          f'{liste_joueurs[match.noir[0]].nom.ljust(20)[0:19]}'
            page += f"{Color.SAUTLIGNE}    {joueur_blanc} {str(liste_joueurs[match.blanc[0]].elo).rjust(4)} elo " \
                    f"- Résultat [{match.blanc[1]}] {Color.YELLOW}vs{Color.END} " \
                    f"{joueur_noir} {str(liste_joueurs[match.noir[0]].elo).rjust(4)} elo " \
                    f"- Résultat [{match.noir[1]}]"
        page += Color.SAUTLIGNE
    return page


def tours_tournoi(tournoi):
    """Liste des tours d'un tournoi"""
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Liste des tours du tournoi de {tournoi.lieu} " \
           f"--------{Color.END}{Color.SAUTLIGNE}"
    for tour in tournoi.liste_tours:
        page += f"{Color.SAUTLIGNE}  Tour {tour.numero} {Color.YELLOW}{tour.nom}{Color.END}" \
                f"{Color.SAUTLIGNE}  Tour lancé le {tour.date_heure_debut.isoformat(sep=' ', timespec='seconds')} "
        if not tour.date_heure_fin:
            page += f"en cours"
        else:
            page += f"et terminé le {tour.date_heure_fin.isoformat(sep=' ', timespec='seconds')}"
        page += Color.SAUTLIGNE
    return page


def joueurs_tournoi(liste_joueurs, lieu, ordre="elo"):
    """Liste des joueurs d'un tournoi"""
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Liste des joueurs du tournoi de {lieu} "
    if ordre == "elo":
        page += f"{Color.YELLOW}(ordre classement elo)"
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('elo', 'nom', 'prenom'), reverse=False)
    else:
        page += f"{Color.YELLOW}(ordre alphabétique)"
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('nom', 'prenom'), reverse=False)
    page += f"{Color.CYAN} --------{Color.END}{Color.SAUTLIGNE}"
    for joueur in joueurs_tries:
        ans = '{:>3}'.format(date.today().year - joueur.date_naissance.year)
        page += f"{Color.SAUTLIGNE}  {joueur.prenom.ljust(15)[0:14]} {joueur.nom.ljust(20)[0:19]} {ans} ans " \
                f"{str(joueur.elo).rjust(4)} elo"
        if len(joueur.nom) > 20 or len(joueur.prenom) > 15:
            page += f" {joueur.prenom} {joueur.nom}"
    page += Color.SAUTLIGNE
    return page


def resultats_tournoi(tournoi, liste_joueurs):
    """Affichage des résultats du tournoi par ordre décroissant des points"""
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Résutats du tournoi de {tournoi.lieu} " \
           f"--------{Color.END}{Color.SAUTLIGNE}"
    resultats = sorted(tournoi.somme_points().items(), key=itemgetter(1), reverse=True)
    rang = 1
    for joueur in resultats:
        page += f"{Color.SAUTLIGNE}  {Color.CYAN}{rang} - {Color.END}" \
                f"{joueur[1]} point tournoi {liste_joueurs[joueur[0]].prenom} {liste_joueurs[joueur[0]].nom}"
        rang += 1
    page += Color.SAUTLIGNE
    return page
