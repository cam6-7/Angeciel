import pygame
pygame.init()
from class_Screen import Screen
from fonction_ressource_path import resource_path
s_click = pygame.mixer.Sound(resource_path("resources/click.mp3"))

class BoutonIMG:

    def __init__(self, image, position, centre=False):
        self.image_originale = image
        self.image = image
        self.gtaille = (image.get_width() + 20, image.get_height() + 20)
        self.ptaille = image.get_size()
        self.position = position
        self.centre = centre

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.taille[0], self.taille[1])

    @property
    def x(self):
        return self.position[0]
    @property
    def y(self):
        return self.position[1]
    @property
    def taille(self):
        return self.image.get_size()

    def afficher(self):
        self._changetaille()
        Screen.screen.blit(self.image, (self.x, self.y))

    def _changetaille(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.taille < self.gtaille:
                nouvelle_taille = (self.taille[0] + 2, self.taille[1] + 2)
                self.image = pygame.transform.scale(self.image_originale, nouvelle_taille)
                self.position = [self.x - 1, self.y - 1]
        else:
            if self.taille > self.ptaille:
                nouvelle_taille = (self.taille[0] - 2, self.taille[1] - 2)
                self.image = pygame.transform.scale(self.image_originale, nouvelle_taille)
                self.position = [self.x + 1, self.y + 1]

    last_clic = 0
    def est_clique(self):
        touch = False
        t = pygame.time.get_ticks()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if t - BoutonIMG.last_clic > 200:
                    touch = True
                    s_click.play()
                    BoutonIMG.last_clic = pygame.time.get_ticks()
        return touch