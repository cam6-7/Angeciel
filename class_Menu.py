from class_Screen import Screen
from fonction_texture import dessiner_plateforme_texturee
import pygame
pygame.init()
class Menu:
    def __init__(self, boutons, couleur = False):
        self.couleur = couleur
        self.boutons = boutons

    def afficher(self):
        if self.couleur:
            Screen.screen.fill(self.couleur)
        else:
            rect = pygame.Rect(0, 0, Screen.largeur(), Screen.hauteur())
            dessiner_plateforme_texturee(rect)

        for bouton in self.boutons:
            bouton.afficher()