import pygame
pygame.init()
class Screen:

    camera = 0
    screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Angeciel")
    pygame.display.set_icon(pygame.image.load("resources/icon.png"))

    @classmethod
    def largeur(cls):
        return cls.screen.get_size()[0]

    @classmethod
    def hauteur(cls):
        return cls.screen.get_size()[1]
