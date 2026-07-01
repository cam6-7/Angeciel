joueur = ply.rect.move(0, ply.vitesse[1])
for asc in Niveau.actuel.ascensseurs:
    if joueur.colliderect(asc):
        ply.vitesse[1], joueur, ply.au_sol = asc.collision_verticale(ply.vitesse[1], joueur, ply.au_sol)
for plat in Niveau.actuel.plateformes:
    if joueur.colliderect(plat.rect):
        ply.vitesse[1], joueur, ply.au_sol = plat.collision_verticale(ply.vitesse[1], joueur, ply.au_sol)

ply.rect.y = joueur.y

joueur = ply.rect.move(ply.vitesse[0],0)
for plat in Niveau.actuel.plateformes:
    if joueur.colliderect(plat.rect):
        joueur.left = plat.collision_horizontale(ply.vitesse[0])
for asc in Niveau.actuel.ascensseurs:
    if joueur.colliderect(asc):
        joueur.left = asc.collision_horizontale(ply.vitesse[0])
ply.rect.x = joueur.x