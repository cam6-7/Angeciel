from UI.class_Debug import Debug
from entities.class_Joueur import Joueur
from core.class_Screen import Screen
from UI.class_Bouton import Bouton
from entities.class_Niveau import Niveau
from entities.class_Plateforme import Plateforme
from core.fonction_texture import dessiner_plateforme_texturee
from core.fonction_ressource_path import resource_path
from UI.class_BoutonIMG import BoutonIMG
from UI.class_Message import Message
import pygame

image_d = pygame.image.load(resource_path("resources/flèche2.png"))
image_g = pygame.transform.flip(pygame.image.load(resource_path("resources/flèche2.png")), True, False)


class Editeur:
    def __init__(self, decalage: int = 0):
        self.action = "rien"
        self.type = "rien"
        self.att : Plateforme = None
        self.souris1 = None
        self.decalage = decalage
        self.fleche_d = BoutonIMG(image_d, (Screen.largeur() - 75, 15))
        self.fleche_g = BoutonIMG(image_g, (200, 15))
        self.boutons = [
            Bouton("Retour", [10, 50], (255, 255, 255)),
            Bouton("Tester", [10, 100], (255, 255, 255)),
            Bouton("Creer un \nnouveau niveau", [10, 200], (255, 255, 255), taille= 25),
            Bouton("paramettre\ndu niveau", [10, 275], (255, 255, 255)),
            Bouton("créer une\nplateforme", [10, 400], (255, 255, 255)),
            Bouton("créer un\nascensseur", [10, 475], (255, 255, 255))]
        self.boutons_n = [Bouton(niv.name, (0, 0), (255, 255, 255)) for niv in Niveau.liste]
        self.listespos = []
        Screen.camera = -200


    def afficher(self):
        #fond
        Screen.screen.fill((255, 255, 255))
        self.draw_grid()

        #objets
        for plat in Niveau.actuel.plateformes:
            plat.mouvement()
            dessiner_plateforme_texturee(plat.rect.move(- Screen.camera, 0))

        #boutons
        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, 200, Screen.hauteur()))
        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, Screen.largeur(), 75))

        for b in self.boutons:
            b.afficher()
        pos = [250, 30]
        for i, b in enumerate(self.boutons_n):
            pos[0] += 50
            b.mise_a_jour(nouvelle_pos=pos)
            if i < self.decalage:
                b.mise_a_jour(nouvelle_pos=(Screen.largeur(), Screen.hauteur()))
                pos = [250, 30]
            elif i == self.decalage or b.rect.right < Screen.largeur() - 100:
                b.mise_a_jour(nouvelle_pos=pos)
                b.afficher()
                pos = list(b.rect.topright)
            else:
                b.mise_a_jour(nouvelle_pos=(Screen.largeur(), Screen.hauteur()))
                pos = [Screen.largeur(), Screen.hauteur()]


        self.fleche_d.mise_a_jour(nouvelle_pos=(Screen.largeur() - 75, 15))
        self.fleche_g.afficher()
        self.fleche_d.afficher()
    def maj_boutons(self):
        if len(self.boutons_n) != Niveau.nombre:
            self.boutons_n = [Bouton(niv.name, (0, 30), (255, 255, 255)) for niv in Niveau.liste]

    def gestion_camera(self):
        Screen.camera -= Screen.camera % 25
        if self.action != "modifier":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                Screen.camera -= 25
            elif keys[pygame.K_RIGHT]:
                Screen.camera += 25
            if Screen.camera < -200:
                Screen.camera = -200
            elif Screen.camera > Niveau.actuel.taille - Screen.largeur() // 2 - 100:
                Screen.camera = Niveau.actuel.taille - Screen.largeur() // 2 - 100



    def gestion_bouton(self):
        if self.boutons[0].est_clique():
            liste_etat = {"menu" : "menu",
                          "jeu" : "menu",
                          "editeur" : "menu",
                          "paramettre" : "editeur",
                          "victoire" : "victoire",
                          }
            Niveau.changer_etat(liste_etat[Niveau.etat])
        elif self.boutons[1].est_clique():
            self.action = "test"
        elif self.boutons[2].est_clique():
            Niveau()
            Niveau.changer(Niveau.nombre)
            self.decalage = Niveau.nombre - 1

        elif self.boutons[3].est_clique():
            Niveau.changer_etat("paramettre")
        elif self.boutons[4].est_clique():
            self.type = "plat"
        elif self.boutons[5].est_clique():
            self.type = "asc"
        if self.fleche_g.est_clique():
            self.decalage -= 1
        elif self.fleche_d.est_clique():
            self.decalage += 1
        try:
            if self.boutons_n[-1].rect.right + self.boutons_n[self.decalage - 1].rect.width < Screen.largeur() - 100: self.decalage -= 1
        except IndexError:
            pass
        if self.decalage < 0: self.decalage = 0
        self.maj_boutons()
        for b in self.boutons_n:
            if b.est_clique():
                Niveau.changer(self.boutons_n.index(b) + 1)

    def gestion_click(self, events):
        for event in events:
            if pygame.mouse.get_pos()[0] > 200:
                if pygame.mouse.get_pressed()[0]:
                    if self.action == "rien":
                        self.souris1 = pygame.mouse.get_pos()
                        clic = False
                        for obj in Niveau.actuel.plateformes:
                            if obj.rect.collidepoint((self.souris1[0] + Screen.camera, self.souris1[1])):
                                obj.supprimer()
                                clic = True
                        if not clic and self.type != "rien":
                            self.att = Plateforme(Niveau.en_cours, (0, 0), [(0, 0)])
                            self.action = "creer"
                    if self.action == "creer" and self.type != "rien":
                        s1 = self.souris1
                        s2 = pygame.mouse.get_pos()
                        x1 = self.arrondir25(min(s1[0] + Screen.camera, s2[0] + Screen.camera), "i")
                        x2 = self.arrondir25(max(s1[0] + Screen.camera, s2[0] + Screen.camera), "s")
                        y1 = self.arrondir25(min(s1[1], s2[1]), "i")
                        y2 = self.arrondir25(max(s1[1], s2[1]), "s")
                        self.att = self.att.maj(x1, y1, x2 - x1, y2 - y1)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.action == "creer":
                    if self.type == "plat":
                        self.action = "rien"
                    elif self.type == "asc":
                        self.action = "modifier"
                        self.listespos.append(self.att.rect.topleft)
        if self.action == "modifier":
            for pos in self.listespos:
                dessiner_plateforme_texturee(pygame.Rect(pos[0] - Screen.camera, pos[1], *self.att.taille))
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.att.rect.y -= 25
                        self.att.rect.x = self.listespos[-1][0]
                    elif event.key == pygame.K_DOWN:
                        self.att.rect.y += 25
                        self.att.rect.x = self.listespos[-1][0]
                    elif event.key == pygame.K_LEFT:
                        self.att.rect.x -= 25
                        self.att.rect.y = self.listespos[-1][1]
                    elif event.key == pygame.K_RIGHT:
                        self.att.rect.x += 25
                        self.att.rect.y = self.listespos[-1][1]
                    elif event.key == pygame.K_RETURN:
                        if self.att.rect.topleft == self.listespos[-1]:
                            Plateforme(Niveau.en_cours, self.att.rect.size, self.listespos)
                            self.att.supprimer()
                            self.listespos.clear()
                            self.action = "rien"
                            self.type = "rien"
                        else:
                            self.listespos.append(self.att.rect.topleft)
        elif self.action == "test":
            if pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 75:
                if pygame.mouse.get_pressed()[0]:
                    self.action = "rien"
                    souris = list(pygame.mouse.get_pos())
                    souris[0] = self.arrondir25(souris[0], "i") + Screen.camera
                    souris[1] = self.arrondir25(souris[1], "i")
                    Niveau.changer_etat("test")
                    Joueur.ply.rect.topleft = souris
                    Joueur.ply.postest = souris
                    Screen.camera = max(0, min(Joueur.ply.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))

    @staticmethod
    def draw_grid(surface=Screen.screen, cell_size=25):
        w, h = surface.get_size()
        # lignes verticales
        for x in range(0, w, cell_size):
            pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, h))
        # lignes horizontales
        for y in range(0, h, cell_size):
            pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))

    @staticmethod
    def arrondir25(nombre, cote):
        if cote == "i":
            nombre = nombre // 25 * 25
        elif cote == "s":
            nombre = nombre // 25 * 25 + 25
        return nombre