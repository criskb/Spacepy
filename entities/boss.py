# entities/boss.py

import pygame
import math
import random
from entities.bullet import Bullet

class Boss:
    def __init__(self, x, y, color_outer, color_inner, screen_width, screen_height):
        self.x = x
        self.y = y
        self.color_outer = color_outer
        self.color_inner = color_inner
        self.radius_outer = 40
        self.radius_inner = 30
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullets = []
        self.health = 20
        self.shoot_delay = 2000  # Time between shots in milliseconds
        self.last_shot_time = pygame.time.get_ticks()
        self.patterns = [self.direct_shot, self.shotgun_spread, self.circular_burst]
        self.current_pattern = random.choice(self.patterns)

    def update(self, target_x, target_y):
        # Move side to side
        self.x += self.speed * self.direction
        if self.x - self.radius_outer <= 0 or self.x + self.radius_outer >= self.screen_width:
            self.direction *= -1  # Change direction

        # Shooting logic
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            # Randomly select a new pattern
            self.current_pattern = random.choice(self.patterns)
            self.current_pattern(target_x, target_y)
            self.last_shot_time = current_time

    def direct_shot(self, target_x, target_y):
        # Shoot directly towards the player
        angle = math.atan2(target_y - self.y, target_x - self.x)
        dx = math.cos(angle) * 6
        dy = math.sin(angle) * 6
        bullet = Bullet(self.x, self.y, dx, dy, 2, 'boss')
        self.bullets.append(bullet)

    def shotgun_spread(self, target_x, target_y):
        # Shoot multiple bullets in a spread towards the player
        num_bullets = 5
        spread_angle = math.radians(45)  # Spread of 45 degrees
        base_angle = math.atan2(target_y - self.y, target_x - self.x)
        start_angle = base_angle - spread_angle / 2
        angle_increment = spread_angle / (num_bullets - 1)
        for i in range(num_bullets):
            angle = start_angle + angle_increment * i
            dx = math.cos(angle) * 6
            dy = math.sin(angle) * 6
            bullet = Bullet(self.x, self.y, dx, dy, 2, 'boss')
            self.bullets.append(bullet)

    def circular_burst(self, target_x, target_y):
        # Shoot bullets in a circular pattern around the boss
        num_bullets = 12
        angle_increment = 2 * math.pi / num_bullets
        for i in range(num_bullets):
            angle = angle_increment * i
            dx = math.cos(angle) * 4
            dy = math.sin(angle) * 4
            bullet = Bullet(self.x, self.y, dx, dy, 2, 'boss')
            self.bullets.append(bullet)

    def move(self):
        # Move bullets
        pass  # Movement is handled in the main game loop

    def draw(self, surface):
        # Draw the boss
        pygame.draw.circle(surface, self.color_outer, (int(self.x), int(self.y)), self.radius_outer)
        pygame.draw.circle(surface, self.color_inner, (int(self.x), int(self.y)), self.radius_inner)

    def draw_health_bar(self, surface):
        # Draw the health bar above the boss
        bar_width = self.radius_outer * 2
        bar_height = 10
        health_ratio = self.health / 20
        health_bar_width = bar_width * health_ratio
        pygame.draw.rect(surface, (255, 0, 0), (self.x - bar_width / 2, self.y - self.radius_outer - 20, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - bar_width / 2, self.y - self.radius_outer - 20, health_bar_width, bar_height))
