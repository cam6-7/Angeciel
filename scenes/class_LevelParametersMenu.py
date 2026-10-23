import pygame
from UI.class_Bouton import Bouton
from UI.class_Message import Message
from entities.class_Niveau import Niveau
from core.class_Screen import Screen
from core.fonction_texture import dessiner_plateforme_texturee

class LevelParametersMenu:
    BOUTONS = {
            "retour" : Bouton("retour", [0, 50]),
            "dupliquer": Bouton("dupliquer", [0, 400]),
            "supprimer": Bouton("supprimer", [0, 450]),
        }
    ETATS = {
            "menu": "menu",
            "jeu": "menu",
            "editeur": "menu",
            "paramettre": "editeur",
            "victoire": "victoire",
        }

    def run(self):
        self.afficher()
        self.gerer_clic()

    def afficher(self):
        rect = pygame.Rect(0, 0, Screen.largeur(), Screen.hauteur())
        dessiner_plateforme_texturee(rect)
        for bouton in self.BOUTONS.values():
            bouton.afficher()

    def gerer_clic(self):
        if self.BOUTONS["retour"].est_clique:
            Niveau.changer_etat(self.ETATS[Niveau.etat])

        elif self.BOUTONS["supprimer"].est_clique:
            if Niveau.nombre == 1:
                Message("Erreur, le dernier niveau ne peut etre supprimer")
                return
            niveau = Niveau.actuel
            if niveau in Niveau.liste:
                Niveau.changer(Niveau.en_cours - 1)
                Niveau.liste.remove(niveau)
                Niveau.nombre -= 1
                Niveau.changer_etat("editeur")
            else:
                Message("Erreur, Niveau inexistant")

        elif self.BOUTONS["dupliquer"].est_clique:
            niv = Niveau()
            niv.plateformes = Niveau.actuel.plateformes
            Niveau.changer(Niveau.nombre)
            Niveau.changer_etat("editeur")
