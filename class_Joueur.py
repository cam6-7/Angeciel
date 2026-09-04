import pygame
pygame.init()
from class_Niveau import Niveau
from class_Screen import Screen
from fonction_ressource_path import resource_path
from typing import ClassVar
# images
image_player_g = pygame.image.load(resource_path("resources/image_player_g.png"))
image_player_d = pygame.image.load(resource_path("resources/image_player_d.png"))
VITESSE_MARCHE = 5
GRAVITE = 0.9
VITESSE_SAUT = 20

class Joueur:
    ply: ClassVar["Joueur"] = None
    def __init__(self):
        self.rect = pygame.Rect(50, 50, 25, 25)
        self.au_sol = False
        self.taille = 25
        self.image = pygame.image.load(resource_path("resources/image_player_d.png"))
        self.gravite = 0
        self.saut = 0
        self.vx = 0
        self.vy = 0
        Joueur.ply = self

    @property
    def pos(self):
        return self.rect.topleft

    def deplacer(self, direction, vitesse = 25, force = False):
        if abs(int(round(vitesse, 0))) ==0:
            return
        if direction == "y":
            if vitesse < 0:
                direction = "top"
            else:
                direction = "bottom"
        elif direction == "x":
            if vitesse < 0:
                direction = "left"
            else:
                direction = "right"
        for i in range(abs(int(round(vitesse, 0)))):
            if direction == "top":
                self.rect.move_ip(0, -1)
            elif direction == "bottom":
                self.rect.move_ip(0, 1)
            elif direction == "left":
                self.rect.move_ip(-1, 0)
            elif direction == "right":
                self.rect.move_ip(1, 0)
            if not force:
                self.gerer_collisions(direction)
        if force and self.touche():
            self.reinitialiser_jeu()

    def bouger(self):
        if self.touche():
            print("erreur de logique, touche avant déplacement")
            self.reinitialiser_jeu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx = VITESSE_MARCHE
            self.image = image_player_g
        if keys[pygame.K_RIGHT]:
            self.vx = VITESSE_MARCHE
            self.image = image_player_d
        if keys[pygame.K_SPACE] and self.au_sol:
            self.vy = -VITESSE_SAUT

        self.vy += GRAVITE

        self.deplacer('x', self.vx)
        self.deplacer('y', self.vy)

        self.au_sol = False
        for plat in Niveau.actuel.objets:
            plat.mouvement()

        self.limit_move()
        Screen.camera = max(0, min(self.rect.x - Screen.largeur() // 2,  Niveau.actuel.taille - Screen.largeur()))

    def afficher(self):
        Screen.screen.blit(self.image, self.rect_ecran)

    def gerer_collisions(self, direction : str):
        liste = [obj for obj in Niveau.actuel.objets if obj.rect.colliderect(self.rect)]
        if len(liste) == 0:
            return
        obj = liste[0]


        if direction == "top" and all([objet.rect.bottom == obj.rect.bottom for objet in liste]):
            self.rect.top = obj.rect.bottom
            self.saut = 0
            self.gravite = 0
        elif direction == "bottom" and all([objet.rect.top == obj.rect.top for objet in liste]):
            self.rect.bottom = obj.rect.top
            self.saut = 0
            self.gravite = 0
            self.au_sol = True
        elif direction == "right" and all([objet.rect.left == obj.rect.left for objet in liste]):
            self.rect.right = obj.rect.left
        elif direction == "left" and all([objet.rect.right == obj.rect.right for objet in liste]):
            self.rect.left = obj.rect.right
        else:
            print("erreur :", direction)
            if not direction in ["top", "bottom", "left", "right"]: raise ValueError
            else : raise ValueError

        if self.touche():
            self.reinitialiser_jeu()

    def touche(self, dx = 0, dy = 0):
        # fonction qui renvoie le nombre de plateform que touche le joueur
        # (on peut le déplacer pour tester des collisions futures ou antérieurs)
        rect = self.rect.move(dx, dy)
        touche = 0
        for obj in Niveau.actuel.objets:
            if rect.colliderect(obj.rect):
                touche += 1
        return touche

    def limit_move(self):
        # si on va trop a gauche
        if self.rect.left < 0:
            self.rect.left = 0
        # si on va trop a droite
        elif self.rect.right > Niveau.actuel.taille:
            Niveau.changer_etat("victoire")

        # si on va trop haut
        if self.rect.y < 0:
            self.rect.y = 0
            self.saut = 0
            self.gravite = 0
        # si on va trop bas
        elif self.rect.top >= Screen.hauteur():
            self.reinitialiser_jeu()

    @property
    def rect_ecran(self):
        return self.rect.move(-Screen.camera, 0)

    def reinitialiser_jeu(self):
        self.saut = 0
        self.gravite = 0
        self.rect.topleft = (50, 50)
        if Niveau.etat == "test":
            Niveau.changer_etat("test")
        else:
            Niveau.changer_etat("jeu")