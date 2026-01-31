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
        self.speed = 2  # Horizontal speed baseline
        self.vertical_speed = 20  # Distance to move down when changing direction
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left
        self.bullets = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shoot_timer = random.randint(60, 120)  # Random shoot interval
        self.vx = self.speed * self.direction
        self.vy = 0
        self.max_speed = 3.2
        self.acceleration = 0.15
        self.wander_angle = random.uniform(0, math.tau)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.x = max(self.radius_outer, min(self.x, self.screen_width - self.radius_outer))
        self.y = max(self.radius_outer, min(self.y, self.screen_height - self.radius_outer))

    def update(self, player_x, player_y, neighbors):
        # Handle shooting
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot(player_x, player_y)
            self.shoot_timer = random.randint(60, 120)
        self.apply_steering(player_x, player_y, neighbors)

    def apply_steering(self, player_x, player_y, neighbors):
        target_x = player_x
        target_y = player_y - 120
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy) or 1.0

        desired_range = 240
        if distance > desired_range:
            desired_vx = (dx / distance) * self.max_speed
            desired_vy = (dy / distance) * self.max_speed
        else:
            desired_vx = (-dx / distance) * self.max_speed
            desired_vy = (-dy / distance) * self.max_speed

        separation_x = 0.0
        separation_y = 0.0
        for neighbor in neighbors:
            if neighbor is self:
                continue
            offset_x = self.x - neighbor.x
            offset_y = self.y - neighbor.y
            offset_dist = math.hypot(offset_x, offset_y)
            if 0 < offset_dist < 80:
                strength = (80 - offset_dist) / 80
                separation_x += (offset_x / offset_dist) * strength
                separation_y += (offset_y / offset_dist) * strength

        edge_push_x = 0.0
        if self.x < self.radius_outer * 2:
            edge_push_x = 1.0
        elif self.x > self.screen_width - self.radius_outer * 2:
            edge_push_x = -1.0

        band_push_y = 0.0
        band_min = 50
        band_max = self.screen_height * 0.45
        if self.y < band_min:
            band_push_y = 1.0
        elif self.y > band_max:
            band_push_y = -1.0

        self.wander_angle += random.uniform(-0.15, 0.15)
        wander_x = math.cos(self.wander_angle) * 0.5
        wander_y = math.sin(self.wander_angle) * 0.5

        steer_x = desired_vx + separation_x * 2.2 + edge_push_x * 1.5 + wander_x
        steer_y = desired_vy + separation_y * 2.2 + band_push_y * 1.5 + wander_y

        self.vx += (steer_x - self.vx) * self.acceleration
        self.vy += (steer_y - self.vy) * self.acceleration

        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

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
