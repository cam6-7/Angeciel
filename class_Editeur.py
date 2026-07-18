from class_Joueur import Joueur
from class_Screen import Screen
from class_Bouton import Bouton, ListeBouton
from class_Niveau import Niveau
from class_Plateforme import Plateforme
from class_Ascensseur import Ascensseur
from fonction_texture import dessiner_plateforme_texturee
from class_Texte import Texte
from cp import *
from fonction_ressource_path import resource_path
from class_BoutonIMG import BoutonIMG
from class_Message import Message
import pygame
pygame.init()
clock = pygame.time.Clock()
fleche_d = pygame.image.load(resource_path("resources/flèche2.png"))
fleche_g = pygame.transform.flip(pygame.image.load(resource_path("resources/flèche2.png")), True, False)
class Editeur:

    def __init__(self ):
        self.camera = -200
        self.action = "rien"
        self.t = Texte(self.action, (500, 50))
        self.att = None
        self.souris1 = None
        self.type = "rien"
        self.decalage = 0
        self.boutons = [
            Bouton("Retour", [10, 50], couleur= WHITE),
            Bouton("Tester", [10, 100], couleur= WHITE),
            Bouton("Creer un \nnouveau niveau", [10, 200], couleur = WHITE, taille= 25),
            Bouton("paramettre\ndu niveau", [10, 300], couleur=WHITE),
            Bouton("créer une\nplateforme", [10, 400], couleur=WHITE),
            Bouton("créer un\nascensseur", [10, 500], couleur=WHITE),]

        self.boutons_n = []
        for i, n in enumerate(Niveau.liste):
            b = Bouton(n.name, (i * 150 + 300, 25), couleur="WHITE")
            self.boutons_n.append(b)
        self.boutons_n = ListeBouton(self.boutons_n)

        self.fleche_d = BoutonIMG(fleche_d, (Screen.largeur() - 75, 15))
        self.fleche_g = BoutonIMG(fleche_g, (200, 15))





    def afficher(self):
        #fond
        Screen.screen.fill(WHITE)
        self.draw_grid()

        #objets
        for plat in Niveau.actuel.plateformes:
            dessiner_plateforme_texturee(plat.rect.move(- self.camera, 0))
        for asc in Niveau.actuel.ascensseurs:
            asc.mouvement()
            dessiner_plateforme_texturee(asc.rect.move(- self.camera, 0))

        #boutons
        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, 200, Screen.hauteur()))
        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, Screen.largeur(), 75))

        for b in self.boutons:
            b.afficher()
        self.boutons_n.afficher(self.decalage)


        self.fleche_d.afficher()
        self.fleche_g.afficher()

        if self.fleche_g.est_clique():
            self.decalage -= 1
            if self.decalage < 0:
                self.decalage = 0
            else:
                self.boutons_n.decaler(-1)

        elif self.fleche_d.est_clique():
            self.decalage += 1
            if self.decalage > Niveau.nombre - 4:
                self.decalage = Niveau.nombre - 4
            else:
                self.boutons_n.decaler(1)


    def gestion_camera(self):
        Screen.camera -= Screen.camera % 25
        self.camera = Screen.camera - 200
        if self.action != "modifier":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                Screen.camera -= 25
            elif keys[pygame.K_RIGHT]:
                Screen.camera += 25
            if self.camera < -200:
                Screen.camera = 0
                self.camera = -200
            elif self.camera > Niveau.actuel.taille - Screen.hauteur():
                self.camera = Niveau.actuel.taille - Screen.hauteur()



    def gestion_bouton(self):
        if self.boutons[0].est_clique():
            self.fermer()
            Niveau.etat = "menu"
        elif self.boutons[1].est_clique():
            self.action = "test"
            Message("Cliquer là où vous voulez allez")
        elif self.boutons[2].est_clique():
            Plateforme.liste[Niveau.nombre + 1] = []
            Ascensseur.liste[Niveau.nombre + 1] = []
            Niveau(Plateforme.liste[Niveau.nombre + 1], Ascensseur.liste[Niveau.nombre + 1], 1000, [150, 150, 150])
            Niveau.changer(Niveau.nombre)
            self.boutons_n = []
            for i, n in enumerate(Niveau.liste):
                b = Bouton(n.name, (i * 150 + 300, 25), couleur="WHITE")
                self.boutons_n.append(b)
            self.boutons_n = ListeBouton(self.boutons_n)
            self.boutons_n.decaler(Niveau.nombre - 4)
            self.decalage = Niveau.nombre - 4
        elif self.boutons[3].est_clique():
            Niveau.etat = "paramettre"
        elif self.boutons[4].est_clique():
            self.type = "plat"
        elif self.boutons[5].est_clique():
            self.type = "asc"
        elif self.boutons_n.est_cliquer():
            Niveau.changer(self.boutons_n.boutons.index(self.boutons_n.bouton) + 1)
            self.fermer(1)


    def gestion_creation(self, events):
        for event in events:
            if pygame.mouse.get_pos()[0] > 200:
                if pygame.mouse.get_pressed()[0]:
                    if self.action == "rien":
                        self._clic_debut()
                    if self.action == "creer" and self.type != "rien":
                        self._clic_enfonce()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.action == "creer":
                    self._clic_relache()
        if self.action == "modifier":
            self._creation_asc(events)
        elif self.action == "test":
            self._gestion_test()


    def _clic_debut(self):

        self.souris1 = pygame.mouse.get_pos()
        sourisE = list(pygame.mouse.get_pos())
        sourisE[0] += self.camera

        clic = 0
        for obj in Niveau.actuel.objets:
            if obj.rect.collidepoint(sourisE):
                obj.supprimer()
                clic = 1
        if clic == 0 and self.type != "rien":
            self.att = Plateforme(0, 0, 0, 0, Niveau.en_cours)
            self.action = "creer"

    def _clic_enfonce(self):
        s1 = self.souris1
        s2 = pygame.mouse.get_pos()
        x1 = s1[0] + self.camera
        y1 = s1[1]
        x2 = s2[0] + self.camera
        y2 = s2[1]
        if x1 < x2:
            x1 = self.arrondir25(x1, "i")
            x2 = self.arrondir25(x2, "s")
            x = x1
        else:
            x1 = self.arrondir25(x1, "s")
            x2 = self.arrondir25(x2, "i")
            x = x2
        if y1 < y2:
            y1 = self.arrondir25(y1, "i")
            y2 = self.arrondir25(y2, "s")
            y = y1
        else:
            y1 = self.arrondir25(y1, "s")
            y2 = self.arrondir25(y2, "i")
            y = y2
        l = abs(x1 - x2)
        h = abs(y1 - y2)
        self.att.maj(x, y, l, h)

    def _clic_relache(self):
        r = self.att.rect
        if self.type == "plat":
            self.action = "rien"

        elif self.type == "asc":
            self.action = "modifier"
            self.att2 = self.att.copy()

    def _gestion_test(self):
        if pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 75:
            if pygame.mouse.get_pressed()[0]:
                souris = list(pygame.mouse.get_pos())
                souris[0] = self.arrondir25(souris[0], "i") + self.camera
                souris[1] = self.arrondir25(souris[1], "i")
                Niveau.etat = "test"
                Joueur.ply.rect.topleft = souris
                #Screen.camera = max(0, min(Joueur.ply.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))
                self.fermer(2)


    def _creation_asc(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.att2.rect.y -= 25
                    self.att2.rect.x =self.att.rect.x
                elif event.key == pygame.K_DOWN:
                    self.att2.rect.y += 25
                    self.att2.rect.x = self.att.rect.x
                elif event.key == pygame.K_LEFT:
                    self.att2.rect.x -= 25
                    self.att2.rect.y = self.att.rect.y
                elif event.key == pygame.K_RIGHT:
                    self.att2.rect.x += 25
                    self.att2.rect.y = self.att.rect.y
                elif event.key == pygame.K_RETURN:
                    Ascensseur(Niveau.en_cours, self.att.rect.size, self.att.rect.topleft, self.att2.rect.topleft)
                    self.att.supprimer()
                    self.att2.supprimer()
                    self.action = "rien"
                    self.type = "rien"




    def fermer(self, force = 0):
        self.action = "rien"
        self.type = "rien"
        self.att = None
        self.souris1 = None
        if force == 0:
            self.boutons_n.decaler(-self.decalage)
            self.decalage = 0
        if force <= 1:
            Screen.camera = -200

    @staticmethod
    def draw_grid(surface=Screen.screen, cell_size=25):
        w, h = surface.get_size()
        # lignes verticales
        for x in range(0, w, cell_size):
            pygame.draw.line(surface, BLACK, (x, 0), (x, h))
        # lignes horizontales
        for y in range(0, h, cell_size):
            pygame.draw.line(surface, BLACK, (0, y), (w, y))

    @staticmethod
    def arrondir25(nombre, cote):
        if cote == "i":
            nombre = nombre // 25 * 25
        elif cote == "s":
            nombre = nombre // 25 * 25 + 25
        return nombre