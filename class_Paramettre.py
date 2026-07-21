from class_Ascensseur import Ascensseur
from class_Bouton import Bouton
from class_Editeur import Editeur
from class_Niveau import Niveau
from class_Plateforme import Plateforme
from class_Question import Question
from class_Screen import Screen
from cp import couleurs as c
from fonction_texture import dessiner_plateforme_texturee
from pygame import Rect
class Paramettre:
    p = None
    def __init__(self):
        self.boutons = {
            "retour" : Bouton("retour", [0, 50]),
            "taille": Bouton("taille", [0, 200]),
            "nom": Bouton("nom", [0, 250]),
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
            Niveau.changer_etat(Niveau.liste_etats.pop(), save=False)
        elif self.boutons["supprimer"].est_clique():
            niveau = Niveau.actuel
            Niveau.changer(Niveau.en_cours - 1)
            Niveau.liste.remove(niveau)
            Niveau.nombre -= 1
            Editeur.e.recreation_bouton()
            self.gerer_decalage()
            Niveau.changer_etat("editeur")
        elif self.boutons["dupliquer"].est_clique():
            Plateforme.liste[Niveau.nombre + 1] = Niveau.actuel.plateformes
            Ascensseur.liste[Niveau.nombre + 1] = Niveau.actuel.ascensseurs
            Niveau(Plateforme.liste[Niveau.nombre + 1], Ascensseur.liste[Niveau.nombre + 1], Niveau.actuel.taille, Niveau.actuel.couleur)
            Niveau.changer(Niveau.nombre)
            Editeur.e.recreation_bouton()
            self.gerer_decalage()
            Niveau.changer_etat("editeur")
        elif self.boutons["taille"].est_clique():
            Question("La taille du niveau?", "Niveau.actuel.taille", typ = int)
        elif self.boutons["nom"].est_clique():
            Question("Le nom du niveau?", "Niveau.actuel.name")

    @staticmethod
    def gerer_decalage():
        Editeur.e.decalage = Niveau.nombre
        Editeur.e.boutons_n.decaler(Editeur.e.decalage)
        while (Screen.largeur() - 50) - Editeur.e.boutons_n.boutons[-1].rect.right >= Editeur.e.boutons_n.boutons[
            -1].rect.width:
            Editeur.e.decalage -= 1
            Editeur.e.boutons_n.decaler(Editeur.e.decalage)