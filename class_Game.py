import pygame
from  entities.class_Joueur import Joueur
from UI.class_Bouton import Bouton
from UI.class_Texte import Texte
from UI.class_TexteD import TexteD
from core.class_Screen import Screen
from core.class_Temps import Timer
from core.fonction_ressource_path import resource_path
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage
from scenes.class_Editeur import Editeur
from scenes.class_Menu import Menu
from scenes.class_Paramettre import Paramettre


clock = pygame.time.Clock()
ply = Joueur()
editeur = Editeur()
paramettre = Paramettre()
# ==================== SON ====================
m_menu = pygame.mixer.Sound(resource_path("resources/menu.mp3"))
m_jeu = pygame.mixer.Sound(resource_path("resources/jeu.mp3"))
m_jeu.set_volume(0.2)
m_menu.set_volume(0.4)
m_menu.play(-1)

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
menu_c = Menu([
            Bouton("retour", ["x", 50] ),
            Bouton("niveau1", [1000/3, 200], centre = "spe" ),
            Bouton("niveau2", [1000/3 * 2, 200], centre = "spe"),
            Bouton("niveau3", [1000/3, 400], centre = "spe"),
            Bouton("niveau4", [1000/3 * 2, 400], centre = "spe")
            ])


# textes de tutoriels
aide1 = TexteD('Utilisez les\nflèches directionnelles\npour vous déplacer', [50, 425], taille = 20)
aide2 = TexteD("Appuyez sur espace\npour sauter", (500, 440), taille = 20)
aide3 = TexteD("Attention\nà ne pas tomber", (1200, 330), taille = 20)
aide4 = TexteD("Sautez\nIl n'y a aucun dégat de chute!", (3300, 50), taille = 20)
aide5 = TexteD("Bravo,\nvous avez fini le tutoriel,\nbonne chance pour\nla suite !", (4700, 150), taille = 20)


class Game:
    def run(self):
        events = []
        for event in pygame.event.get():
            events.append(event)
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

        # ==================== MENUS ====================
        if Niveau.etat == "menu":
            menu1.afficher()
            menu1.boutons[0].mise_a_jour(f"Commencer le niveau {Niveau.en_cours}")
            if menu1.boutons[1].est_clique():
                ply.reinitialiser_jeu()
            if menu1.boutons[2].est_clique():
                Niveau.changer_etat("choix_niv")
            if menu1.boutons[3].est_clique():
                Niveau.changer_etat("close")
            if menu1.boutons[4].est_clique():
                Niveau.changer_etat("editeur")
                editeur.cam_x = -200
                e_type = "rien"

        if Niveau.etat == "choix_niv":
            menu_c.afficher()
            if menu_c.boutons[0].est_clique():
                Niveau.changer_etat("menu")
            for bouton in menu_c.boutons:
                if bouton.est_clique():
                    Niveau.changer(menu_c.boutons.index(bouton))
                    ply.reinitialiser_jeu()

        if Niveau.etat == "paramettre":
            paramettre.afficher()
            paramettre.gerer_clic()

        # ==================== EDITEUR =====================
        if Niveau.etat == "editeur":
            editeur.gestion_camera()
            editeur.afficher()
            editeur.gestion_creation(events)
            editeur.gestion_bouton()

        # ==================== VICTOIRE ====================
        if Niveau.etat == "victoire":
            menu_v.boutons[0].mise_a_jour(f"Vous avez fini le niveau {Niveau.en_cours}")
            if Niveau.en_cours == Niveau.nombre:
                menu_v.boutons[1].mise_a_jour("Recommencer le jeu")
            else:
                menu_v.boutons[1].mise_a_jour("Niveau suivant")
            menu_v.boutons[2].mise_a_jour(f"Refaire le niveau {Niveau.en_cours}")
            menu_v.afficher()
            if menu_v.boutons[1].est_clique():
                Niveau.suivant()
                ply.reinitialiser_jeu()
            if menu_v.boutons[2].est_clique():
                ply.reinitialiser_jeu()
            if menu_v.boutons[3].est_clique():
                Niveau.changer_etat("close")


        # ==================== JEU =================================================================
        elif Niveau.etat == "jeu" or Niveau.etat == "test":

            # ==================== COLLISIONS + MOUVEMENTS ====================
            ply.bouger()

            # ==================== AFFICHAGE ==================================================================================
            Screen.screen.fill(Niveau.actuel.couleur)

            # Nuages
            for pos in Nuage.liste:
                pos.afficher()

            # Plateformes et ascenseurs
            for obj in Niveau.actuel.objets:
                dessiner_plateforme_texturee(obj.rect.move(- Screen.camera, 0))

                # Joueur
                ply.afficher()

            # Aides pour le niveau 1
            if Niveau.en_cours == 1:
                aide1.move(Screen.camera, ply.rect_ecran)
                aide2.move(Screen.camera, ply.rect_ecran)
                aide3.move(Screen.camera, ply.rect_ecran)
                aide4.move(Screen.camera, ply.rect_ecran)
                aide5.move(Screen.camera, ply.rect_ecran)

        Timer.mise_a_jour()
        pygame.display.flip()
        clock.tick(60)