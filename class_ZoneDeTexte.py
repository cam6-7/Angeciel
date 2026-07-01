import ast
from class_Screen import Screen
from class_Texte import Texte
from cp import *

class ZoneDeTexte(Texte):
    def __init__(self, text, position,  variable, module, couleur=BLACK, taille = 30, police = "arial", centre = ""):
        super().__init__(text, position, couleur, taille, police, centre)
        self.active = False
        self.var = variable
        self.module = module
        self.type = type(getattr(self.module, self.var))
        self.text = str(getattr(self.module, self.var))
        self.mise_a_jour(self.text)


    def afficher(self, events):

        self.gerer_events(events)

        if self.active:
            couleur = BLUE
        else:
            couleur = BLACK

        pygame.draw.rect(Screen.screen, couleur, self.rect.inflate(20, 10), 3)
        super().afficher()

    def gerer_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    print(self.type)
                    if self.type == list:
                        print("tuple !!!")
                        donnee = ast.literal_eval(self.text)

                    elif self.type == int:
                        donnee = int(self.text)
                    else:
                        donnee = self.text
                    print(donnee)
                    print(type(donnee))
                    setattr(self.module, self.var, donnee)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.mise_a_jour(self.text)