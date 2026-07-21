import pygame
pygame.init()

from mes_class import *
from cp import couleurs as c
vitesse = 2


class Question:
    def __init__(self, question : str, stockage : str, typ = str):
        self.stockage = stockage
        self.text = str(self.obtenir())
        self.question = Texte(question, ["x", 200], c["BLACK"], police = "couriernew")
        self.reponse = Texte(self.text, ["x", 400], c["BLACK"], police = "couriernew")
        self.typ = typ
        self.en_cours = True
        self.decalage = 0
        self.afficher()

    def afficher(self):
        while self.en_cours:
            self.gerer_events()
            pygame.draw.rect(Screen.screen, (255, 255, 255), (100, 150, Screen.largeur() - 200, 300))
            self.question.afficher()
            self.reponse.afficher()
            self.afficher_trait()
            pygame.display.flip()

    def gerer_events(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    donnee = self.typ(self.text)
                    self.modifier(donnee)
                    self.en_cours = False
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) <= 1:
                        self.text = ""
                    elif self.decalage == 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.text[:-(self.decalage + 1)] + self.text[-self.decalage:]
                elif event.key == pygame.K_LEFT:
                    self.decalage +=1
                elif event.key == pygame.K_RIGHT:
                    self.decalage -=1
                else:
                    if self.decalage == 0:
                        self.text += event.unicode
                    else:
                        self.text = self.inserer(self.text, event.unicode, - self.decalage)
                if self.decalage < 0: self.decalage = 0
                elif self.decalage > len(self.text): self.decalage = len(self.text)
                self.reponse.mise_a_jour(self.text)

    def afficher_trait(self):
        temps = pygame.time.get_ticks()
        if (temps // (1000 // vitesse ))% 2 == 0:
            trait = pygame.Rect(self.reponse.rect.right - (self.decalage * 18), self.reponse.rect.y, 1, self.reponse.rect.height)
            pygame.draw.rect(Screen.screen, (0, 0, 0), trait)

    def obtenir(self):
        morceaux = self.stockage.split(".")
        nom_racine, *reste = morceaux
        obj = globals()[nom_racine]
        for attribut in reste:
            obj = getattr(obj, attribut)
        return obj

    def modifier(self, valeur):
        morceaux = self.stockage.split(".")
        nom_racine, *reste = morceaux
        obj = globals()[nom_racine]
        *parents, dernier = reste
        for attribut in parents:
            obj = getattr(obj, attribut)
        setattr(obj, dernier, valeur)

    @staticmethod
    def inserer(chaine, texte, position):
        return chaine[:position] + texte + chaine[position:]