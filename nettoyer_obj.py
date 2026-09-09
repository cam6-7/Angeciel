import os, glob, json

from entities.class_Niveau import Niveau
from entities.class_Plateforme import Plateforme

dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))
nb_bon_niv = 4
for numero in range(nb_bon_niv + 1, nombre_de_niveau + 1):
    os.remove(dossier + "/objets/niveau" + str(numero) + ".json")
    os.remove(dossier + "/objets/plateforme" + str(numero) + ".json")
print("\033[32msupression de", nombre_de_niveau - len(glob.glob(dossier + "/objets/niveau*.json")), "niveaux réussi\033[0m")

for i in range(1, nombre_de_niveau+1):
    with open("objets/plateforme"+str(i)+".json", "r") as f:
        data = json.load(f)
    for plat in data:
        Plateforme(plat["niveau"], plat["taille"], plat["positions"])
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

nombre_de_suppression = 0
for niv in Niveau.liste:
    pos = []
    taille = []
    for obj in niv.objets:
        if obj.rect.topleft in pos and obj.rect.size in taille:
            obj.supprimer()
            nombre_de_suppression += 1
        elif obj.rect.topleft == (0, 0) or obj.rect.left < 0:
            obj.supprimer()
            nombre_de_suppression += 1
        else:
            pos.append(obj.rect.topleft)
            taille.append(obj.rect.size)
    Plateforme.liste[niv.numero] = sorted(niv.objets, key=lambda x: (- x.nb_positions, x.pos1[0]))
print("\033[32msupression de", nombre_de_suppression, "objets réussi\033[0m")


for i in range(1, Niveau.nombre + 1):
    with open( "objets/plateforme"+str(i)+".json", "w") as f:
        json.dump([plat.to_dict() for plat in Plateforme.liste[i]], f, indent=4)
    with open( "objets/niveau"+str(i)+".json", "w") as f:
        json.dump(Niveau.liste[i-1].to_dict(), f, indent=4)