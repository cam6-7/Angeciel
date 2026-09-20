import pygame

from core.class_Clickable import Clickable
from core.class_Screen import Screen

class BoutonIMG(Clickable):

    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.taille = self.image.get_size()
        super().__init__(self.position, self.taille)

    def afficher(self):
        self.afficherfond()
        Screen.screen.blit(self.image, self.position)

    def mise_a_jour(self, nouvelle_pos):
        self.position = nouvelle_pos