from  pygame import Rect
from class_Niveau import Niveau
from class_Screen import Screen
class Joueur:
    gravite = 1
    ply = None
    def __init__(self):
        self.vitesse = [0, 0]
        self.decal = [0,0]
        self.rect = Rect(50, 50, 25, 25)
        self.frect = Rect(50, 50, 25, 25)
        self.au_sol = False
        self.force = [5, -17]
        self.taille = 25
        self.collids = {"gauche": 0, "droite": 0, "haut": 0, "bas" : 0}
        Joueur.ply = self

    def bouger(self):
        self.frect = self.rect.copy()


        self.frect.x += self.vitesse[0]
        for obj in Niveau.actuel.objet:
            if obj.rect.colliderect(self.frect):
                obj.collision("h")

        self.frect.y += self.vitesse[1]
        for obj in Niveau.actuel.objet:
            if obj.rect.colliderect(self.frect):
                obj.collision("v")

        for obj in Niveau.actuel.objet:
            col = obj.toucher(self.rect)
            if col:
                for dir in col:
                    self.collids[dir] = 1 if self.collids[dir] <= 1 else 2

        if self.collids["haut"] + self.collids["bas"] > 2:
            self.reinitialiser_jeu()
        elif self.collids["gauche"] + self.collids["droite"] > 2:
            self.reinitialiser_jeu()


        self.rect = self.frect.copy()
        self.limit_move()

    def limit_move(self):
        # si on va trop a gauche
        if self.rect.left + self.vitesse[0] < 0:
            self.rect.left = 0
            self.vitesse[0] = 0
        # si on va trop a droite
        elif self.rect.right > Niveau.actuel.taille:
            Niveau.etat = "victoire"

        # si on va trop haut
        if self.rect.y < 0:
            self.rect.y = 0
            self.vitesse[1] = 0
        # si on va trop bas
        elif self.rect.top >= Screen.hauteur():
            self.reinitialiser_jeu()


    @property
    def rect_ecran(self):
        return self.rect.move(-Screen.camera, 0)

    @property
    def position(self):
        return self.rect.topleft

    def reinitialiser_jeu(self):
        self.vitesse = [0, 0]
        self.frect.topleft = (50, 50)
        self.rect.topleft = (50, 50)
        Niveau.etat = "jeu" if not Niveau.etat == "test" else "test"