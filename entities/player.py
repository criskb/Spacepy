# entities/player.py

import pygame
import math
from entities.bullet import Bullet

class Player:
    def __init__(self, x, y, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20
        self.speed = 5
        self.direction_x = 0  # -1 for left, 1 for right, 0 for no movement
        self.direction_y = 0  # -1 for up, 1 for down, 0 for no movement
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullets = []
        self.health = 10
        self.max_health = 10

        # Power-up related attributes
        self.power_up_active = None  # 'rapid_fire' or 'shotgun'
        self.power_up_end_time = 0  # Timestamp when power-up expires

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update_position(self):
        # Update horizontal position
        self.x += self.direction_x * self.speed
        # Constrain horizontal position
        self.x = max(self.radius, min(self.x, self.screen_width - self.radius))
        # Update vertical position
        self.y += self.direction_y * self.speed
        # Constrain vertical position to lower half of the screen
        min_y = self.screen_height // 2
        max_y = self.screen_height - self.radius
        self.y = max(min_y, min(self.y, max_y))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        # Determine shoot delay based on power-up
        if self.power_up_active == 'rapid_fire':
            shoot_delay = 100  # Faster shooting
        elif self.power_up_active == 'shotgun':
            shoot_delay = 500  # Slight delay between shots
        else:
            shoot_delay = 300  # Normal shooting

        if hasattr(self, 'last_shot_time'):
            if current_time - self.last_shot_time < shoot_delay:
                return False  # Still in cooldown
        else:
            self.last_shot_time = 0  # Initialize if not present

        self.last_shot_time = current_time

        if self.power_up_active == 'shotgun':
            # Shotgun shooting: fire multiple bullets in a spread
            num_bullets = 5
            spread_angle = math.radians(45)  # 45 degrees spread
            start_angle = -spread_angle / 2
            angle_increment = spread_angle / (num_bullets - 1)
            for i in range(num_bullets):
                angle = start_angle + angle_increment * i
                dx = math.sin(angle) * 10
                dy = -math.cos(angle) * 10
                bullet = Bullet(self.x, self.y - self.radius, dx, dy, 1, 'player')
                self.bullets.append(bullet)
        else:
            # Normal or rapid shooting
            bullet = Bullet(self.x, self.y - self.radius, 0, -10, 1, 'player')
            self.bullets.append(bullet)

        return True  # Indicate that a shot was fired

    def activate_power_up(self, power_type):
        self.power_up_active = power_type
        self.power_up_end_time = pygame.time.get_ticks() + 30000  # 30 seconds duration

        if power_type == 'rapid_fire':
            # Reduce shoot delay for rapid fire
            self.shoot_delay = 100
        elif power_type == 'shotgun':
            # Set shoot delay for shotgun
            self.shoot_delay = 500

    def deactivate_power_up(self):
        self.power_up_active = None
        self.power_up_end_time = 0
        self.shoot_delay = 300  # Reset to normal shooting delay

    def update_power_up(self):
        if self.power_up_active and pygame.time.get_ticks() > self.power_up_end_time:
            self.deactivate_power_up()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height - 100
        self.direction_x = 0
        self.direction_y = 0
        self.bullets.clear()
        self.health = self.max_health
        self.power_up_active = None
        self.power_up_end_time = 0
        self.last_shot_time = 0  # Reset shooting timer
