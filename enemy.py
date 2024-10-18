"""
Ce module définit la classe Enemy utilisée dans le jeu.

La classe Enemy gère la création et le mouvement des ennemis dans le jeu.
Les ennemis se déplacent vers le bas de l'écran et peuvent être détruits par les balles du joueur.
"""

import pygame

class Enemy(pygame.sprite.Sprite):
    """Classe représentant un ennemi dans le jeu.

    Cette classe gère l'initialisation et le mouvement d'un ennemi qui se déplace 
    vers le bas de l'écran.

    Attributs :
        image (pygame.Surface) : L'image représentant l'ennemi.
        rect (pygame.Rect) : Le rectangle définissant la position et les dimensions 
                             de l'ennemi.
        down_imgs (list) : Liste des images affichées lorsque l'ennemi est abattu.
        speed (int) : La vitesse à laquelle l'ennemi se déplace vers le bas.
        down_index (int) : Index pour suivre l'animation de l'explosion de l'ennemi.
    """

    def __init__(self, enemy_img: pygame.Surface, enemy_down_imgs: list,
                 init_pos: tuple[int, int]):
        """Initialise un ennemi avec une image, une liste d'images pour 
        l'explosion, et une position initiale.

        Args :
            enemy_img (pygame.Surface) : L'image représentant l'ennemi.
            enemy_down_imgs (list) : Liste des images à afficher lorsque l'ennemi 
                                      est abattu.
            init_pos (tuple[int, int]) : La position initiale de l'ennemi.
        """
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(topleft=init_pos)
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self) -> None:
        """Déplace l'ennemi vers le bas en augmentant sa position verticale (y)."""
        self.rect.top += self.speed

    def reset(self, init_pos: tuple[int, int]) -> None:
        """Réinitialise la position de l'ennemi.

        Args :
            init_pos (tuple[int, int]) : La nouvelle position initiale de l'ennemi.
        """
        self.rect.topleft = init_pos
