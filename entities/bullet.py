# entities/bullet.py

import pygame

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
        color = (255, 255, 0) if self.owner == 'player' else (255, 0, 0)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
