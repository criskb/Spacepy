# entities/health_item.py

import pygame
import colorsys
import random
from utils import draw_glow_circle, lighten_color

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
        center = (int(self.x), int(self.y))
        draw_glow_circle(surface, lighten_color(rgb, 0.3), center, self.radius, glow_radius=10, alpha=140)
        pygame.draw.circle(surface, rgb, center, self.radius)
        cross_color = (255, 255, 255)
        thickness = 4
        pygame.draw.rect(
            surface,
            cross_color,
            (self.x - thickness / 2, self.y - self.radius * 0.6, thickness, self.radius * 1.2),
            border_radius=2,
        )
        pygame.draw.rect(
            surface,
            cross_color,
            (self.x - self.radius * 0.6, self.y - thickness / 2, self.radius * 1.2, thickness),
            border_radius=2,
        )
