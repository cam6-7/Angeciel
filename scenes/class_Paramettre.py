from UI.class_Bouton import Bouton
from UI.class_Message import Message
from entities.class_Niveau import Niveau
from core.class_Screen import Screen
from core.fonction_texture import dessiner_plateforme_texturee
from pygame import Rect
class Paramettre:
    p = None
    def __init__(self):
        self.boutons = {
            "retour" : Bouton("retour", [0, 50]),
            "dupliquer": Bouton("dupliquer", [0, 400]),
            "supprimer": Bouton("supprimer", [0, 450]),
        }
        Paramettre.p = self

    def afficher(self):
        dessiner_plateforme_texturee(Rect(0, 0, Screen.largeur(), Screen.hauteur()))
        for bouton in self.boutons.values():
            bouton.afficher()

    def gerer_clic(self):
        if self.boutons["retour"].est_clique():
            liste_etat = {"menu" : "menu",
                          "jeu" : "menu",
                          "editeur" : "menu",
                          "paramettre" : "editeur",
                          "victoire" : "victoire",
                          }
            Niveau.changer_etat(liste_etat[Niveau.etat])
        elif self.boutons["supprimer"].est_clique():
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
        elif self.boutons["dupliquer"].est_clique():
            niv = Niveau()
            niv.plateformes = Niveau.actuel.plateformes
            Niveau.changer(Niveau.nombre)
            Niveau.changer_etat("editeur")
