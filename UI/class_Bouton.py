from UI.class_Texte import Texte
from core.class_Clickable import Clickable
from core.class_Screen import Screen
import pygame


class Bouton(Texte, Clickable):

    def __init__(self, text : str, position : tuple, couleur: tuple = (0, 0, 0), taillepolice: int = 30, police ="arial", centre =""):
        Texte.__init__(*locals().values())
        Clickable.__init__(self, tuple(self.position), self.surface.get_rect().size)
        self.gtaille = (self.gtaille[0] + 20, self.gtaille[1] + 20)
    @property
    def rect(self) -> pygame.Rect:
        rect = self.surface.get_rect(topleft = self.position)
        if "x" in self.centre :
            rect.centerx = Screen.largeur() // 2
        if "y" in self.centre :
            rect.centery = Screen.hauteur() // 2
        return rect

    def afficher(self):
        if self.est_survole:
            fond_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            fond_surface.fill((80, 80, 80, 150))
            Screen.screen.blit(fond_surface, self.rect)
        Screen.screen.blit(self.surface, self.rect)