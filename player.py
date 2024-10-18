"""
Ce module définit la classe Player utilisée dans le jeu.

La classe Player gère le joueur, son mouvement, et la création de balles.
"""

import pygame
from bullet import Bullet

class PlayerSettings:
    """Classe pour encapsuler la configuration des paramètres du joueur."""

    def __init__(self, speed: int, bullet_speed: int):
        """Initialise les paramètres du joueur.

        Args:
            speed (int): La vitesse de déplacement du joueur.
            bullet_speed (int): La vitesse de déplacement des balles.
        """
        self.speed = speed
        self.bullet_speed = bullet_speed

class PlayerConfig:
    """Classe pour encapsuler la configuration du joueur."""

    def __init__(self, plane_img: pygame.Surface, player_rect: list,
                 init_pos: tuple, screen_size: tuple):
        """Initialise la configuration du joueur.

        Args:
            plane_img (pygame.Surface): L'image du joueur.
            player_rect (list): Liste des rectangles représentant les différentes images du joueur.
            init_pos (tuple): Position initiale du joueur (x, y).
            screen_size (tuple): Taille de l'écran (largeur, hauteur).
        """
        self.plane_img = plane_img
        self.player_rect = player_rect
        self.init_pos = init_pos
        self.screen_width, self.screen_height = screen_size

class Player(pygame.sprite.Sprite):
    """Classe représentant un joueur dans le jeu."""

    def __init__(self, config: PlayerConfig, settings: PlayerSettings):
        """Initialise un joueur avec une configuration et des paramètres donnés.

        Args:
            config (PlayerConfig): La configuration du joueur.
            settings (PlayerSettings): Les paramètres du joueur.
        """
        super().__init__()
        self.image = [config.plane_img.subsurface(rect).convert_alpha()
                      for rect in config.player_rect]
        self.rect = config.player_rect[0].copy()
        self.rect.topleft = config.init_pos
        self.settings = settings
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        self.screen_width = config.screen_width
        self.screen_height = config.screen_height

    def move_up(self) -> None:
        """Déplace le joueur vers le haut."""
        if self.rect.top > 0:
            self.rect.top -= self.settings.speed

    def move_down(self) -> None:
        """Déplace le joueur vers le bas."""
        if self.rect.top < self.screen_height - self.rect.height:
            self.rect.top += self.settings.speed

    def move_left(self) -> None:
        """Déplace le joueur vers la gauche."""
        if self.rect.left > 0:
            self.rect.left -= self.settings.speed

    def move_right(self) -> None:
        """Déplace le joueur vers la droite."""
        if self.rect.left < self.screen_width - self.rect.width:
            self.rect.left += self.settings.speed

    def shoot(self, bullet_img: pygame.Surface) -> None:
        """Tire une balle à la position actuelle du joueur.

        Args:
            bullet_img (pygame.Surface): L'image de la balle.
        """
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def check_hit(self) -> None:
        """Vérifie si le joueur a été touché (placeholder pour une logique future)."""
        return self.is_hit

    def update(self) -> None:
        """Met à jour l'état du joueur, comme vérifier les collisions ou l'état."""
        self.check_hit()

    def get_bullet_count(self) -> int:
        """Retourne le nombre de balles que le joueur a tirées.

        Returns:
            int: Le nombre de balles.
        """
        return len(self.bullets)

    def get_position(self) -> tuple:
        """Retourne la position actuelle du joueur.

        Returns:
            tuple: La position (x, y) du joueur.
        """
        return self.rect.topleft

    def reset_hit_status(self) -> None:
        """Réinitialise l'état de collision du joueur."""
        self.is_hit = False

    def add_bullet(self, bullet: Bullet) -> None:
        """Ajoute une balle au groupe de balles du joueur.

        Args:
            bullet (Bullet): La balle à ajouter.
        """
        self.bullets.add(bullet)

    def remove_bullet(self, bullet: Bullet) -> None:
        """Retire une balle du groupe de balles du joueur.

        Args:
            bullet (Bullet): La balle à retirer.
        """
        self.bullets.remove(bullet)

    def modify_speed(self, new_speed: int) -> None:
        """Modifie la vitesse du joueur.

        Args:
            new_speed (int): La nouvelle vitesse du joueur.
        """
        self.settings.speed = new_speed
