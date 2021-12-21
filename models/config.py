from tinydb import TinyDB

db = TinyDB('chess_db.json')
JOUEURS = db.table('joueurs')
TOURNOIS = db.table('tournois')
TOURS = db.table('tours')
MATCHS = db.table('matchs')
CLEFSJOUEURS = db.table('clefsjoueurs')
MENUS = db.table('menus')
