from core.class_Screen import Screen
import pygame

class Texte:
    def __init__(self, text : str, position: tuple, couleur: tuple | list= (0, 0, 0), taillepolice: int = 30, police: str = "arial", centre:str = ""):
        self.text = text
        self.position = list(position)
        self.couleur = couleur
        self.taillepolice = taillepolice
        self.police = police
        self.centre = centre
        if position[0] == "x":
            self.centre += "x"
            self.position[0] = Screen.largeur() // 2
        if position[1] == "y":
            self.centre += "y"
            self.position[1] = Screen.hauteur() // 2
    @property

    def rect(self) -> pygame.Rect:
        rect = self.surface.get_rect(topleft = self.position)
        if "x" in self.centre :
            rect.centerx = Screen.largeur() // 2
        if "y" in self.centre :
            rect.centery = Screen.hauteur() // 2
        return rect

    @property
    def surface(self):
        font = pygame.font.SysFont(self.police, self.taillepolice)
        surfaces = [font.render(line, True, self.couleur) for line in self.text.split("\n")]
        width = max(s.get_width() for s in surfaces)
        height = sum(s.get_height() for s in surfaces)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        y = 0
        for s in surfaces:
            surface.blit(s, (0, y))
            y += s.get_height()
        return surface

    def mise_a_jour(self, nouveau_text  : str | bool = False, nouvelle_pos : tuple  | list | bool = False):
        if nouveau_text or nouveau_text == "":
            self.text = nouveau_text
        if nouvelle_pos:
            self.position = nouvelle_pos

    def afficher(self):
        Screen.screen.blit(self.surface, self.rect)