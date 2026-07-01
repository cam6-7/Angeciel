from class_Screen import Screen
from fonction_ressource_path import resource_path
import pygame
pygame.init()

texture_plateforme = pygame.transform.scale(pygame.image.load(resource_path("resources/texture.jpg")).convert_alpha(), (200, 200))
def dessiner_plateforme_texturee(rect):
    """Dessine une plateforme avec texture répétée."""
    tex_l, tex_h = texture_plateforme.get_size()
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for x in range(0, rect.width, tex_l):
        for y in range(0, rect.height, tex_h):
            surface.blit(texture_plateforme, (x, y))
    Screen.screen.blit(surface, (rect.x, rect.y))