import pygame
pygame.init()
from class_Niveau import Niveau
from class_Screen import Screen
from fonction_ressource_path import resource_path
from typing import ClassVar
# images
image_player_g = pygame.image.load(resource_path("resources/image_player_g.png"))
image_player_d = pygame.image.load(resource_path("resources/image_player_d.png"))
class Joueur:
    ply: ClassVar["Joueur"] = None
    def __init__(self):
        self.rect = pygame.Rect(50, 50, 25, 25)
        self.au_sol = False
        self.taille = 25
        self.image = pygame.image.load(resource_path("resources/image_player_d.png"))
        self.gravite = 0
        self.saut = 0
        Joueur.ply = self

    @property
    def pos(self):
        return self.rect.topleft

    def bouger(self):
        if self.touche():
            self.reinitialiser_jeu(True)
        self.au_sol = False

        self.rect.move_ip(0, self.gravite)
        self.gravite += 0.9
        self.gerer_collisions("bottom")

        self.rect.move_ip(0, -self.saut)
        self.saut -= 0.5 if self.saut > 0 else 0
        self.gerer_collisions("top")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.au_sol and self.saut == 0:
            self.saut = 20
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.gerer_collisions("left")
            self.image = image_player_g
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.gerer_collisions("right")
            self.image = image_player_d
        self.limit_move()
        Screen.camera = max(0, min(self.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))


    def afficher(self):
        Screen.screen.blit(self.image, self.rect_ecran)


    def transportage(self):
        for plat in Niveau.actuel.ascensseurs:
            if plat.est_porter():
                self.rect.bottom = plat.rect.top

    def gerer_collisions(self, direction : str):
        vitesse = self.gravite - self.saut
        if self.touche() == 1:
            for obj in Niveau.actuel.objets:
                if obj.rect.colliderect(self.rect):
                    if direction == "top":
                        self.rect.top = obj.rect.bottom
                        if vitesse < 0:
                            self.saut = 0
                            self.gravite = 0
                    elif direction == "bottom":
                        self.rect.bottom = obj.rect.top
                        if vitesse > 0:
                            self.saut = 0
                            self.gravite = 0
                            self.au_sol = True

                    elif direction == "right":
                        self.rect.right = obj.rect.left
                    elif direction == "left":
                        self.rect.left = obj.rect.right
                    else: raise ValueError

        elif self.touche() > 1:
            liste = [ obj.rect for obj in Niveau.actuel.objets if obj.rect.colliderect(self.rect)]
            obj = liste[0]
            if direction == "top" and all([objet.bottom == obj.bottom for objet in liste ]):
                self.rect.top = obj.bottom
                self.saut = 0
                self.gravite = 0
            elif direction == "bottom" and all([objet.top == obj.top for objet in liste ]):
                self.rect.bottom = obj.top
                self.au_sol = True
                self.gravite = 0
                self.saut = 0
            elif direction == "right" and all([objet.left == obj.left for objet in liste ]):
                self.rect.right = obj.left
            elif direction == "left" and all([objet.right == obj.right for objet in liste ]):
                self.rect.left = obj.right
            else: print("erreur :", direction)

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
            self.reinitialiser_jeu(True)

    @property
    def rect_ecran(self):
        return self.rect.move(-Screen.camera, 0)

    def reinitialiser_jeu(self, mort = False):
        self.saut = 0
        self.gravite = 0
        self.rect.topleft = (50, 50)
        if mort: print("renitialisation du jeu par mort")
        else: print("renitialisation du jeu basique")
        save = not mort
        if Niveau.etat == "test":
            Niveau.changer_etat("test",not  save)
        else:
            Niveau.changer_etat("jeu",not  save)