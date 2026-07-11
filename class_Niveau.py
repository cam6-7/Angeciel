import pygame
pygame.init()

class Niveau:
    actuel = None
    en_cours = 1
    nombre = 0
    etat = "menu"

    liste = []
    def __init__(self, plateformes, ascensseurs, taille, couleur, name = f""):
        self.plateformes = plateformes
        self.ascensseurs = ascensseurs
        self.taille = taille
        self.couleur = couleur

        Niveau.nombre += 1
        Niveau.liste.append(self)
        self.numero = Niveau.nombre
        if name == "":
            self.name = f"niveau{Niveau.nombre}"
        else:
            self.name = name
        if self.numero == Niveau.en_cours:
            Niveau.actuel = self

    @property
    def objet(self):
        return self.plateformes + self.ascensseurs

    @classmethod
    def suivant(cls):
        cls.en_cours += 1
        if cls.en_cours > cls.nombre:
            cls.en_cours = 1
        for niv in cls.liste:
            if niv.numero == Niveau.en_cours:
                Niveau.actuel = niv

    @classmethod
    def changer(cls, nouveau_niveau):
        if nouveau_niveau <= cls.nombre:
            cls.en_cours = nouveau_niveau
        else: print("erreur : not " + str(nouveau_niveau) + " >= " + str(cls.nombre))
        for niv in cls.liste:
            if niv.numero == Niveau.en_cours:
                Niveau.actuel = niv
    def to_dict(self):
        return {
            "taille": self.taille,
            "couleur": self.couleur,
            "numero": self.numero,
        }










