from controllers.menusequence import menu_general

"""
Paramètres généraux : 
 - nombre de joueurs (nombre pair pour un appairage correct des matchs)
 - nombre de tours (au maximum = à nombre de joueurs -1)
 - génération automatique des joueurs et des résultats des matchs (True/mode test, False/mode exploitation)
"""
NB_JOUEURS = 8
NB_TOURS = 4
AUTO = False

""" Programme principal tournoi d'échecs"""
if __name__ == '__main__':
    menu_general(NB_JOUEURS, NB_TOURS, AUTO)
