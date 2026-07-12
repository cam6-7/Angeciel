import pygame
from pygame import time
from mes_class import *
pygame.init()

class Timer:
    liste = []
    def __init__(self, durre, tip, fonction, paramettres = []):
        self.durre = durre * 1000
        self.type = tip
        self.fonction = fonction
        self.paramettre = paramettres
        self.debut = time.get_ticks()
        self.fin = self.debut + self.durre
        Timer.liste.append(self)

    @classmethod
    def mise_a_jour(cls):
        temps = time.get_ticks()
        for t in cls.liste:
            if t.type == "m":
                if temps >= t.fin:
                    t.fonction(*t.paramettre)
                    cls.liste.remove(t)
            elif t.type == "c":
                if temps < t.fin:
                    t.fonction(*t.paramettre)
                elif temps >= t.fin:
                    cls.liste.remove(t)
            else:
                raise ValueError