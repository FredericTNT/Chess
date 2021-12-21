from datetime import date
import random
from models.joueur import Joueur
from models.tournoi import Tournoi
from models.menu import Color
import models.config as tb


def saisie_tournoi(nb_tours):
    print(f"{Color.GREEN}\n-------- Enregistrement du tournoi --------{Color.END}")
    confirme = False
    while not confirme:
        nom = input(f"\n{Color.BOLD}  Nom du tournoi ? {Color.END}")
        lieu = input(f"{Color.BOLD}  Lieu du tournoi ? {Color.END}")
        temps = input(f"{Color.BOLD}  Mode de contrôle du temps ({Color.END}"
                      f"{Color.YELLOW}B{Color.END}{Color.BOLD}/Bullet, "
                      f"{Color.YELLOW}Z{Color.END}{Color.BOLD}/Blitz ou "
                      f"{Color.YELLOW}R{Color.END}{Color.BOLD}/Coup Rapide) ? {Color.END}")
        while temps not in ('B', 'Z', 'R'):
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                  f"{Color.END}{Color.SAUTLIGNE}")
            temps = input(f"{Color.BOLD}  Mode de contrôle du temps ({Color.END}"
                          f"{Color.YELLOW}B{Color.END}{Color.BOLD}/Bullet, "
                          f"{Color.YELLOW}Z{Color.END}{Color.BOLD}/Blitz ou "
                          f"{Color.YELLOW}R{Color.END}{Color.BOLD}/Coup Rapide) ? {Color.END}")
        if temps == 'B':
            compteur_temps = 'Bullet'
        elif temps == 'Z':
            compteur_temps = 'Blitz'
        else:
            compteur_temps = 'Coup rapide'
        description = input(f"{Color.BOLD}  Commentaires du directeur du tournoi ? {Color.END}")
        print("")
        choix = input(f"{Color.BOLD}  Confirmez-vous la saisie ({Color.END}"
                      f"{Color.YELLOW}O{Color.END}{Color.BOLD}/Oui, "
                      f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Non) ? {Color.END}")
        while choix not in ('O', 'N'):
            print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                  f"{Color.END}{Color.SAUTLIGNE}")
            choix = input(f"{Color.BOLD}  Confirmez-vous la saisie ({Color.END}"
                          f"{Color.YELLOW}O{Color.END}{Color.BOLD}/Oui, "
                          f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Non) ? {Color.END}")
        confirme = (choix == 'O')
    tournoi = Tournoi(nom, lieu, date.today(),
                      nb_tour=nb_tours, compteur_temps=compteur_temps, description=description)
    return tournoi


def select_tournoi():
    liste_tournois = tb.TOURNOIS.all()
    if len(liste_tournois) == 0:
        return None
    print(f"{Color.GREEN}\n-------- Sélection d'un tournoi --------{Color.END}\n")
    for tournoi in liste_tournois:
        print(f"{Color.YELLOW}  {liste_tournois.index(tournoi) + 1}.  {Color.END}"
              f"Tournoi {tournoi['nom']} de {tournoi['lieu']} du {tournoi['date_debut']}")
    print()
    choix = input(Color.BOLD + "  Votre choix ? " + Color.END)
    try:
        indice = int(choix) - 1
    except ValueError:
        indice = -1
    while indice not in range(0, len(liste_tournois)):
        print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
              f"{Color.END}{Color.SAUTLIGNE}")
        choix = input(Color.BOLD + "  Votre choix ? " + Color.END)
        try:
            indice = int(choix) - 1
        except ValueError:
            indice = -1
    clef_tournoi = liste_tournois[indice]['nom'] + liste_tournois[indice]['lieu'] + liste_tournois[indice]['date_debut']
    return clef_tournoi


def joueurs_inscrits(nb_joueurs, tournoi, auto=False):
    liste_joueurs = []
    if auto:
        for i in range(0, nb_joueurs):
            joueur = Joueur(f"TNT{tournoi.lieu}", f'Joueur{i}', date(2000, 7, 22), "M",
                            random.randrange(1000, 1800, 100))
            liste_joueurs.append(joueur)
            tournoi.clefs_joueurs.append(joueur.nom + joueur.prenom + date.isoformat(joueur.date_naissance))
    else:
        pass
    return liste_joueurs


def saisie_resultats(tour, liste_joueurs, nb_match, auto=False):
    if auto:
        for i in range(0, nb_match):
            tour.liste_matchs[i].resultat(random.choice(['G', 'P', 'N']))
    else:
        print(f"{Color.GREEN}\n-------- Saisie des résultats des matchs du tour {tour.numero} --------{Color.END}")
        for match in tour.liste_matchs:
            joueur_blanc = '{:<15} {:<20}'.format(liste_joueurs[match.blanc[0]].prenom,
                                                  liste_joueurs[match.blanc[0]].nom)
            joueur_noir = '{:<15} {:<20}'.format(liste_joueurs[match.noir[0]].prenom,
                                                 liste_joueurs[match.noir[0]].nom)
            print(f"\n    {joueur_blanc} {liste_joueurs[match.blanc[0]].elo} elo {Color.YELLOW}vs{Color.END} "
                  f"{joueur_noir} {liste_joueurs[match.noir[0]].elo} elo \n")
            saisie = input(f"{Color.BOLD}  Résultat du match {tour.liste_matchs.index(match) + 1} ("
                           f"{Color.YELLOW}G{Color.END}{Color.BOLD}/Gagné, "
                           f"{Color.YELLOW}P{Color.END}{Color.BOLD}/Perdu ou "
                           f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Nul) ? {Color.END}")
            while saisie not in ('G', 'P', 'N'):
                print(f"{Color.SAUTLIGNE}{Color.YELLOW}  Désolé! Votre choix ne correspond à aucune option valide"
                      f"{Color.END}{Color.SAUTLIGNE}")
                saisie = input(f"{Color.BOLD}  Résultat du match {tour.liste_matchs.index(match) + 1} ("
                               f"{Color.YELLOW}G{Color.END}{Color.BOLD}/Gagné, "
                               f"{Color.YELLOW}P{Color.END}{Color.BOLD}/Perdu ou "
                               f"{Color.YELLOW}N{Color.END}{Color.BOLD}/Nul) ? {Color.END}")
            match.resultat(saisie)
    return
