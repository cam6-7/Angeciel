import sys, json, glob, os, pygame

from core.class_Screen import Screen
from entities.class_Niveau import Niveau
from entities.class_Nuage import Nuage
from entities.class_Plateforme import Plateforme
from class_Game import Game

pygame.init()

# ==================== VARIABLES DU JEU ====================
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))

# ================= IMPORTS ===================
# ascensseurs

# plateformes
for i in range(1, nombre_de_niveau+1):
    with open("objets/plateforme"+str(i)+".json", "r") as f:
        [Plateforme(plat["niveau"], plat["taille"], plat["positions"], plat["avance"]) for plat in json.load(f)]

# niveaux
for i in range(1, nombre_de_niveau+1):
    with open("objets/niveau"+str(i)+".json", "r") as f:
        data = json.load(f)
        Niveau(
            Plateforme.liste[i],
            data["taille"],
            data["couleur"],
            name = data["name"]
        )


nb_nuage = 7
for i in range(nb_nuage):
    Nuage()
game = Game()
print("\ndébut\n")
# ==================== BOUCLE PRINCIPALE ====================
while Niveau.etat != "close":
    game.run()

# sauvergarde des objets quand le jeu est fini
for i in range(1, Niveau.nombre + 1):
    with open("objets/plateforme"+str(i)+".json", "w") as f:
        json.dump([plat.to_dict() for plat in Plateforme.liste[i]], f, indent=4)
    with open("objets/niveau"+str(i)+".json", "w") as f:
        json.dump(Niveau.liste[i-1].to_dict(), f, indent=4)

nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))
for i in range(1, nombre_de_niveau + 1):
    if i > Niveau.nombre:
        os.remove("objets/ascensseur"+ str(i) +".json")
        os.remove("objets/plateforme"+ str(i) +".json")
        os.remove("objets/niveau"+ str(i) +".json")

print("fin sauvergardé")
Screen.screen.fill((0, 0, 0))
pygame.display.flip()
pygame.quit()
sys.exit()