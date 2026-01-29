# entities/enemy.py

import pygame
import random
import math
from entities.bullet import Bullet
from utils import draw_glow_circle, lighten_color, darken_color

class Enemy:
    def __init__(self, x, y, color_outer, color_inner, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius_outer = 20
        self.radius_inner = 10
        self.color_outer = color_outer
        self.color_inner = color_inner
        self.speed = 2  # Horizontal speed
        self.vertical_speed = 20  # Distance to move down when changing direction
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left
        self.bullets = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shoot_timer = random.randint(60, 120)  # Random shoot interval

    def move(self):
        # Move horizontally
        self.x += self.speed * self.direction
        # Check for screen boundaries
        if self.x - self.radius_outer <= 0 or self.x + self.radius_outer >= self.screen_width:
            # Move down when hitting an edge
            self.y += self.vertical_speed
            # Reverse direction
            self.direction *= -1
            # Correct position if out of bounds
            self.x = max(self.radius_outer, min(self.x, self.screen_width - self.radius_outer))

    def update(self, player_x, player_y):
        # Handle shooting
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot(player_x, player_y)
            self.shoot_timer = random.randint(60, 120)

    def shoot(self, target_x, target_y):
        # Shoot towards the player
        angle = math.atan2(target_y - self.y, target_x - self.x)
        dx = math.cos(angle) * 5
        dy = math.sin(angle) * 5
        bullet = Bullet(self.x, self.y, dx, dy, 1, 'enemy')
        self.bullets.append(bullet)

    def draw(self, surface):
        center = (int(self.x), int(self.y))
        glow_color = lighten_color(self.color_outer, 0.4)
        draw_glow_circle(surface, glow_color, center, self.radius_outer, glow_radius=10, alpha=120)

        ring_color = darken_color(self.color_outer, 0.2)
        pygame.draw.circle(surface, self.color_outer, center, self.radius_outer)
        pygame.draw.circle(surface, ring_color, center, self.radius_outer, width=3)

        inner_color = lighten_color(self.color_inner, 0.3)
        pygame.draw.circle(surface, inner_color, center, self.radius_inner)
        pygame.draw.circle(surface, self.color_inner, center, int(self.radius_inner * 0.6))

        eye_offset = self.radius_inner * 0.6
        eye_color = (255, 120, 120)
        pygame.draw.circle(surface, eye_color, (int(self.x - eye_offset), int(self.y - eye_offset * 0.2)), 3)
        pygame.draw.circle(surface, eye_color, (int(self.x + eye_offset), int(self.y - eye_offset * 0.2)), 3)
