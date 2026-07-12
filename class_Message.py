from class_Screen import Screen
from class_Temps import Timer
from class_Texte import Texte
from class_Niveau import Niveau
import pygame
pygame.init()
font = pygame.font.SysFont("arial", 30)

class Message(Texte):
    def __init__(self, message):
        if Niveau.etat == "editeur":
            super().__init__(message, ("x", 100) , centre= "spe")
        else:
            super().__init__(message, ("x", 2) , centre= "x")
        Timer(3, "c", self.afficher)
