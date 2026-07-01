from class_Plateforme import Plateforme
import pygame
pygame.init()

class Ascensseur(Plateforme):

    liste = {}
    for i in range(1,5):
        liste[i] = []


    def __init__(self, niveau, x, taille, max_min):
        super().__init__(x, max_min[0], taille[0], taille[1], niveau )
        self.taille = taille
        self.max = sorted(max_min)
        self.rect = pygame.Rect(x, self.max[0], taille[0], taille[1])
        self.niveau = niveau
        self.monte = True
        Ascensseur.liste[self.niveau].append(self)

    def mouvement(self):
        if self.rect.y < self.max[0]:
            self.monte = False
        elif self.rect.y > self.max[1]:
            self.monte = True
        self.rect.y += -1 if self.monte else 1

    def to_dict(self):
        return {
            "niveau": self.niveau,
            "x": self.rect.x,
            "taille": self.rect.size,
            "max_min": list(self.max),  # tuple -> liste JSON
        }
