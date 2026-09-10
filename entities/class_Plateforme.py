import pygame
from entities.class_Joueur import Joueur
from entities.class_Niveau import Niveau


class Plateforme:
    def __init__(self, niveau, taille, positions , avance : bool = True):
        self.niveau = niveau
        self.taille = taille
        self.positions = list(positions)
        self.initial_avance = avance
        self.avance = avance
        self.nb_positions = len(positions)
        self.nu_position = 0 if avance else self.nb_positions - 1
        self.rect = pygame.Rect(self.pos1[0], self.pos1[1], self.taille[0], self.taille[1])
        self.direction = self.get_direction()
        Niveau.actuel.plateformes.append(self)

    @property
    def pos1(self):
        return self.positions[self.nu_position]

    @property
    def pos2(self):
        if self.nb_positions == 1: return self.pos1
        elif self.avance: return self.positions[self.nu_position + 1]
        else: return self.positions[self.nu_position - 1]

    def porte(self):
        if self.direction in ("top", "bottom"): tolerance = 2
        else: tolerance = 0
        return (    abs(self.rect.top - Joueur.ply.rect.bottom) <= tolerance
                    and Joueur.ply.rect.right > self.rect.left
                    and Joueur.ply.rect.left < self.rect.right  )

    def get_direction(self):
        pos = self.rect.topleft
        if pos[1] < self.pos2[1]:
            return "bottom"
        elif pos[1] > self.pos2[1]:
            return "top"
        elif pos[0] > self.pos2[0]:
            return "left"
        elif pos[0] < self.pos2[0]:
            return "right"
        else :
            return None

    def mouvement(self):
        if self.nb_positions < 2: return
        dx, dy = {"top": (0, -2), "bottom": (0, 2), "left": (-2, 0), "right": (2, 0)}[self.direction]
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
        if self.direction != self.get_direction():
            if self.avance:
                self.nu_position += 1
                if self.nu_position + 1 >= self.nb_positions:
                    self.avance = False
            else:
                self.nu_position -= 1
                if self.nu_position <= 0:
                    self.avance = True

            self.rect.topleft = self.pos1
            self.direction = self.get_direction()

    def supprimer(self):
        if self in Niveau.actuel.plateformes:
            Niveau.actuel.plateformes.remove(self)
        else:
            print("Erreur, il n'y a pas cette plateforme dans le niveau", Niveau.en_cours)

    def maj(self, x, y, l, h):
        self.supprimer()
        return Plateforme(self.niveau, (l, h), [(x, y)])


    def copy(self):
        return Plateforme(self.niveau, self.taille, self.positions)


    def to_dict(self):
        return {
            "niveau": self.niveau,
            "taille": self.taille,
            "positions": self.positions,
            "avance": self.initial_avance
        }