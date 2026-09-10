import glob, json, os, sys, pygame
from  entities.class_Joueur import Joueur
from UI.class_Bouton import Bouton
from UI.class_Texte import Texte
from UI.class_TexteD import TexteD
from core.class_Screen import Screen
from core.class_Temps import Timer
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage
from entities.class_Plateforme import Plateforme
from scenes.class_Editeur import Editeur
from scenes.class_Menu import Menu
from scenes.class_Paramettre import Paramettre

# ==================== INITIALISATION DES OBJETS ====================
#les menus
menu1 = Menu([
            Texte("Bienvenue sur Angeciel",["x", 100], taille=70),
            Bouton("Commencer le jeu", ["x", 300], (0,0, 255)),
            Bouton("Choix du niveau", ["x", 400], (0, 255, 0)),
            Bouton("Quitter le jeu", ["x", 500], (255, 0, 0)),
            Bouton("éditeur de niveau", [20, 20], taille= 20)
            ])
menu_v = Menu([
            Texte(f"Vous avez fini le niveau {Niveau.en_cours}", ["x", 150], taille=70),
            Bouton("Niveau suivant", ["x", 310], (0, 0, 255)),
            Bouton(f"Refaire le niveau {Niveau.en_cours}", ["x", 400], (0, 255, 0)),
            Bouton("Quitter le jeu", ["x", 490], (255, 0, 0)),
            ])

# textes de tutoriels
aide1 = TexteD('Utilisez les\nflèches directionnelles\npour vous déplacer', [50, 425], taille = 20)
aide2 = TexteD("Appuyez sur espace\npour sauter", (500, 440), taille = 20)
aide3 = TexteD("Attention\nà ne pas tomber", (1200, 330), taille = 20)
aide4 = TexteD("Sautez\nIl n'y a aucun dégat de chute!", (3300, 50), taille = 20)
aide5 = TexteD("Bravo,\nvous avez fini le tutoriel,\nbonne chance pour\nla suite !", (4700, 150), taille = 20)


nb_nuage = 7
for i in range(nb_nuage):
    Nuage()

class Game:
    def __init__(self):
        self.events = []
        self.clock = pygame.time.Clock()
        self.joueur = Joueur()
        self.editeur = Editeur()
        self.paramettre = Paramettre()

        dossier = os.path.dirname(os.path.abspath(__file__))
        nombre_de_niveau = len(glob.glob(dossier + "/objets/plateforme*.json"))
        for niv in range(1, nombre_de_niveau + 1):
            Niveau()
            with open("objets/plateforme" + str(niv) + ".json", "r") as f:
                [Plateforme(plat["niveau"], plat["taille"], plat["positions"], plat["avance"]) for plat in json.load(f)]

    def run(self):

        self.get_events()
        self.display_menus()
        if Niveau.etat == "jeu" or Niveau.etat == "test":
            self.joueur.bouger()
            self.display_game()

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("\n " + str(pygame.mouse.get_pos()))
                print(pygame.mouse.get_pos()[0] + Screen.camera, pygame.mouse.get_pos()[1] + Screen.camera, "\n")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m and Niveau.etat == "editeur":
                Editeur.e.montrer_boutons = not Editeur.e.montrer_boutons

    def display_menus(self):
        if Niveau.etat == "menu":
            menu1.afficher()
            menu1.boutons[0].mise_a_jour(f"Commencer le niveau {Niveau.en_cours}")
            if menu1.boutons[1].est_clique():
                self.joueur.reinitialiser_jeu()
            if menu1.boutons[2].est_clique():
                Niveau.changer_etat("choix_niv")
            if menu1.boutons[3].est_clique():
                Niveau.changer_etat("close")
            if menu1.boutons[4].est_clique():
                Niveau.changer_etat("editeur")
                self.editeur.cam_x = -200
        elif Niveau.etat == "paramettre":
            self.paramettre.afficher()
            self.paramettre.gerer_clic()
        elif Niveau.etat == "editeur":
            self.editeur.gestion_camera()
            self.editeur.afficher()
            self.editeur.gestion_creation(self.events)
            self.editeur.gestion_bouton()
        elif Niveau.etat == "victoire":
            menu_v.boutons[0].mise_a_jour(f"Vous avez fini le niveau {Niveau.en_cours}")
            if Niveau.en_cours == Niveau.nombre:
                menu_v.boutons[1].mise_a_jour("Recommencer le jeu")
            else:
                menu_v.boutons[1].mise_a_jour("Niveau suivant")
            menu_v.boutons[2].mise_a_jour(f"Refaire le niveau {Niveau.en_cours}")
            menu_v.afficher()
            if menu_v.boutons[1].est_clique():
                Niveau.suivant()
                self.joueur.reinitialiser_jeu()
            if menu_v.boutons[2].est_clique():
                self.joueur.reinitialiser_jeu()
            if menu_v.boutons[3].est_clique():
                Niveau.changer_etat("close")

    def display_game(self):
        Screen.screen.fill(Niveau.actuel.couleur)

        # Nuages
        for pos in Nuage.liste:
            pos.afficher()

        # Plateformes et ascenseurs
        for obj in Niveau.actuel.plateformes:
            dessiner_plateforme_texturee(obj.rect.move(- Screen.camera, 0))

        # Joueur
        self.joueur.afficher()

        # Aides pour le niveau 1
        if Niveau.en_cours == 1:
            aide1.move(Screen.camera, self.joueur.rect_ecran)
            aide2.move(Screen.camera, self.joueur.rect_ecran)
            aide3.move(Screen.camera, self.joueur.rect_ecran)
            aide4.move(Screen.camera, self.joueur.rect_ecran)
            aide5.move(Screen.camera, self.joueur.rect_ecran)

    @staticmethod
    def save():
        # sauvergarde des objets quand le jeu est fini
        for niv in range(1, Niveau.nombre + 1):
            with open("objets/plateforme" + str(niv) + ".json", "w") as f:
                json.dump([plat.to_dict() for plat in Niveau.liste[niv - 1].plateformes], f, indent=4)

        print("fin sauvergardé")
        Screen.screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.quit()
        sys.exit()