# entities/health_item.py

import pygame
import colorsys
import random

class HealthItem:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hue = random.uniform(0, 1)
        self.radius = 15

    def move(self):
        """Move the health item downward."""
        self.y += self.speed

    def update_hue(self):
        """Update the hue for RGB cycling effect."""
        self.hue += 0.005
        if self.hue > 1:
            self.hue -= 1

    def draw(self, surface):
        """Draw the health item with RGB cycling."""
        rgb_fractional = colorsys.hsv_to_rgb(self.hue, 1, 1)
        rgb = tuple(int(c * 255) for c in rgb_fractional)
        pygame.draw.circle(surface, rgb, (int(self.x), int(self.y)), self.radius)
