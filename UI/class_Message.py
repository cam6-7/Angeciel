from core.class_Temps import Timer
from UI.class_Texte import Texte
from entities.class_Niveau import Niveau
import pygame
pygame.init()
font = pygame.font.SysFont("arial", 30)

class Message(Texte):
    stop = False
    liste = [None,]
    def __init__(self, message):
        if Niveau.etat == "editeur":
            super().__init__(message, ("x", 100) , centre= "spe")
        else:
            super().__init__(message, ("x", 2) , centre= "x")
        Message.liste.append(self)
        Timer(3, "c", self.afficher, condition= lambda : not Message.stop and Message.liste[-1] is self)
