from operator import itemgetter
from datetime import date
from models.menu import Color
import models.config as tb


def chess_tournois():
    """Liste des tournois"""
    liste_tournois = tb.TOURNOIS.all()
    page = f"{Color.CYAN}\n-------- Liste des tournois d'échecs --------\n{Color.END}"
    if len(liste_tournois) == 0:
        page += f"\n  Aucun tournoi n'est enregistré"
    else:
        for tournoi in liste_tournois:
            page += f"\n  Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}"
    page += "\n"
    return page


def acteurs_tournois(ordre="elo"):
    """Liste des acteurs des tournois"""
    liste_acteurs = tb.JOUEURS.all()
    page = f"{Color.CYAN}\n-------- Liste des acteurs des tournois "
    if ordre == "elo":
        page += f"{Color.YELLOW}(ordre classement elo)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('elo', 'nom', 'prenom'), reverse=False)
    else:
        page += f"{Color.YELLOW}(ordre alphabétique)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('nom', 'prenom'), reverse=False)
    page += f"{Color.CYAN} --------\n{Color.END}"
    if len(liste_acteurs) == 0:
        page += f"\n  Aucun joueur n'est inscrit à un tournoi"
    else:
        for acteur in acteurs_tries:
            identite = '{:<15} {:<20}'.format(acteur['prenom'], acteur['nom'])
            ans = '{:>3}'.format(date.today().year - date.fromisoformat(acteur['date_naissance']).year)
            page += f"\n  {identite} {ans} ans {acteur['elo']} elo"
    page += "\n"
    return page
