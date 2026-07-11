from cp import *
from class_Screen import Screen

class Texte:
    def __init__(self, text, position, couleur=BLACK, taille = 30, police = "arial", centre = ""):
        self.text = text
        self.x = position[0]
        self.y = position[1]
        self.couleur = couleur
        self.taille = taille
        self.police = police
        self.font = pygame.font.SysFont(self.police, self.taille)
        self.centre = ""
        if type(self.x) == str:
            self.centre += "x"
        if type(self.y) == str:
            self.centre += "y"
        if self.centre == "":
            self.centre = centre
        self.base = position
        self.centrer()
        self.surface = self._get_surface()
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def _get_surface(self):
        if "\n" in self.text:
            lines = self.text.split("\n")
            surfaces = [self.font.render(line, True, self.couleur) for line in lines]
            width = max(s.get_width() for s in surfaces)
            height = sum(s.get_height() for s in surfaces)
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            y = 0
            for s in surfaces:
                surface.blit(s, (0, y))
                y += s.get_height()
        else:
            line = self.text
            s = self.font.render(line, True, self.couleur)
            surface = pygame.Surface((s.get_width(), s.get_height()), pygame.SRCALPHA)
            surface.blit(s, (0, 0))
        return surface

    def mise_a_jour(self, nouveau_text = "", nouvelle_pos = False):
        if nouveau_text != "":
            self.text = nouveau_text
            self.surface = self._get_surface()
            self.rect = self.surface.get_rect(topleft = (self.x, self.y))
        if nouvelle_pos:
            self.x = nouvelle_pos[0]
            self.y = nouvelle_pos[1]
            self.rect = self.surface.get_rect(topleft = nouvelle_pos)

    def afficher(self):
        self.centrer()
        Screen.screen.blit(self.surface, self.rect)

    def centrer(self):
        if "x" in self.centre :
            self.rect = self._get_surface().get_rect(midtop = (Screen.largeur() / 2,  self.y))
            self.x = self.rect.left
        if "y" in self.centre :
            self.rect = self._get_surface().get_rect(midleft = (self.x, Screen.hauteur() / 2))
            self.y = self.rect.top
        if self.centre == "spe":
            self.rect = self._get_surface().get_rect(midtop=(self.base[0] * Screen.largeur() / 1000, self.y))
            self.x = self.rect.left
            self.rect = self._get_surface().get_rect(midleft=(self.x, self.base[1] * Screen.hauteur() / 600))
            self.y = self.rect.top
