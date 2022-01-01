from operator import itemgetter
from datetime import date
from views.chessinput import Color


def chess_tournois(tb_tournois):
    """Liste des tournois"""
    liste_tournois = tb_tournois.all()
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Liste des tournois d'échecs --------{Color.SAUTLIGNE}{Color.END}"
    if len(liste_tournois) == 0:
        page += f"{Color.SAUTLIGNE}  Aucun tournoi n'est enregistré{Color.SAUTLIGNE}"
    else:
        for tournoi in liste_tournois:
            page += f"{Color.SAUTLIGNE}  {Color.BOLD}Tournoi {tournoi['nom']} de {tournoi['lieu']} " \
                    f"du {tournoi['date_debut']}"\
                    f"{Color.SAUTLIGNE}  {Color.END}mode {tournoi['compteur_temps']} {tournoi['nb_tour']} tours - "\
                    f"Description : {tournoi['description']}{Color.SAUTLIGNE}"
    return page


def acteurs_tournois(tb_joueurs, ordre="elo"):
    """Liste des acteurs des tournois"""
    liste_acteurs = tb_joueurs.all()
    page = f"{Color.SAUTLIGNE}{Color.CYAN}-------- Liste des acteurs des tournois "
    if ordre == "elo":
        page += f"{Color.YELLOW}(ordre classement elo)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('elo', 'nom', 'prenom'), reverse=False)
    else:
        page += f"{Color.YELLOW}(ordre alphabétique)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('nom', 'prenom'), reverse=False)
    page += f"{Color.CYAN} --------{Color.END}{Color.SAUTLIGNE}"
    if len(liste_acteurs) == 0:
        page += f"{Color.SAUTLIGNE}  Aucun joueur n'est inscrit à un tournoi"
    else:
        for acteur in acteurs_tries:
            ans = '{:>3}'.format(date.today().year - date.fromisoformat(acteur['date_naissance']).year)
            page += f"{Color.SAUTLIGNE}  {acteur['prenom'].ljust(15)[0:14]} {acteur['nom'].ljust(20)[0:19]}" \
                    f" {ans} ans {str(acteur['elo']).rjust(4)} elo"
            if len(acteur['nom']) > 20 or len(acteur['prenom']) > 15:
                page += f" {acteur['prenom']} {acteur['nom']}"
    page += Color.SAUTLIGNE
    return page
