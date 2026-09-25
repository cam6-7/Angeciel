from core.class_Texte import Texte
from core.class_Clickable import Clickable
from core.class_Screen import Screen


class Bouton(Texte, Clickable):

    def __init__(self, text : str, position : tuple | callable, couleur: tuple = (0, 0, 0), taillepolice: int = 30, police ="arial"):
        Texte.__init__(*locals().values())
        Clickable.__init__(self, self.position, self.taille)

    def afficher(self):
        self.afficherfond()
        Screen.screen.blit(self.surface, self.rect)