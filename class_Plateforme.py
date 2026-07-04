import pygame
pygame.init()
from class_Niveau import Niveau
from class_Joueur import Joueur


class Plateforme:

    liste = {}
    for i in range(1, 5):
        liste[i] = []


    def __init__(self, x, y, l, h, niveau):
        self.niveau = niveau
        self.rect = pygame.Rect(x, y, l, h)
        if type(self) is Plateforme: Plateforme.liste[self.niveau].append(self)

    def supprimer(self):
        if self in Niveau.actuel.ascensseurs :
            Niveau.actuel.ascensseurs.remove(self)
        if self in Niveau.actuel.plateformes:
            Niveau.actuel.plateformes.remove(self)

    def move(self, x, y, l, h):
        self.supprimer()
        self.rect = pygame.Rect(x, y, l, h)
        Plateforme.liste[self.niveau].append(self)


    def collision_horizontale(self):
        ply = Joueur.ply
        # par la gauche
        if ply.vitesse[0] > 0:
            ply.frect.right = self.rect.x
        # par la droite
        elif ply.vitesse[0] < 0:
            ply.frect.x = self.rect.right

    def collidepoint(self, point):
        if self.rect.collidepoint(point):
            return True
        else:
            return False

    def copy(self):
        return Plateforme(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.niveau)

    def collision_verticale(self):
        ply = Joueur.ply
        # Collision par le dessus
        if ply.vitesse[1] > 0:
            ply.frect.bottom = self.rect.top
            ply.au_sol = True
            ply.vitesse[1] = 0

        # Collision par le dessous
        elif ply.vitesse[1] <= 0:
            ply.frect.top = self.rect.bottom
            ply.vitesse[1] = 0


    def to_dict(self):
        return {
            "type": "Plateforme",
            "niveau": self.niveau,
            "x": self.rect.x,
            "y": self.rect.y,
            "largeur": self.rect.width,
            "hauteur": self.rect.height,
        }
