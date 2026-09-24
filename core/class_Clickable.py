import pygame

from core.class_Screen import Screen
from core.fonction_ressource_path import resource_path
s_click = pygame.mixer.Sound(resource_path("resources/click.mp3"))


class Clickable:
    last_clic = 0
    def __init__(self, position : tuple| callable, taille : tuple):
        if callable(position):  self.position = position
        else: self.position = list(position)
        self.taille = list(taille)


    def afficherfond(self, force = False):
        if self.est_survole or force:
            fond_surface = pygame.Surface(self.zonedecollision.size, pygame.SRCALPHA)
            fond_surface.fill((80, 80, 80, 150))
            Screen.screen.blit(fond_surface, self.zonedecollision)

    @property
    def est_survole(self):
        return self.zonedecollision.collidepoint(pygame.mouse.get_pos())


    @property
    def zonedecollision(self) -> pygame.Rect:
        if callable(self.position): pos : list = list(self.position(self))
        else: pos : list = self.position
        return pygame.Rect(*pos, *self.taille)

    @property
    def est_clique(self):
        touch = False
        t = pygame.time.get_ticks()
        if self.zonedecollision.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if t - Clickable.last_clic > 200:
                    touch = True
                    s_click.play()
                    Clickable.last_clic = pygame.time.get_ticks()
        return touch