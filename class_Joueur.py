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
        self.au_sol = False
        self.force = [5, -17]
        self.taille = 25
        self.collids = {"gauche" : 0,
                   "droite" : 0,
                   "haut" : 0,
                   "bas" : 0}
        Joueur.ply = self

    @property
    def pos(self):
        return self.rect.topleft

    def bouger(self):

        self.transportage()
        self.gerer_collisions()
        self.limit_move()
        Screen.camera = max(0, min(self.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))

    def transportage(self):
        for plat in Niveau.actuel.ascensseurs:
            if plat.est_porter():
                self.rect.bottom = plat.rect.top
                self.vitesse[0] += plat.move[0]

    def gerer_collisions(self):
        self.au_sol = False
        vx, vy = self.vitesse

        for obj in Niveau.actuel.objets:
            if self.rect.colliderect(obj.rect):
                self.reinitialiser_jeu()

        frect = self.rect.move(vx, 0)
        mrect = frect.copy()


        for obj in Niveau.actuel.objets:
            if obj.rect.colliderect(frect):
                if vx > 0:
                    mrect.right = obj.rect.left
                    self.collids["droite"] = 1 if self.collids["droite"] == 0 else 2
                elif vx < 0:
                    mrect.left = obj.rect.right
                    self.collids["gauche"] = 1 if self.collids["gauche"] == 0 else 2
                elif vx == 0:
                    self.reinitialiser_jeu()

        for obj in Niveau.actuel.objets:
            if mrect.colliderect(obj.rect):
                self.reinitialiser_jeu()

        mrect.move_ip(0, vy)
        frect = mrect.copy()

        for obj in Niveau.actuel.objets:
            if obj.rect.colliderect(frect):
                if vy > 0:
                    mrect.bottom = obj.rect.top
                    self.au_sol = True
                    vy = 0
                    self.collids["bas"] = 1 if self.collids["bas"] == 0 else 2
                elif vy < 0:
                    vy = 0
                    mrect.top = obj.rect.bottom
                    self.collids["haut"] = 1 if self.collids["haut"] == 0 else 2
                elif vy == 0:
                    self.reinitialiser_jeu()

        for obj in Niveau.actuel.objets:
            if mrect.colliderect(obj.rect):
                self.reinitialiser_jeu()

        if (self.collids["gauche"] + self.collids["droite"] > 2
            or self.collids["bas"] + self.collids["haut"] > 2):
            self.reinitialiser_jeu()

        self.rect = mrect.copy()
        self.vitesse = [vx, vy]

    def touche(self, dx = 0, dy = 0):
        # fonction qui renvoie le nombre de plateform que touche le joueur
        # (on peut le déplacer pour tester des collisions futures ou antérieurs)
        rect = self.rect.move(dx, dy)
        touche = 0
        for obj in Niveau.actuel.objets:
            if rect.colliderect(obj.rect):
                touche += 1
        return touche

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

    def reinitialiser_jeu(self):
        self.vitesse = [0, 0]
        self.rect.topleft = (50, 50)
        Niveau.etat = "jeu" if not Niveau.etat == "test" else "test"