import os, glob, json

from entities.class_Niveau import Niveau
from entities.class_Plateforme import Plateforme
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/plateforme*.json"))
nb_bon_niv = 4
nombre_de_suppression = 0

for numero in range(nb_bon_niv + 1, nombre_de_niveau + 1):
    os.remove(dossier + "/objets/plateforme" + str(numero) + ".json")
    nombre_de_suppression += 1
print("\033[32msupression de", nombre_de_suppression, "niveaux réussi\033[0m")


nombre_de_suppression = 0
nombre_de_niveau = len(glob.glob(dossier + "/objets/plateforme*.json"))
for niv in range(1, nombre_de_niveau + 1):
    Niveau()
    with open("objets/plateforme" + str(niv) + ".json", "r") as f:
        [Plateforme(plat["niveau"], plat["taille"], plat["positions"], plat["avance"]) for plat in json.load(f)]
for niv in Niveau.liste:
    pos = []
    taille = []
    for obj in niv.plateformes:
        if obj.rect.topleft in pos and obj.rect.size in taille:
            obj.supprimer()
            nombre_de_suppression += 1
        elif obj.rect.topleft == (0, 0) or obj.rect.left < 0:
            obj.supprimer()
            nombre_de_suppression += 1
        else:
            pos.append(obj.rect.topleft)
            taille.append(obj.rect.size)
    niv.plateformes = sorted(niv.plateformes, key=lambda x: (- x.nb_positions, x.pos1[0]))
print("\033[32msupression de", nombre_de_suppression, "objets réussi\033[0m")

for i in range(Niveau.nombre):
    with open( "objets/plateforme"+str(i+1)+".json", "w") as f:
        json.dump([plat.to_dict() for plat in Niveau.liste[i].plateformes], f, indent=4)