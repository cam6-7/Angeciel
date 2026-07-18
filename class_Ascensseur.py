from class_Joueur import Joueur
from class_Niveau import Niveau
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

    def est_porter(self):

        if self.direction == "v" and self.avance and Joueur.ply.touche(0, 3) == 1:
            tolerance = 2
        else:
            tolerance = 0

        ply = Joueur.ply
        return (
                abs(ply.rect.bottom - self.rect.top) <= tolerance
                and ply.rect.right > self.rect.left
                and ply.rect.left < self.rect.right
        )

    def mouvement(self):
        ply = Joueur.ply
        self.move = [0, 0]
        d = ""

        if self.direction == "v":
            if self.avance:
                self.move[1] = 2
                d = "haut"
                if self.rect.y > self.pos_b[1]:
                    self.avance = False
            else:
                self.move[1] = -2
                d = "bas"
                if self.rect.y < self.pos_h[1]:
                    self.avance = True

        elif self.direction == "h":
            if self.avance:
                self.move[0] = 2
                d = "gauche"
                if self.rect.x > self.pos_d[0]:
                    self.avance = False
            else:
                self.move[0] = -2
                d = "droite"
                if self.rect.x < self.pos_g[0]:
                    self.avance = True

        self.rect.move_ip(*self.move)
        if self.rect.colliderect(ply.rect):
            if d == "droite":
                ply.rect.right = self.rect.left
                ply.collids["droite"] = 2
            elif d == "gauche":
                ply.rect.left = self.rect.right
                ply.collids["gauche"] = 2
            elif d == "bas" :
                ply.rect.bottom = self.rect.top
                ply.collids["bas"] = 2
            elif d == "haut":
                ply.rect.top = self.rect.bottom
                ply.collids["haut"] = 2

    def to_dict(self):
        return {
            "niveau": self.niveau,
            "taille": self.rect.size,
            "pos1": self.pos1,
            "pos2": self.pos2,
        }