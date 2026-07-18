from class_Niveau import Niveau
from class_Texte import Texte
from class_Temps import Timer
from class_Screen import Screen
class Debug(Texte):
    liste = []
    nombre = 0
    def __init__(self, variable, module, etats, description = "", cle = None, fonction  = lambda text : text):
        super().__init__("", (0, 0))
        self.fonction = fonction
        self.variable = variable
        self.module = module
        self.etats = etats
        self.valeur = ""
        self.valeur_o = ""
        self.cle = cle
        self.y = 30 * Debug.nombre
        self.description = description
        self.taille = self._get_surface().get_rect().width
        Debug.liste.append(self)
        Debug.nombre += 1
        Timer(1, "i", self.afficher, condition= lambda : Niveau.etat in self.etats)

    def afficher(self):
        self.valeur_o = self.fonction(getattr(self.module, self.variable))
        getattr(self.module, self.variable)
        self.taille = self._get_surface().get_rect().width
        if self.cle:
            if type(self.valeur_o) == dict:
                self.valeur_o = self.valeur_o[self.cle]
            elif type(self.valeur_o) == list:
                self.valeur_o = self.valeur_o[int(self.cle)]
        self.valeur = str(self.valeur_o)
        if self.description == "":
            self.mise_a_jour(f"{self.variable} : {self.valeur}", (Screen.largeur() - self.taille, self.y))
        else:
            self.mise_a_jour(f"{self.description}{self.valeur}", (Screen.largeur() - self.taille, self.y))
        super().afficher()
