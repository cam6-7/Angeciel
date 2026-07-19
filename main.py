import sys, json, glob, os
from mes_class import *
clock = pygame.time.Clock()

# ==================== VARIABLES DU JEU ====================
dossier = os.path.dirname(os.path.abspath(__file__))
nombre_de_niveau = len(glob.glob(dossier + "/objets/niveau*.json"))
premiere_ouverture = True
ply = Joueur()

# ================= IMPORTS ===================
# ascensseurs

for i in range(1, nombre_de_niveau+1):
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
editeur = Editeur()
paramettre = Paramettre()
Debug("en_cours", Niveau, ["jeu", "test"], "Niveau ")

# images
image_player_d = pygame.image.load(resource_path("resources/image_player_d.png"))
image_player_g = pygame.image.load(resource_path("resources/image_player_g.png"))
image = image_player_d

# ==================== SON ====================
m_menu = pygame.mixer.Sound(resource_path("resources/menu.mp3"))
m_jeu = pygame.mixer.Sound(resource_path("resources/jeu.mp3"))
m_jeu.set_volume(0.2)
m_menu.set_volume(0.4)
m_menu.play(-1)

# ==================== INITIALISATION DES OBJETS ====================
#les menus
menu1 = Menu([
            Texte("Bienvenue sur Angeciel",["x", 100], taille=70),
            Bouton("Commencer le jeu", ["x", 300], couleur=BLUE),
            Bouton("Choix du niveau", ["x", 400], couleur=GREEN),
            Bouton("Quitter le jeu", ["x", 500], couleur=RED),
            Bouton("éditeur de niveau", [20, 20], taille= 10)
            ])
menu_v = Menu([
            Texte(f"Vous avez fini le niveau {Niveau.en_cours}", ["x", 150], taille=70),
            Bouton("Niveau suivant", ["x", 310], couleur=BLUE),
            Bouton(f"Refaire le niveau {Niveau.en_cours}", ["x", 400], couleur=GREEN),
            Bouton("Quitter le jeu", ["x", 490], couleur=RED),
            Bouton("éditeur de niveau", [20, 20], taille= 10)
            ])
menu_c = Menu([
            Bouton("retour", ["x", 50] ),
            Bouton("niveau1", [1000/3, 200], centre = "spe" ),
            Bouton("niveau2", [1000/3 * 2, 200], centre = "spe"),
            Bouton("niveau3", [1000/3, 400], centre = "spe"),
            Bouton("niveau4", [1000/3 * 2, 400], centre = "spe")
            ])


# textes de tutoriels
aide1 = TexteD('Utilisez les\nflèches directionnelles\npour vous déplacer', [50, 425], taille = 20)
aide2 = TexteD("Appuyez sur espace\npour sauter", (500, 440), taille = 20)
aide3 = TexteD("Attention\nà ne pas tomber", (1200, 330), taille = 20)
aide4 = TexteD("Sautez\nIl n'y a aucun dégat de chute!", (3300, 50), taille = 20)
aide5 = TexteD("Bravo,\nvous avez fini le tutoriel,\nbonne chance pour\nla suite !", (4700, 150), taille = 20)

# nuages
nb_nuage = 7
for i in range(nb_nuage):
    Nuage()

# zones de textes
"""
input_box1 = ZoneDeTexte("", (130, 230), "couleur", Niveau.actuel)
input_box2 = ZoneDeTexte("", (100, 370), "taille", Niveau.actuel)
input_box3 = ZoneDeTexte("", (100, 510), "name", Niveau.actuel)"""


