from tinydb import TinyDB
from controllers.menusequence import menu_general

NB_JOUEURS = 8
NB_TOURS = 4


def main():
    db = TinyDB('chess_db.json')
    joueurs_table = db.table('joueurs')
    tournois_table = db.table('tournois')
    tours_table = db.table('tours')
    matchs_table = db.table('matchs')
    menu_general(NB_JOUEURS, NB_TOURS, joueurs_table, tournois_table, tours_table, matchs_table)


# Programme principal tournoi d'échecs
if __name__ == '__main__':
    main()
