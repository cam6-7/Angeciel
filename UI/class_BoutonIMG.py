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
        if self.est_survole:
            fond_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            fond_surface.fill((80, 80, 80, 150))
            Screen.screen.blit(fond_surface, self.rect)
        Screen.screen.blit(self.image, self.position)

    def mise_a_jour(self, nouvelle_pos):
        self.position = nouvelle_pos