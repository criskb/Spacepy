# entities/bullet.py

import pygame
from utils import draw_glow_circle, lighten_color

class Bullet:
    def __init__(self, x, y, dx, dy, damage, owner):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 5
        self.damage = damage
        self.owner = owner  # 'player', 'enemy', or 'boss'

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        color = (255, 220, 80) if self.owner == 'player' else (255, 80, 100)
        glow_color = lighten_color(color, 0.3)
        center = (int(self.x), int(self.y))
        draw_glow_circle(surface, glow_color, center, self.radius, glow_radius=8, alpha=160)
        pygame.draw.circle(surface, color, center, self.radius)
        pygame.draw.circle(surface, (255, 255, 255), center, max(1, self.radius // 2))
