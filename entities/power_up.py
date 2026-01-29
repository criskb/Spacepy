# entities/power_up.py

import pygame
import random
import math

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
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw icon representing the power-up type
        font = pygame.font.Font(None, 24)
        if self.type == 'rapid_fire':
            text = font.render('R', True, (0, 0, 0))
        elif self.type == 'shotgun':
            text = font.render('S', True, (0, 0, 0))
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(text, text_rect)
