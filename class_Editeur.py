from class_Joueur import Joueur
from class_Screen import Screen
from class_Bouton import Bouton, ListeBouton
from class_Niveau import Niveau
from class_Plateforme import Plateforme
from fonction_texture import dessiner_plateforme_texturee
from class_Texte import Texte
from cp import couleurs as c
from fonction_ressource_path import resource_path
from class_BoutonIMG import BoutonIMG
from class_Message import Message
import pygame
pygame.init()
clock = pygame.time.Clock()
class Editeur:

    e = None
    def __init__(self ):
        self.camera = -200
        self.action = "rien"
        self.t = Texte(self.action, (500, 50))
        self.att = None
        self.souris1 = None
        self.type = "rien"
        self.decalage = 0
        self.montrer_boutons = True
        self.boutons = [
            Bouton("Retour", [10, 50], couleur= c["WHITE"]),
            Bouton("Tester", [10, 100], couleur= c["WHITE"]),
            Bouton("Creer un \nnouveau niveau", [10, 200], couleur = c["WHITE"], taille= 25),
            Bouton("paramettre\ndu niveau", [10, 275], couleur=c["WHITE"]),
            Bouton("créer une\nplateforme", [10, 400], couleur=c["WHITE"]),
            Bouton("créer un\nascensseur", [10, 475], couleur=c["WHITE"]),]
        self.decalage = 0
        self.recreation_bouton()
        self.listespos = []
        Editeur.e = self

    def afficher_fleche(self):
        image_d = pygame.image.load(resource_path("resources/flèche2.png"))
        image_g = pygame.transform.flip(pygame.image.load(resource_path("resources/flèche2.png")), True, False)
        self.fleche_d = BoutonIMG(image_d, (Screen.largeur() - 75, 15))
        self.fleche_g = BoutonIMG(image_g, (200, 15))
        self.fleche_d.afficher()
        self.fleche_g.afficher()

    def afficher(self):
        #fond
        Screen.screen.fill(c["WHITE"])
        self.draw_grid()

        #objets
        for plat in Niveau.actuel.objets:
            plat.mouvement()
            dessiner_plateforme_texturee(plat.rect.move(- self.camera, 0))

        #boutons
        pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, 200, Screen.hauteur()))
        for b in self.boutons:
            b.afficher()

        if self.montrer_boutons:
            pygame.draw.rect(Screen.screen, (0, 0, 0), (0, 0, Screen.largeur(), 75))

            for b in self.boutons:
                b.afficher()
            self.recreation_bouton()
            self.boutons_n.afficher()
            self.afficher_fleche()

            if self.fleche_g.est_clique():
                self.decalage -= 1 if self.decalage >= 0 else 0
                self.boutons_n.decaler(self.decalage)

            elif self.fleche_d.est_clique():
                self.decalage += 1
                self.boutons_n.decaler(self.decalage)
                while (Screen.largeur() - 50) - self.boutons_n.boutons[-1].rect.right >= self.boutons_n.boutons[-1].rect.width:
                    self.decalage -= 1
                    self.boutons_n.decaler(self.decalage)


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
            elif self.camera > Niveau.actuel.taille - Screen.largeur() // 2 - 100:
                Screen.camera = Niveau.actuel.taille - Screen.largeur() // 2 + 100
                self.camera = Screen.camera - 200



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
            Message("Cliquer là où vous voulez allez")
        elif self.boutons[2].est_clique():
            Plateforme.liste[Niveau.nombre + 1] = []
            Niveau(Plateforme.liste[Niveau.nombre + 1], 1000)
            Niveau.changer(Niveau.nombre)
            Niveau.changer_etat("editeur")
            self.recreation_bouton()

        elif self.boutons[3].est_clique():
            Niveau.changer_etat("paramettre")
        elif self.boutons[4].est_clique():
            self.type = "plat"
        elif self.boutons[5].est_clique():
            self.type = "asc"
        elif self.boutons_n.est_cliquer() and self.montrer_boutons:
            Niveau.changer(self.boutons_n.boutons.index(self.boutons_n.bouton) + 1)
            self.fermer(1)

    def recreation_bouton(self):
        boutons_n = []
        i = 250
        for n in Niveau.liste:
            b = Bouton(n.name, (i + 50, 25), couleur="WHITE")
            boutons_n.append(b)
            i = b.rect.right
        self.boutons_n = ListeBouton(boutons_n)
        self.boutons_n.decaler(self.decalage)


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
            self.att = Plateforme(Niveau.en_cours, (0, 0), [(0, 0)])
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
        self.att = self.att.maj(x, y, l, h)

    def _clic_relache(self):
        r = self.att.rect
        if self.type == "plat":
            self.action = "rien"

        elif self.type == "asc":
            self.action = "modifier"
            self.listespos.append(self.att.rect.topleft)

    def _gestion_test(self):
        if pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[1] > 75:
            if pygame.mouse.get_pressed()[0]:
                souris = list(pygame.mouse.get_pos())
                souris[0] = self.arrondir25(souris[0], "i") + self.camera
                souris[1] = self.arrondir25(souris[1], "i")
                Niveau.changer_etat("test")
                Joueur.ply.rect.topleft = souris
                Joueur.ply.postest = souris
                Screen.camera = max(0, min(Joueur.ply.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))
                self.fermer(2)


    def _creation_asc(self, events):
        for pos in self.listespos:
            dessiner_plateforme_texturee(pygame.Rect(pos[0] - self.camera, pos[1], *self.att.taille))
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




    def fermer(self, force = 0):
        self.action = "rien"
        self.type = "rien"
        self.att = None
        self.souris1 = None
        if force == 0:
            self.decalage = 0
            self.boutons_n.decaler(self.decalage)
        if force <= 1:
            Screen.camera = -200

    @staticmethod
    def draw_grid(surface=Screen.screen, cell_size=25):
        w, h = surface.get_size()
        # lignes verticales
        for x in range(0, w, cell_size):
            pygame.draw.line(surface, c["BLACK"], (x, 0), (x, h))
        # lignes horizontales
        for y in range(0, h, cell_size):
            pygame.draw.line(surface, c["BLACK"], (0, y), (w, y))

    @staticmethod
    def arrondir25(nombre, cote):
        if cote == "i":
            nombre = nombre // 25 * 25
        elif cote == "s":
            nombre = nombre // 25 * 25 + 25
        return nombre