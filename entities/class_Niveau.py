class Niveau:
    actuel = None
    en_cours = 1
    nombre = 0
    etat = "menu"
    liste = []
    liste_etats = ["menu"]

    def __init__(self):

        self.plateformes = []
        self.couleur = (135, 206, 235)

        Niveau.nombre += 1
        Niveau.liste.append(self)
        self.numero = Niveau.nombre
        self.name = f"niveau{Niveau.nombre}"
        if self.numero == Niveau.en_cours:
            Niveau.actuel = self

    @classmethod
    def changer_etat(cls, nouvel_etat):
        cls.etat = nouvel_etat

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

    @property
    def taille(self):
        if len(self.plateformes) == 0: return  1000
        else: return max(obj.rect.right for obj in self.plateformes)
