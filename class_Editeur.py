from class_Screen import Screen
from class_Bouton import Bouton
from class_Niveau import Niveau
from class_Plateforme import Plateforme
from class_Ascensseur import Ascensseur
from fonction_texture import dessiner_plateforme_texturee
from class_Texte import Texte
from cp import *
import pygame
pygame.init()
clock = pygame.time.Clock()

class Editeur:

    def __init__(self ):
        self.camera = -200
        self.action = "rien"
        self.t = Texte(self.action, (500, 50))
        self.att = None
        self.souris1 = None
        self.type = "rien"
        self.boutons = [
    Bouton("Retour", [10, 50], couleur= WHITE),
    Bouton("Tester", [10, 100], couleur= WHITE),
    Bouton("changer de\nniveau", [10, 200], couleur=WHITE),
    Bouton("paramettre\ndu niveau", [10, 300], couleur=WHITE),
    Bouton("créer une\nplateforme", [10, 400], couleur=WHITE),
    Bouton("créer un\nascensseur", [10, 500], couleur=WHITE),
]



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

        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, 200, Screen.hauteur()))

        for b in self.boutons:
            b.afficher()

        #self.t.mise_a_jour(self.action + "      " + self.type)
        #self.t.afficher()


    def gestion_camera(self):
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
        etat = "editeur"
        if self.boutons[0].est_clique():
            self.fermer()
            etat = "menu"
        if self.boutons[1].est_clique():
            self.fermer()
            etat = "test"
        elif self.boutons[2].est_clique():
            etat = "choix_niv2"
        elif self.boutons[3].est_clique():
            etat = "paramettre"
        elif self.boutons[4].est_clique():
            self.type = "plat"
        elif self.boutons[5].est_clique():
            self.type = "asc"
        return etat

    def gestion_creation(self, events):
        for event in events:
            if pygame.mouse.get_pos()[0] > 200:
                if pygame.mouse.get_pressed()[0]:
                    if self.action == "rien":
                        self.souris1 = pygame.mouse.get_pos()
                        self._clic_debut()
                        self.att = Plateforme(0, 0, 0, 0, Niveau.en_cours)
                    if self.action == "creer" and self.type != "rien":
                        self._clic_enfonce()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.action == "creer":
                    self._clic_relache()
        if self.action == "modifier":
            self._creation_asc()


    def _clic_debut(self):
        clic = 0
        sourisE = list(pygame.mouse.get_pos())
        sourisE[0] += self.camera
        for plat in Niveau.actuel.plateformes:
            if plat.rect.collidepoint(sourisE):
                plat.supprimer()
                clic = 1
        for asc in Niveau.actuel.ascensseurs:
            if asc.rect.collidepoint(sourisE):
                asc.supprimer()
                clic = 1
        if clic == 0 and self.type != "rien":
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
        self.att.move(x, y, l, h)

    def _clic_relache(self):
        r = self.att.rect
        if self.type == "plat":
            self.att.copy()
            self.att.supprimer()
            self.action = "rien"
            self.type = "rien"

        elif self.type == "asc":
            self.action = "modifier"
            self.att2 = self.att.copy()



    def _creation_asc(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.att2.rect.y -= 5
            self.att2.rect.x =self.att.rect.x
        elif keys[pygame.K_DOWN]:
            self.att2.rect.y += 5
            self.att2.rect.x = self.att.rect.x
        elif keys[pygame.K_LEFT]:
            self.att2.rect.x -= 5
            self.att2.rect.y = self.att.rect.y
        elif keys[pygame.K_RIGHT]:
            self.att2.rect.x += 5
            self.att2.rect.y = self.att.rect.y

        elif keys[pygame.K_RETURN]:
            Ascensseur(Niveau.en_cours, self.att.rect.x, self.att.rect.size, (self.att.rect.y, self.att2.rect.y))
            self.att.supprimer()
            self.att2.supprimer()
            self.action = "rien"
            self.type = "rien"




    def fermer(self):
        Screen.camera = -200
        self.action = "rien"
        self.type = "rien"
        self.att = None
        self.souris1 = None

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