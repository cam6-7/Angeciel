import pygame

from UI.class_Bouton import Bouton
from core.class_Screen import Screen
from core.class_Texte import Texte
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Joueur import Joueur
from entities.class_Niveau import Niveau


class MainMenu:
    
    BOUTONS  : dict[str, Texte | Bouton] = {
            'titre' : Texte("Bienvenue sur Angeciel", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 100), taillepolice=70),
            'commencer' : Bouton("Commencer le jeu", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 310), (0,0, 255)),
            'quitter' : Bouton("Quitter le jeu", lambda s: (Screen.largeur() //2 - s.taille[0] // 2, 390), (255, 0, 0)),
            'editeur' : Bouton("éditeur de niveau", (20, 20), taillepolice= 10)
    }
    
    def run(self, joueur: Joueur):
        self._maj()
        self._display()
        return self._check_events(joueur)

        
    def _maj(self):
        self.BOUTONS['titre'].mise_a_jour(f"Commencer le niveau {Niveau.en_cours}")

    def _check_events(self , joueur: Joueur):
        if self.BOUTONS['commencer'].est_clique:
            joueur.reinitialiser_jeu()
        if self.BOUTONS['quitter'].est_clique:
            Niveau.changer_etat("close")
        if self.BOUTONS['editeur'].est_clique:
            Niveau.changer_etat("editeur")
            return True

    def _display(self):
        rect = pygame.Rect(0, 0, Screen.largeur(), Screen.hauteur())
        dessiner_plateforme_texturee(rect)
        for bouton in self.BOUTONS.values():
            bouton.afficher()
