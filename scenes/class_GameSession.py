import pygame

from UI.class_TexteD import TexteD
from core.class_Screen import Screen
from core.fonction_texture import dessiner_plateforme_texturee
from entities.class_Joueur import Joueur
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage
from entities.class_Plateforme import Plateforme


class GameSession:
    aide1 = TexteD('Utilisez les\nflèches directionnelles\npour vous déplacer', (50, 425), taillepolice=20)
    aide2 = TexteD("Appuyez sur espace\npour sauter", (500, 440), taillepolice=20)
    aide3 = TexteD("Attention\nà ne pas tomber", (1200, 330), taillepolice=20)
    aide4 = TexteD("Sautez\nIl n'y a aucun dégat de chute!", (3300, 50), taillepolice=20)
    aide5 = TexteD("Bravo,\nvous avez fini le tutoriel,\nbonne chance pour\nla suite !", (4700, 150), taillepolice=20)

    def run(self, player: Joueur):
        self._display(player)
        self._moveplayer(player)


    def _moveplayer(self, player : Joueur):
        VITESSE_MARCHE = 5
        GRAVITE = 0.5
        FORCE_SAUT = 23
        keys = pygame.key.get_pressed()

        player.vx = 0
        if keys[pygame.K_LEFT]:
            player.vx -= VITESSE_MARCHE
        if keys[pygame.K_RIGHT]:
            player.vx += VITESSE_MARCHE

        player.vy += GRAVITE
        if keys[pygame.K_SPACE] and player.au_sol:
            player.vy += FORCE_SAUT
        player.rect.y += player.vy

        self._checkcollids(player, Niveau.actuel.plateformes)
        player.limit_move()
        #joueur.bouger()

    def _checkcollids(self, player: Joueur, plateformes: list[Plateforme]):
        for x in range(abs(int(player.vx))):
            if player.vx > 0:
                player.rect.x += 1
            else:
                player.rect.x -= 1
        for y in range(abs(int(player.vy))):
            if player.vy > 0:
                player.rect.y += 1
            else:
                player.rect.y -= 1

    def _display(self, joueur : Joueur):
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
