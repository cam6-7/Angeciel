import pygame

from UI.class_Bouton import Bouton
from core.class_Screen import Screen
from core.class_Texte import Texte
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Joueur import Joueur
from entities.class_Niveau import Niveau


class VictoryMenu():
    BOUTONS = [
            Texte(f"Vous avez fini le niveau {Niveau.en_cours}", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 150), taillepolice=70),
            Bouton("Niveau suivant", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 310), (0, 0, 255)),
            Bouton(f"Refaire le niveau {Niveau.en_cours}", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 400), (0, 255, 0)),
            Bouton("Quitter le jeu", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 490), (255, 0, 0)),
        ]

    def run(self, joueur: Joueur):
        self._maj()
        self._check_events(joueur)
        self._display()

    def _maj(self):
        self.BOUTONS[0].mise_a_jour(f"Vous avez fini le niveau {Niveau.en_cours}")
        if Niveau.en_cours == Niveau.nombre:
            self.BOUTONS[1].mise_a_jour("Recommencer le jeu")
        else:
            self.BOUTONS[1].mise_a_jour("Niveau suivant")
        self.BOUTONS[2].mise_a_jour(f"Refaire le niveau {Niveau.en_cours}")

    def _check_events(self, joueur: Joueur):
        if self.BOUTONS[1].est_clique:
            Niveau.suivant()
            joueur.reinitialiser_jeu()
        if self.BOUTONS[2].est_clique:
            joueur.reinitialiser_jeu()
        if self.BOUTONS[3].est_clique:
            Niveau.changer_etat("close")

    def _display(self):
        rect = pygame.Rect(0, 0, Screen.largeur(), Screen.hauteur())
        dessiner_plateforme_texturee(rect)
        for bouton in self.BOUTONS:
            bouton.afficher()
