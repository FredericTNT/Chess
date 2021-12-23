from operator import itemgetter
from datetime import date
from models.menu import Color
import models.config as tb


def chess_tournois():
    """Liste des tournois"""
    liste_tournois = tb.TOURNOIS.all()
    page = f"{Color.CYAN}\n-------- Liste des tournois d'échecs --------\n{Color.END}"
    if len(liste_tournois) == 0:
        page += f"\n  Aucun tournoi n'est enregistré\n"
    else:
        for tournoi in liste_tournois:
            page += f"\n  {Color.BOLD}Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}\n"\
                    f"  {Color.END}mode {tournoi['compteur_temps']} {tournoi['nb_tour']} tours - "\
                    f"Description : {tournoi['description']}\n"
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
            ans = '{:>3}'.format(date.today().year - date.fromisoformat(acteur['date_naissance']).year)
            page += f"\n  {acteur['prenom'].ljust(15)[0:14]} {acteur['nom'].ljust(20)[0:19]}" \
                    f" {ans} ans {acteur['elo']} elo"
            if len(acteur['nom']) > 20 or len(acteur['prenom']) > 15:
                page += f" {acteur['prenom']} {acteur['nom']}"
    page += "\n"
    return page
