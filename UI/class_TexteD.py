from core.class_Texte import Texte
import math

class TexteD(Texte):

    def __init__(self, text, position, couleur= (0, 0, 0), taillepolice = 30, police ="arial"):
        super().__init__(text, position, couleur, taillepolice, police)
        self.base = position[0]

    def move(self, cam, joueur):
        self.position[0] = self.base - cam
        self.mise_a_jour(nouvelle_pos= self.position)
        self.transparence(joueur)
        self.afficher()

    def transparence(self, joueur):

        self.distance = math.hypot(self.rect.centerx - joueur.centerx, self.rect.centery - joueur.centery)
        opacite = max(0, min(255, 350 - round(self.distance)))
        self.surface.set_alpha(opacite)
