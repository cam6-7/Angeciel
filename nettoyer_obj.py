import os, glob, json

from class_Niveau import Niveau
from class_Plateforme import Plateforme
from class_Ascensseur import Ascensseur

dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))
nb_bon_niv = 4
for numero in range(nb_bon_niv + 1, nombre_de_niveau + 1):
    os.remove(dossier + "/objets/niveau" + str(numero) + ".json")
    os.remove(dossier + "/objets/ascensseur" + str(numero) + ".json")
    os.remove(dossier + "/objets/plateforme" + str(numero) + ".json")
print("\033[32msupression de", nombre_de_niveau - len(glob.glob(dossier + "/objets/niveau*.json")), "niveaux réussi\033[0m")






for i in range(1, nb_bon_niv+1):
    with open("objets/ascensseur"+str(i)+".json", "r") as f:
        data = json.load(f)
    for asc in data:
        Ascensseur(
            niveau =asc["niveau"],
            taille=(asc["taille"]),
            pos1=(asc["pos1"]),
            pos2 =(asc["pos2"])

        )
# plateformes
for i in range(1, nombre_de_niveau+1):
    with open("objets/plateforme"+str(i)+".json", "r") as f:
        data = json.load(f)
    for plat in data:
        Plateforme(
            niveau = i,
            x = plat["x"],
            y = plat["y"],
            l = plat["largeur"],
            h = plat["hauteur"],
        )

# niveaux
for i in range(1, nombre_de_niveau+1):
    with open("objets/niveau"+str(i)+".json", "r") as f:
        data = json.load(f)
        Niveau(
            Plateforme.liste[i],
            Ascensseur.liste[i],
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
        else:
            pos.append(obj.rect.topleft)
            taille.append(obj.rect.size)
print("\033[32msupression de", nombre_de_suppression, "objets réussi\033[0m")


for i in range(1, Niveau.nombre + 1):
    with open("objets/ascensseur"+ str(i) +".json", "w") as f:
        json.dump([asc.to_dict() for asc in Ascensseur.liste[i]], f, indent=4)
    with open("objets/plateforme"+str(i)+".json", "w") as f:
        json.dump([plat.to_dict() for plat in Plateforme.liste[i]], f, indent=4)
    with open("objets/niveau"+str(i)+".json", "w") as f:
        json.dump(Niveau.liste[i-1].to_dict(), f, indent=4)