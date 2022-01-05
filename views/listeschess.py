from operator import itemgetter
from views.viewschess import Color


def chess_tournois(tb_tournois):
    """Liste des tournois"""
    liste_tournois = tb_tournois.all()
    page = f"{Color.LIGNE}{Color.CYAN}-------- Liste des tournois d'échecs --------{Color.LIGNE}{Color.END}"
    if len(liste_tournois) == 0:
        page += f"{Color.LIGNE}  Aucun tournoi n'est enregistré{Color.LIGNE}"
    else:
        for tournoi in liste_tournois:
            page += f"{Color.LIGNE}  {Color.BOLD}Tournoi {tournoi['nom']} de {tournoi['lieu']} " \
                    f"du {tournoi['date_debut']}{Color.END}{Color.LIGNE}" \
                    f"  mode {tournoi['compteur_temps']} {tournoi['nb_tour']} tours - "\
                    f"Description : {tournoi['description']}{Color.LIGNE}"
    return page


def acteurs_tournois(tb_joueurs, ordre="elo"):
    """Liste des acteurs des tournois triés par ordre alphabétique ou classement elo"""
    liste_acteurs = tb_joueurs.all()
    page = f"{Color.LIGNE}{Color.CYAN}-------- Liste des acteurs des tournois "
    if ordre == "elo":
        page += f"{Color.YELLOW}(ordre classement elo)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('elo', 'nom', 'prenom'), reverse=False)
    else:
        page += f"{Color.YELLOW}(ordre alphabétique)"
        acteurs_tries = sorted(liste_acteurs, key=itemgetter('nom', 'prenom'), reverse=False)
    page += f"{Color.CYAN} --------{Color.END}{Color.LIGNE}"
    if len(liste_acteurs) == 0:
        page += f"{Color.LIGNE}  Aucun joueur n'est inscrit à un tournoi"
    else:
        for acteur in acteurs_tries:
            amj = acteur['date_naissance'].split('-')
            page += f"{Color.LIGNE}  {acteur['prenom'].ljust(15)[0:14]} {acteur['nom'].ljust(20)[0:19]}" \
                    f" né(e) le {amj[2]}-{amj[1]}-{amj[0]} ({acteur['sexe']}) {str(acteur['elo']).rjust(4)} elo"
            if len(acteur['nom']) > 20 or len(acteur['prenom']) > 15:
                page += f" {acteur['prenom']} {acteur['nom']}"
    page += Color.LIGNE
    return page
