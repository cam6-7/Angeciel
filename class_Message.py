from class_Screen import Screen
from class_Temps import Timer
from class_Texte import Texte
import pygame
pygame.init()
font = pygame.font.SysFont("arial", 30)

class Message(Texte):
    def __init__(self, message):
        super().__init__(message, (Screen.largeur()//2, 2) , centre= "x")
        Timer(3, "c", self.afficher)
