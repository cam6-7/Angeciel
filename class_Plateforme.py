import pygame, os, glob
pygame.init()
from class_Niveau import Niveau
from class_Joueur import Joueur
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))

class Plateforme:

    liste = {}
    for i in range(1, nombre_de_niveau + 1):
        liste[i] = []

    def toucher(self, rect):
        if self.rect.colliderect(rect.inflate(2,2)):
            distance = { "gauche" : self.rect.right - rect.left, "droite" : rect.right - self.rect.left , "haut" : self.rect.bottom - rect.top , "bas" : rect.bottom - self.rect.top}
            cles = [cle for cle, valeur in distance.items() if valeur >= 0]
            distance = {cle: distance[cle] for cle in cles}
            valeur_max = min(distance.values())
            return [cle for cle, valeur in distance.items() if valeur == valeur_max]
        else :
            return False



    def __init__(self, x, y, l, h, niveau):
        self.niveau = niveau
        self.rect = pygame.Rect(x, y, l, h)
        if type(self) is Plateforme:
            Plateforme.liste[self.niveau].append(self)

    def supprimer(self):
        if self in Niveau.actuel.ascensseurs :
            Niveau.actuel.ascensseurs.remove(self)
        if self in Niveau.actuel.plateformes:
            Niveau.actuel.plateformes.remove(self)

    def move(self, x, y, l, h):
        self.supprimer()
        self.rect = pygame.Rect(x, y, l, h)
        Plateforme.liste[self.niveau].append(self)


    def collidepoint(self, point):
        if self.rect.collidepoint(point):
            return True
        else:
            return False

    def copy(self):
        return Plateforme(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.niveau)

    def collision(self, direction):
        ply = Joueur.ply
        collids = ply.collids
        d = ""
        if direction == "h":
            # par la droite
            if ply.vitesse[0] >= 0:
                ply.frect.right = self.rect.x
                ply.vitesse[0] = 0
                d = "droite"

            # par la gauche
            elif ply.vitesse[0] < 0:
                ply.frect.x = self.rect.right
                ply.vitesse[0] = 0
                d = "gauche"


        elif direction == "v":
        # Collision par le dessus
            if ply.vitesse[1] > 0:
                ply.frect.bottom = self.rect.top
                ply.au_sol = True
                ply.vitesse[1] = 0
                d = "bas"

            # Collision par le dessous
            elif ply.vitesse[1] <= 0:
                ply.frect.top = self.rect.bottom
                ply.vitesse[1] = 0
                d = "haut"
        collids[d] = 1 if collids[d] == 0 else 2





    def to_dict(self):
        return {
            "type": "Plateforme",
            "niveau": self.niveau,
            "x": self.rect.x,
            "y": self.rect.y,
            "largeur": self.rect.width,
            "hauteur": self.rect.height,
        }
