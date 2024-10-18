"""
Ce module définit la classe Bullet utilisée dans le jeu.

La classe Bullet gère la création et le mouvement des balles tirées par le joueur.
Les balles se déplacent vers le haut de l'écran et sont détruites lorsqu'elles sortent de l'écran.
"""
import pygame

class Bullet(pygame.sprite.Sprite):
    """Classe représentant une balle dans le jeu.
    Cette classe gère le mouvement et l'initialisation d'une balle, 
    qui est tirée par le joueur et se déplace vers le haut de l'écran.

    Attributs :
        image (pygame.Surface) : L'image représentant la balle.
        rect (pygame.Rect) : Le rectangle définissant la position et les dimensions de la balle.
        speed (int) : La vitesse à laquelle la balle se déplace vers le haut.
    """
    def __init__(self, bullet_img: pygame.Surface, init_pos: tuple[int, int], speed: int = 10):
        """Initialise une balle avec une image et une position initiale.

        Args :
            bullet_img (pygame.Surface) : L'image représentant la balle.
            init_pos (tuple[int, int]) : La position initiale de la balle.
            speed (int, optionnel) : La vitesse à laquelle la balle se déplace. Par défaut à 10.
        """
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(midbottom=init_pos)
        self.speed = speed

    def move(self) -> None:
        """Déplace la balle vers le haut en diminuant sa position verticale (y)."""
        self.rect.top -= self.speed

    def update(self) -> None:
        """Met à jour l'état de la balle, en appelant la méthode move()."""
        self.move()
