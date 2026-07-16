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
        Joueur.ply = self

    def bouger(self):

        self.transportage()
        self.deplacer()
        self.gerer_ecrasement()
        self.limit_move()
        Screen.camera = max(0, min(self.rect.x - Screen.largeur() // 2, Niveau.actuel.taille - Screen.largeur()))

    def transportage(self):
        for plat in Niveau.actuel.ascensseurs:
            if plat.est_porter():
                self.rect.move_ip(plat.move)

    def deplacer(self):
        prev_rect = self.rect.copy()

        # Horizontal
        self.rect.x += self.vitesse[0]
        for plat in Niveau.actuel.objets:
            y_overlap_avant = prev_rect.bottom > plat.rect.top and prev_rect.top < plat.rect.bottom
            if self.rect.colliderect(plat.rect) and not y_overlap_avant:
                if self.vitesse[0] > 0:
                    self.rect.right = plat.rect.left
                    self.vitesse[0] = 0
                elif self.vitesse[0] < 0:
                    self.rect.left = plat.rect.right
                    self.vitesse[0] = 0

        # Vertical
        self.rect.y += self.vitesse[1]
        self.au_sol = False
        for plat in Niveau.actuel.objets:
            if self.rect.colliderect(plat.rect):
                if self.vitesse[1] > 0:
                    self.rect.bottom = plat.rect.top
                    self.vitesse[1] = 0
                    self.au_sol = True
                elif self.vitesse[1] < 0:
                    self.rect.top = plat.rect.bottom
                    self.vitesse[1] = 0

    def gerer_ecrasement(self):
        overlapping = [p for p in Niveau.actuel.objets if self.rect.colliderect(p.rect)]
        if len(overlapping) >= 2:
            self.reinitialiser_jeu()
            return
        elif len(overlapping) == 1:
            overlap_rect = self.rect.clip(overlapping[0].rect)
            if overlap_rect.width > self.rect.width * 0.5 or overlap_rect.height > self.rect.height * 0.5:
                self.reinitialiser_jeu()

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