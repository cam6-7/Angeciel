from core.class_Texte import Texte
from core.class_Screen import Screen
from core.class_Temps import Timer


class Debug(Texte):
    liste = []
    nombre = 0
    def __init__(self, fonction = lambda : "", description : tuple(str) = ("", "")):
        super().__init__("", (0, 0), couleur= (86, 97, 156))
        self.fonction = fonction
        self.y = 30 * Debug.nombre
        self.description = description
        Debug.liste.append(self)
        Debug.nombre += 1
        Timer(1, "i", self.afficher)

    def afficher(self):
        self.mise_a_jour(str(self.description[0]) + str(self.fonction()) + self.description[1], (Screen.largeur() - self.taille[0], self.y))
        super().afficher()