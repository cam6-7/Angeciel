from class_Texte import Texte
from cp import couleurs as c
import math

class TexteD(Texte):

    def __init__(self, text, position, couleur=c["BLACK"], taille = 30, police = "arial", centrer = ""):
        super().__init__(text, position, couleur, taille, police, centrer)
        self.base = position[0]

    def move(self, cam, joueur):
        self.x = self.base - cam
        self.mise_a_jour(nouvelle_pos= (self.x, self.y))
        self.transparence(joueur)
        self.afficher()

    def transparence(self, joueur):

        self.distance = math.hypot(self.rect.centerx - joueur.centerx, self.rect.centery - joueur.centery)
        opacite = max(0, min(255, 350 - round(self.distance)))
        self.surface.set_alpha(opacite)
