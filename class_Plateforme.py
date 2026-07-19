import pygame, os, glob

pygame.init()
from class_Niveau import Niveau
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))

class Plateforme:

    liste = {}
    for i in range(1, nombre_de_niveau + 1):
        liste[i] = []
    def __init__(self, x, y, l, h, niveau):
        self.niveau = niveau
        self.rect = pygame.Rect(x, y, l, h)
        Plateforme.liste[self.niveau].append(self)


    def supprimer(self):
        if self in Niveau.actuel.ascensseurs :
            Niveau.actuel.ascensseurs.remove(self)
        if self in Niveau.actuel.plateformes:
            Niveau.actuel.plateformes.remove(self)

    def maj(self, x, y, l, h):
        self.rect = pygame.Rect(x, y, l, h)


    def copy(self):
        return Plateforme(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.niveau)


    def to_dict(self):
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "largeur": self.rect.width,
            "hauteur": self.rect.height,
        }
