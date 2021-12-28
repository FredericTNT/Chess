from models.menu import Color
from operator import attrgetter, itemgetter
from datetime import date


def matchs_tournoi(tournoi, liste_joueurs):
    """Liste des matchs d'un tournoi"""
    page = f"{Color.CYAN}\n-------- Liste des matchs du tournoi de {tournoi.lieu} --------\n{Color.END}"
    for tour in tournoi.liste_tours:
        page += f"\n  Tour {tour.numero} {Color.YELLOW}{tour.nom}{Color.END}"
        for match in tour.liste_matchs:
            joueur_blanc = '{:<15} {:<20}'.format(liste_joueurs[match.blanc[0]].prenom,
                                                  liste_joueurs[match.blanc[0]].nom)
            joueur_noir = '{:<15} {:<20}'.format(liste_joueurs[match.noir[0]].prenom,
                                                 liste_joueurs[match.noir[0]].nom)
            page += f"\n    {joueur_blanc} {liste_joueurs[match.blanc[0]].elo} elo " \
                    f"- Résultat [{match.blanc[1]}] {Color.YELLOW}vs{Color.END} " \
                    f"{joueur_noir} {liste_joueurs[match.noir[0]].elo} elo " \
                    f"- Résultat [{match.noir[1]}]"
        page += "\n"
    return page


def tours_tournoi(tournoi):
    """Liste des tours d'un tournoi"""
    page = f"{Color.CYAN}\n-------- Liste des tours du tournoi de {tournoi.lieu} --------\n{Color.END}"
    for tour in tournoi.liste_tours:
        page += f"\n  Tour {tour.numero} {Color.YELLOW}{tour.nom}{Color.END}" \
                f"\n  Tour lancé le {tour.date_heure_debut.isoformat(sep=' ', timespec='seconds')} "
        if not tour.date_heure_fin:
            page += f"en cours"
        else:
            page += f"et terminé le {tour.date_heure_fin.isoformat(sep=' ', timespec='seconds')}"
        page += "\n"
    return page


def joueurs_tournoi(liste_joueurs, lieu, ordre="elo"):
    """Liste des joueurs d'un tournoi"""
    page = f"{Color.CYAN}\n-------- Liste des joueurs du tournoi de {lieu} "
    if ordre == "elo":
        page += f"{Color.YELLOW}(ordre classement elo)"
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('elo', 'nom', 'prenom'), reverse=False)
    else:
        page += f"{Color.YELLOW}(ordre alphabétique)"
        joueurs_tries = sorted(liste_joueurs, key=attrgetter('nom', 'prenom'), reverse=False)
    page += f"{Color.CYAN} --------\n{Color.END}"
    for joueur in joueurs_tries:
        ans = '{:>3}'.format(date.today().year - joueur.date_naissance.year)
        page += f"\n  {joueur.prenom.ljust(15)[0:14]} {joueur.nom.ljust(20)[0:19]} {ans} ans {joueur.elo} elo"
        if len(joueur.nom) > 20 or len(joueur.prenom) > 15:
            page += f" {joueur.prenom} {joueur.nom}"
    page += "\n"
    return page


def resultats_tournoi(tournoi, liste_joueurs):
    """Affichage des résultats du tournoi par ordre décroissant des points"""
    page = f"{Color.CYAN}\n-------- Résutats du tournoi de {tournoi.lieu} --------\n{Color.END}"
    resultats = sorted(tournoi.somme_points().items(), key=itemgetter(1), reverse=True)
    rang = 1
    for joueur in resultats:
        page += f"\n  {Color.CYAN}{rang} - {Color.END}" \
                f"{joueur[1]} point tournoi {liste_joueurs[joueur[0]].prenom} {liste_joueurs[joueur[0]].nom}"
        rang += 1
    page += "\n"
    return page
