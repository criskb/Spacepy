# entities/enemy.py

import pygame
import random
import math
from entities.bullet import Bullet

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
        # Draw the enemy
        pygame.draw.circle(surface, self.color_outer, (int(self.x), int(self.y)), self.radius_outer)
        pygame.draw.circle(surface, self.color_inner, (int(self.x), int(self.y)), self.radius_inner)
