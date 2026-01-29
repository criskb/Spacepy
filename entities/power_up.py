# entities/power_up.py

import pygame
import random
import math
from utils import draw_glow_circle, lighten_color, darken_color

class PowerUp:
    def __init__(self, x, y, speed, type):
        self.x = x
        self.y = y
        self.speed = speed
        self.type = type  # 'rapid_fire' or 'shotgun'
        self.radius = 15
        self.color = (255, 215, 0)  # Gold color

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        center = (int(self.x), int(self.y))
        glow_color = lighten_color(self.color, 0.4)
        draw_glow_circle(surface, glow_color, center, self.radius, glow_radius=12, alpha=160)

        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            px = self.x + math.cos(angle) * self.radius
            py = self.y + math.sin(angle) * self.radius
            points.append((px, py))
        pygame.draw.polygon(surface, self.color, points)
        pygame.draw.polygon(surface, darken_color(self.color, 0.2), points, width=2)

        # Draw icon representing the power-up type
        font = pygame.font.Font(None, 24)
        if self.type == 'rapid_fire':
            text = font.render('R', True, (15, 15, 15))
        elif self.type == 'shotgun':
            text = font.render('S', True, (15, 15, 15))
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)
