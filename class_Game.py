import glob, json, os, sys, pygame

from UI.class_Message import Message
from  entities.class_Joueur import Joueur
from core.class_Screen import Screen
from core.class_Temps import Timer
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage
from entities.class_Plateforme import Plateforme
from scenes.class_Editeur import Editeur
from scenes.class_GameSession import GameSession
from scenes.class_LevelParametersMenu import LevelParametersMenu
from scenes.class_MainMenu import MainMenu
from scenes.class_VictoryMenu import VictoryMenu

nb_nuage = 7
for i in range(nb_nuage):
    Nuage()

class Game:
    def __init__(self):
        self.events = []
        self.clock = pygame.time.Clock()

        self.joueur = Joueur()
        self.editeur = Editeur()
        self.paramettre = LevelParametersMenu()
        self.game_session = GameSession()
        self.main_menu = MainMenu()
        self.victoy_menu = VictoryMenu()

        self.dossier = os.path.dirname(os.path.abspath(__file__))
        self.nombre_de_niveau = len(glob.glob(self.dossier + "/objets/plateforme*.json"))
        for niv in range(1, self.nombre_de_niveau + 1):
            Niveau()
            with open("objets/plateforme" + str(niv) + ".json", "r") as f:
                [Plateforme(niv , plat["taille"], plat["positions"], plat["avance"]) for plat in json.load(f)]

    def run(self):

        self.get_events()
        self.display_menus()

        Timer.mise_a_jour()
        pygame.display.flip()
        self.clock.tick(60)

    def get_events(self):
        self.events = []
        for event in pygame.event.get():
            self.events.append(event)
            if event.type == pygame.QUIT:
                Niveau.changer_etat("close")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                liste_etat = {"menu": "menu",
                              "jeu": "menu",
                              "editeur": "menu",
                              "paramettre": "editeur",
                              "test": "editeur",
                              "victoire": "victoire",
                              }
                Niveau.changer_etat(liste_etat[Niveau.etat])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Message("\n" + str(pygame.mouse.get_pos()))
                    Message(str(pygame.mouse.get_pos()[0] + Screen.camera) +", " + str(pygame.mouse.get_pos()[1]) + "\n")


    def display_menus(self):
        if Niveau.etat == "menu":
            new_editeur = self.main_menu.run(self.joueur)
            if new_editeur: self.editeur = Editeur()
        elif Niveau.etat == "paramettre":
            self.paramettre.run()
        elif Niveau.etat == "editeur":
            self.editeur.run(self.events)
        elif Niveau.etat == "victoire":
            self.victoy_menu.run(self.joueur)
        elif Niveau.etat == "jeu" or Niveau.etat == "test":
            self.game_session.run(self.joueur)


    def save(self):
        # sauvergarde des objets quand le jeu est fini
        for niv in range(1, Niveau.nombre + 1):
            with open("objets/plateforme" + str(niv) + ".json", "w") as f:
                json.dump([plat.to_dict() for plat in Niveau.liste[niv - 1].plateformes], f, indent=4)
        for niv in range(Niveau.nombre + 1, self.nombre_de_niveau + 1):
            os.remove(self.dossier + "/objets/plateforme" + str(niv) + ".json")

        print("fin sauvergardé")
        Screen.screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.quit()
        sys.exit()