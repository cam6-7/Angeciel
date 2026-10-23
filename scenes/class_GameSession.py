from UI.class_TexteD import TexteD
from core.class_Screen import Screen
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Joueur import Joueur
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage


class GameSession:
    aide1 = TexteD('Utilisez les\nflèches directionnelles\npour vous déplacer', (50, 425), taillepolice=20)
    aide2 = TexteD("Appuyez sur espace\npour sauter", (500, 440), taillepolice=20)
    aide3 = TexteD("Attention\nà ne pas tomber", (1200, 330), taillepolice=20)
    aide4 = TexteD("Sautez\nIl n'y a aucun dégat de chute!", (3300, 50), taillepolice=20)
    aide5 = TexteD("Bravo,\nvous avez fini le tutoriel,\nbonne chance pour\nla suite !", (4700, 150), taillepolice=20)

    def run(self, joueur: Joueur):
        joueur.bouger()
        self.display(joueur)

    def display(self, joueur : Joueur):
        Screen.screen.fill(Niveau.actuel.couleur)

        # Nuages
        for pos in Nuage.liste:
            pos.afficher()

        # Plateformes et ascenseurs
        for obj in Niveau.actuel.plateformes:
            dessiner_plateforme_texturee(obj.rect.move(- Screen.camera, 0))

        # Joueur
        joueur.afficher()

        # Aides pour le niveau 1
        if Niveau.en_cours == 1:
            self.aide1.move(Screen.camera, joueur.rect_ecran)
            self.aide2.move(Screen.camera, joueur.rect_ecran)
            self.aide3.move(Screen.camera, joueur.rect_ecran)
            self.aide4.move(Screen.camera, joueur.rect_ecran)
            self.aide5.move(Screen.camera, joueur.rect_ecran)
