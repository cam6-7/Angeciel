from class_Joueur import Joueur
from class_Plateforme import Plateforme
import pygame, os, glob
pygame.init()
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))
class Ascensseur(Plateforme):

    liste = {}
    for i in range(1,nombre_de_niveau + 1):
        liste[i] = []


    def __init__(self, niveau, taille, pos1, pos2):
        self.taille = taille
        self.pos1 = pos1
        self.pos2 = pos2
        self.rect = pygame.Rect(self.pos1[0], self.pos1[1], taille[0], taille[1])
        self.niveau = niveau
        self.avance = True
        self.move = []
        self.direction = "h" if pos1[0] != pos2[0] else "v"
        if self.direction == "v":
            self.sens = True if pos1[1] < pos2[1] else False
        elif self.direction == "h":
            self.sens = True if pos1[0] < pos2[0] else False
        self.pos_g, self.pos_d = sorted([pos1, pos2], key=lambda x: x[0])
        self.pos_h, self.pos_b = sorted([pos1, pos2], key=lambda x: x[1])
        Ascensseur.liste[self.niveau].append(self)

    def est_porter(self, tolerance=2):
        ply = Joueur.ply
        return (
                abs(ply.rect.bottom - self.rect.top) <= tolerance
                and ply.rect.right > self.rect.left
                and ply.rect.left < self.rect.right
        )

    def mouvement(self):
        self.move = [0, 0]
        if self.direction == "v":
            if self.avance:
                self.move[1] = 2
                if self.rect.y > self.pos_b[1]:
                    self.avance = False
            else:
                self.move[1] = -2
                if self.rect.y < self.pos_h[1]:
                    self.avance = True


        elif self.direction == "h":
            if self.avance:
                self.move[0] = 2
                if self.rect.x > self.pos_d[0]:
                    self.avance = False
            else:
                self.move[0] = -2
                if self.rect.x < self.pos_g[0]:
                    self.avance = True

        self.rect.move_ip(*self.move)

    def to_dict(self):
        return {
            "niveau": self.niveau,
            "taille": self.rect.size,
            "pos1": self.pos1,
            "pos2": self.pos2,
        }
