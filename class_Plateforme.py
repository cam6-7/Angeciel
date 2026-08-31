import pygame, os, glob
pygame.init()
from class_Joueur import Joueur

dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))

class Plateforme:

    liste = {}
    for i in range(1, nombre_de_niveau + 1):
        liste[i] = []

    def __init__(self, niveau, taille, positions , avance : bool = True):
        self.niveau = niveau
        self.taille = taille
        self.nb_positions = len(positions)
        self.positions = list(positions)
        self.nu_position = 0
        if self.nb_positions == 1:
            self.pos1 = positions[0]
            self.rect = pygame.Rect(self.pos1[0], self.pos1[1], self.taille[0], self.taille[1])
        elif self.nb_positions >= 2:
            self.pos1 = self.positions[self.nu_position]
            self.pos2 = self.positions[self.nu_position + 1]
            self.rect = pygame.Rect(self.pos1[0], self.pos1[1], self.taille[0], self.taille[1])
            self.direction = self.get_direction()

        self.initial_avance = avance
        self.avance = avance
        Plateforme.liste[self.niveau].append(self)

    def est_porter(self):

        if self.direction == "v" and self.avance and Joueur.ply.touche(0, 3) == 1: tolerance = 2
        else: tolerance = 0
        return (
                abs(Joueur.rect.bottom - self.rect.top) <= tolerance
                and Joueur.rect.right > self.rect.left
                and Joueur.rect.left < self.rect.right
        )

    def get_direction(self, vraiepose = False):
        if vraiepose:
            pos = self.rect.topleft
        else:
            pos = self.pos1


        if pos[1] < self.pos2[1]:
            return "bottom"
        elif pos[1] > self.pos2[1]:
            return "top"
        elif pos[0] > self.pos2[0]:
            return "left"
        elif pos[0] < self.pos2[0]:
            return "right"

    def mouvement(self):
        if self.nb_positions < 2:
            return
        print(self.direction)
        if self.direction == "top":
            self.rect.move_ip(0, -2)
        elif self.direction == "bottom":
            self.rect.move_ip(0, 2)
        elif self.direction == "left":
            self.rect.move_ip(-2, 0)
        elif self.direction == "right":
            self.rect.move_ip(2, 0)
        self.check_avance()

    def check_avance(self):
        if self.direction != self.get_direction(True):
            if self.avance:
                self.nu_position += 1
                if self.nu_position >= self.nb_positions -1:
                    self.avance = False
                    self.pos1 = self.positions[self.nu_position]
                    self.pos2 = self.positions[self.nu_position - 1]
                else:
                    self.pos1 = self.positions[self.nu_position]
                    self.pos2 = self.positions[self.nu_position + 1]
            elif not self.avance:
                self.nu_position -= 1
                if self.nu_position <= 0:
                    self.avance = True
                    self.pos1 = self.positions[self.nu_position]
                    self.pos2 = self.positions[self.nu_position + 1]
                else:
                    self.pos1 = self.positions[self.nu_position]
                    self.pos2 = self.positions[self.nu_position - 1]

            self.direction = self.get_direction()


    def supprimer(self):
        Plateforme.liste[self.niveau].remove(self)

    def maj(self, x, y, l, h):
        self.pos1 = [x, y]
        self.positions = [self.pos1]
        self.taille = [l, h]
        self.rect = pygame.Rect(x, y, l, h)


    def copy(self):
        return Plateforme(self.niveau, self.taille, self.positions)


    def to_dict(self):
        return {
            "niveau": self.niveau,
            "taille": self.taille,
            "positions": self.positions,
            "avance": self.initial_avance
        }

