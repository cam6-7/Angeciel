from class_Texte import Texte
from cp import *
from class_Screen import Screen
from fonction_ressource_path import resource_path
s_click = pygame.mixer.Sound(resource_path("resources/click.mp3"))

class Bouton(Texte):

    def __init__(self, text, position, couleur=BLACK, taille = 30, police = "arial", centre = ""):
        super().__init__(text, position, couleur, taille, police, centre)
        self.gtaille = self.taille + 10
        self.ptaille = self.taille

    def afficher(self):
        self._changetaille()
        self.centrer()
        Screen.screen.blit(self.ecri, (self.x, self.y))

    def _changetaille(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.taille < self.gtaille:
                self.taille += 2
        else:
            if self.taille > self.ptaille:
                self.taille -= 2
        self.font = pygame.font.SysFont(self.police, self.taille)
        self.ecri = self._get_surface()
        self.rect = self.ecri.get_rect(topleft=(self.x, self.y))

    last_clic = 0
    def est_clique(self):
        touch = False
        t = pygame.time.get_ticks()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if t - Bouton.last_clic > 200:
                    touch = True
                    s_click.play()
                    Bouton.last_clic = pygame.time.get_ticks()
        return touch