from UI.class_Bouton import Bouton
from core.class_Screen import Screen
from core.class_Temps import Timer
import pygame
font = pygame.font.SysFont("arial", 30)
tempsaffichage = 100

class Message(Bouton):
    liste : list= [None,]
    liste_relative : list = [None,]
    def __init__(self, texte):
        Message.liste.append(self)
        Message.liste_relative.append(self)
        self.decalage = 0

        super().__init__(texte, lambda s: (Screen.largeur() - s.taille[0] + self.decalage, Screen.hauteur() - ((Message.liste_relative.index(s) + 1) * 40) - s.taille[1]))

        self.timer1 = Timer(tempsaffichage, "c", self.afficher)
        self.timer2 = Timer(tempsaffichage, "m", Message.liste.remove, paramettres=self)
        self.timers = [Timer(tempsaffichage, "m", Message.liste_relative.remove, paramettres=self)]
        for l in range(self.nb_lignes - 1):
            Message.liste_relative.append(self)
            self.timers.append(Timer(tempsaffichage, "m", Message.liste_relative.remove, paramettres=self))
        self.decalage = self.taille[0]



    def afficher(self):
        self.decalage *= 0.9
        if self.decalage < 0: self.decalage = 0
        super().afficher()
        if self.est_clique:
            Message.liste.remove(self)
            Message.liste_relative = [m for m in Message.liste_relative if m != self]
            self.timer1.stop()
            self.timer2.stop()
            for timer in self.timers:
                timer.stop()


