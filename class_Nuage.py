import random
from class_Screen import Screen
import pygame
pygame.init()
from fonction_ressource_path import resource_path

nuage = pygame.image.load(resource_path("resources/nuage.png"))


class Nuage:
    liste = []
    def __init__(self):
        self.vitesse = random.randint(8, 18) / 10
        self.position = [random.randint(-200, Screen.largeur() - 200), random.choice([50, 75, 100, 125, 150])]
        facteur =  random.randint(5, 15) / 10 # double la taille
        w, h = nuage.get_size()
        self.image = pygame.transform.scale(nuage, (w * facteur, h * facteur))
        Nuage.liste.append(self)

    def afficher(self):
        self.position[0] += self.vitesse
        if self.position[0] > Screen.largeur():
            self.position = [-200, random.randint(0, random.choice([50, 75, 100]))]
            self.vitesse = random.randint(8, 18) / 10
        self.rect = pygame.Rect(self.position[0], self.position[1], 400, 400)
        Screen.screen.blit(self.image, self.rect)