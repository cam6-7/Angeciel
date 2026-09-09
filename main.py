import pygame

from entities.class_Niveau import Niveau
from class_Game import Game

pygame.init()

# ==================== VARIABLES DU JEU ====================

game = Game()
print("\ndébut\n")
# ==================== BOUCLE PRINCIPALE ====================
while Niveau.etat != "close":
    game.run()

game.save()

