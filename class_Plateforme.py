import pygame, os, glob

from class_Message import Message

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
        elif not avance:
            self.nu_position = self.nu_position - 1
            self.pos1 = self.positions[self.nu_position]
            self.pos2 = self.positions[self.nu_position - 1]
            self.rect = pygame.Rect(self.pos1[0], self.pos1[1], self.taille[0], self.taille[1])
            self.direction = self.get_direction()
        else :
            self.pos1 = self.positions[self.nu_position]
            self.pos2 = self.positions[self.nu_position + 1]
            self.rect = pygame.Rect(self.pos1[0], self.pos1[1], self.taille[0], self.taille[1])
            self.direction = self.get_direction()

        self.initial_avance = avance
        self.avance = avance
        Plateforme.liste[self.niveau].append(self)

    def porte(self):

        if self.direction in ("top", "bottom") and Joueur.ply.touche(0, 3) == 1:
            tolerance = 2
        else:
            tolerance = 0

        return (
                abs(Joueur.ply.rect.bottom - self.rect.top) <= tolerance
                and Joueur.ply.rect.right > self.rect.left
                and Joueur.ply.rect.left < self.rect.right
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

    @staticmethod
    def _vecteur(direction):
        return {"top": (0, -2), "bottom": (0, 2), "left": (-2, 0), "right": (2, 0)}[direction]

    def mouvement(self):
        if self.nb_positions < 2:
            return
        dx, dy = self._vecteur(self.direction)
        self.rect.move_ip(dx, dy)
        self.check_avance()
        if self.porte():
            Joueur.ply.rect.move_ip(dx, 0)
            Joueur.ply.rect.bottom = self.rect.top
            Joueur.ply.au_sol = True
            Joueur.ply.vy = 0
        elif self.rect.colliderect(Joueur.ply.rect):
            Joueur.ply.deplacer('x' if dx else 'y', dx or dy, True)

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

            self.rect.topleft = self.pos1
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

