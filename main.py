from tinydb import TinyDB
from controllers.menusequence import menu_general

NB_JOUEURS = 8
NB_TOURS = 4


def main():
    """Initialisation TinyDB et lancement du menu général de l'application"""
    db = TinyDB('chess_db.json')
    joueurs_table = db.table('joueurs')
    tournois_table = db.table('tournois')
    tours_table = db.table('tours')
    matchs_table = db.table('matchs')
    menus_table = db.table('menus')
    menu_general(NB_JOUEURS, NB_TOURS, joueurs_table, tournois_table, tours_table, matchs_table, menus_table)


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
