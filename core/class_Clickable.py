import pygame
from core.fonction_ressource_path import resource_path
s_click = pygame.mixer.Sound(resource_path("resources/click.mp3"))


class Clickable:
    last_clic = 0
    def __init__(self, position : tuple, taille : tuple):
        self.position = list(position)
        self.taille = list(taille)
        self.gtaille = (self.taille[0] + 10, self.taille[1] + 10)
        self.ptaille = self.taille


    @property
    def est_survole(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.position, *self.taille)

    @property
    def est_clique(self):
        touch = False
        t = pygame.time.get_ticks()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if t - Clickable.last_clic > 200:
                    touch = True
                    s_click.play()
                    Clickable.last_clic = pygame.time.get_ticks()
        return touch