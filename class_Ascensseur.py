from class_Plateforme import Plateforme
import pygame
pygame.init()

class Ascensseur(Plateforme):

    liste = {}
    for i in range(1,5):
        liste[i] = []


    def __init__(self, niveau, taille, pos1, pos2):
        self.taille = taille
        self.pos1 = pos1
        self.pos2 = pos2
        self.rect = pygame.Rect(self.pos1[0], self.pos1[1], taille[0], taille[1])
        self.niveau = niveau
        self.avance = True
        self.direction = "h" if pos1[0] != pos2[0] else "v"
        if self.direction == "v":
            self.sens = True if pos1[1] < pos2[1] else False
        elif self.direction == "h":
            self.sens = True if pos1[0] < pos2[0] else False
        Ascensseur.liste[self.niveau].append(self)



    def mouvement(self):

        if not self.sens: self.avance = not self.avance
        if self.direction == "v":
            if self.avance:
                self.rect.move_ip(0, 1)
                if self.rect.y > self.pos2[1]:
                    self.avance = False
            else:
                self.rect.move_ip(0, -1)
                if self.rect.y < self.pos1[1]:
                    self.avance = True
        elif self.direction == "h":
            if self.avance:
                self.rect.move_ip(1, 0)
                if self.rect.x > self.pos2[0]:
                    self.avance = False
            else:
                self.rect.move_ip(-1, 0)
                if self.rect.x < self.pos1[0]:
                    self.avance = True

    def to_dict(self):
        return {
            "niveau": self.niveau,
            "taille": self.rect.size,
            "pos1": self.pos1,
            "pos2": self.pos2,
        }
