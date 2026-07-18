import os, glob
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))


nb_bon_niv = 4

for numero in range(nb_bon_niv + 1, nombre_de_niveau + 1):
    os.remove(dossier + "/objets/niveau" + str(numero) + ".json")
    os.remove(dossier + "/objets/ascensseur" + str(numero) + ".json")
    os.remove(dossier + "/objets/plateforme" + str(numero) + ".json")


print("\033[32msupression de", nombre_de_niveau - len(glob.glob(dossier + "/objets/niveau*.json")), "niveaux réussi\033[0m")