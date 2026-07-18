def deplacer(self):
    prev_rect = self.rect.copy()

    # Horizontal (inchangé, avec le check y_overlap_avant qu'on avait déjà)
    self.rect.x += self.vitesse[0]
    for plat in Niveau.actuel.objets:
        y_overlap_avant = prev_rect.bottom > plat.rect.top and prev_rect.top < plat.rect.bottom
        if self.rect.colliderect(plat.rect) and not y_overlap_avant:
            if self.vitesse[0] > 0:
                self.rect.right = plat.rect.left
                self.vitesse[0] = 0
            elif self.vitesse[0] < 0:
                self.rect.left = plat.rect.right
                self.vitesse[0] = 0

    # Vertical — décision basée sur la position AVANT collision (celle de la frame précédente),
    # pas sur le signe de vitesse[1]
    prev_top, prev_bottom = self.rect.top, self.rect.bottom
    self.rect.y += self.vitesse[1]
    self.au_sol = False
    for plat in Niveau.actuel.objets:
        if not self.rect.colliderect(plat.rect):
            continue

        # position de la plateforme À LA FRAME PRÉCÉDENTE (avant son propre déplacement)
        plat_move = getattr(plat, "move", [0, 0])
        prev_plat_top = plat.rect.top - plat_move[1]
        prev_plat_bottom = plat.rect.bottom - plat_move[1]

        etait_au_dessus = prev_bottom <= prev_plat_top
        etait_en_dessous = prev_top >= prev_plat_bottom

        if etait_au_dessus:
            self.rect.bottom = plat.rect.top
            self.vitesse[1] = 0
            self.au_sol = True
        elif etait_en_dessous:
            self.rect.top = plat.rect.bottom
            self.vitesse[1] = 0