print("\ndébut\n")
# ==================== BOUCLE PRINCIPALE ====================
while Niveau.etat != "close":
    events = []
    for event in pygame.event.get():
        events.append(event)
        if event.type == pygame.QUIT:
            Niveau.etat = "close"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if Niveau.etat == "jeu" or Niveau.etat == "editeur":
                premiere_ouverture = False
                Niveau.etat = "menu"
            elif Niveau.etat == "test":
                Niveau.etat = "editeur"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            print("\n " + str(pygame.mouse.get_pos()))
            print(pygame.mouse.get_pos()[0] + Screen.camera, pygame.mouse.get_pos()[1] + Screen.camera, "\n" )

    # ==================== MENUS ====================
    if Niveau.etat == "menu":
        menu1.afficher()
        if not premiere_ouverture:
            menu1.boutons[0].mise_a_jour(f"Reprendre le niveau {Niveau.en_cours}")
        if menu1.boutons[1].est_clique():
            ply.reinitialiser_jeu()
        if menu1.boutons[2].est_clique():
            Niveau.etat = "choix_niv"
        if menu1.boutons[3].est_clique():
            Niveau.etat = "close"
        if menu1.boutons[4].est_clique():
            Niveau.etat = "editeur"
            editeur.cam_x = -200
            e_type = "rien"

    if Niveau.etat == "choix_niv":
        menu_c.afficher()
        if menu_c.boutons[0].est_clique():
            Niveau.etat = "menu"
        for bouton in menu_c.boutons:
            if bouton.est_clique():
                Niveau.changer(menu_c.boutons.index(bouton))
                Niveau.etat = "menu"

    if Niveau.etat == "paramettre":
        paramettre.afficher()
        paramettre.gerer_clic()
    # ==================== EDITEUR =====================
    if Niveau.etat == "editeur":
        editeur.gestion_camera()
        editeur.afficher()
        editeur.gestion_creation(events)
        editeur.gestion_bouton()

    # ==================== VICTOIRE ====================
    if Niveau.etat == "victoire":
        menu_v.boutons[0].mise_a_jour(f"Vous avez fini le niveau {Niveau.en_cours}")
        if Niveau.en_cours == Niveau.nombre:
            menu_v.boutons[1].mise_a_jour("Recommencer le jeu")
        else:
            menu_v.boutons[1].mise_a_jour("Niveau suivant")
        menu_v.boutons[2].mise_a_jour(f"Refaire le niveau {Niveau.en_cours}")
        menu_v.afficher()
        if menu_v.boutons[1].est_clique():
            Niveau.suivant()
            ply.reinitialiser_jeu()
        if menu_v.boutons[2].est_clique():
            ply.reinitialiser_jeu()
        if menu_v.boutons[3].est_clique():
            Niveau.etat = "close"
        if menu_v.boutons[4].est_clique():
            Niveau.etat = "editeur"
            Screen.camera = 0


    # ==================== JEU =================================================================
    elif Niveau.etat == "jeu" or Niveau.etat == "test":
        m_menu.stop()


        ply.collids = {"gauche" : 0,
                        "droite" : 0,
                        "haut" : 0,
                        "bas": 0}

        # Mouvement des ascenseurs
        for asc in Niveau.actuel.ascensseurs:
            asc.mouvement()

         # Deplacements horizontaux
        ply.vitesse[0] = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ply.vitesse[0] -= ply.force[0]
            image = image_player_g
        if keys[pygame.K_RIGHT]:
            ply.vitesse[0] += ply.force[0]
            image = image_player_d

        # Sauts + gravite
        ply.vitesse[1] += ply.gravite
        if keys[pygame.K_SPACE] and ply.au_sol:
            ply.vitesse[1] += ply.force[1]

        # ==================== COLLISIONS + MOUVEMENTS ====================
        ply.bouger()

        # ==================== AFFICHAGE ==================================================================================
        Screen.screen.fill(Niveau.actuel.couleur)
        # Nuages

        for pos in Nuage.liste:
            pos.afficher()


        # Plateformes et ascenseurs
        for obj in Niveau.actuel.objets:
            dessiner_plateforme_texturee(obj.rect.move(- Screen.camera, 0))

        # Joueur
        Screen.screen.blit(image, ply.rect_ecran)

        # Aides pour le niveau 1
        if Niveau.en_cours == 1:
            aide1.move(Screen.camera, ply.rect_ecran)
            aide2.move(Screen.camera, ply.rect_ecran)
            aide3.move(Screen.camera, ply.rect_ecran)
            aide4.move(Screen.camera, ply.rect_ecran)
            aide5.move(Screen.camera, ply.rect_ecran)

    Timer.mise_a_jour()
    pygame.display.flip()
    clock.tick(60)

# sauvergarde des objets quand le jeu est fini
for i in range(1, Niveau.nombre + 1):
    with open("objets/ascensseur"+ str(i) +".json", "w") as f:
        json.dump([asc.to_dict() for asc in Ascensseur.liste[i]], f, indent=4)
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
pygame.quit()
sys.exit()