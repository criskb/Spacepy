# entities/boss.py

import pygame
import math
import random
from entities.bullet import Bullet
from utils import draw_glow_circle, lighten_color, darken_color

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
        self.max_health = 30
        self.health = self.max_health
        self.shoot_delay = 1800  # Time between shots in milliseconds
        self.last_shot_time = pygame.time.get_ticks()
        self.patterns = [self.direct_shot, self.shotgun_spread, self.circular_burst, self.spiral_burst]
        self.current_pattern = random.choice(self.patterns)
        self.vx = 0
        self.vy = 0
        self.max_speed = 3.6
        self.acceleration = 0.12
        self.wander_angle = random.uniform(0, math.tau)
        self.last_special_time = pygame.time.get_ticks()
        self.special_cooldown = 6500
        self.charge_duration = 1200
        self.charging = False
        self.charge_start_time = 0
        self.spiral_angle = 0.0

    def update(self, player):
        current_time = pygame.time.get_ticks()
        phase = self.get_phase()
        speed_scale = 1.0 + phase * 0.25
        self.shoot_delay = max(800, 1800 - phase * 400)
        self.special_cooldown = max(3500, 6500 - phase * 900)

        self.apply_movement(player, current_time, speed_scale)

        if not self.charging and current_time - self.last_special_time > self.special_cooldown:
            self.charging = True
            self.charge_start_time = current_time

        special_triggered = False
        if self.charging and current_time - self.charge_start_time > self.charge_duration:
            self.charging = False
            self.last_special_time = current_time
            self.shockwave_burst(phase)
            special_triggered = True

        if current_time - self.last_shot_time > self.shoot_delay:
            if phase >= 2:
                self.current_pattern = random.choice(self.patterns + [self.arc_burst])
            else:
                self.current_pattern = random.choice(self.patterns)
            self.current_pattern(player, phase)
            self.last_shot_time = current_time
        return special_triggered

    def apply_movement(self, player, current_time, speed_scale):
        oscillation = math.sin(current_time / 700) * 150
        target_x = player.x + oscillation
        target_y = 100 + math.sin(current_time / 1100) * 30
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy) or 1.0
        desired_vx = (dx / distance) * self.max_speed * speed_scale
        desired_vy = (dy / distance) * self.max_speed * speed_scale

        self.wander_angle += random.uniform(-0.1, 0.1)
        wander_x = math.cos(self.wander_angle) * 0.4
        wander_y = math.sin(self.wander_angle) * 0.2

        edge_push = 0.0
        if self.x < self.radius_outer * 1.5:
            edge_push = 1.0
        elif self.x > self.screen_width - self.radius_outer * 1.5:
            edge_push = -1.0

        self.vx += (desired_vx + wander_x + edge_push) * self.acceleration
        self.vy += (desired_vy + wander_y) * self.acceleration

        speed = math.hypot(self.vx, self.vy)
        max_speed = self.max_speed * speed_scale
        if speed > max_speed:
            scale = max_speed / speed
            self.vx *= scale
            self.vy *= scale

        self.x += self.vx
        self.y += self.vy
        self.x = max(self.radius_outer, min(self.x, self.screen_width - self.radius_outer))
        self.y = max(self.radius_outer, min(self.y, self.screen_height * 0.4))

    def get_phase(self):
        health_ratio = self.health / self.max_health
        if health_ratio > 0.66:
            return 0
        if health_ratio > 0.33:
            return 1
        return 2

    def direct_shot(self, player, phase):
        # Shoot directly towards the player
        lead_x = player.x + player.direction_x * player.speed * 10
        lead_y = player.y + player.direction_y * player.speed * 10
        angle = math.atan2(lead_y - self.y, lead_x - self.x)
        bullet_speed = 6 + phase
        dx = math.cos(angle) * bullet_speed
        dy = math.sin(angle) * bullet_speed
        bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
        self.bullets.append(bullet)

    def shotgun_spread(self, player, phase):
        # Shoot multiple bullets in a spread towards the player
        num_bullets = 5 + phase
        spread_angle = math.radians(45 + phase * 10)
        base_angle = math.atan2(player.y - self.y, player.x - self.x)
        start_angle = base_angle - spread_angle / 2
        angle_increment = spread_angle / (num_bullets - 1)
        for i in range(num_bullets):
            angle = start_angle + angle_increment * i
            dx = math.cos(angle) * (6 + phase)
            dy = math.sin(angle) * (6 + phase)
            bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
            self.bullets.append(bullet)

    def circular_burst(self, player, phase):
        # Shoot bullets in a circular pattern around the boss
        num_bullets = 12 + phase * 4
        angle_increment = 2 * math.pi / num_bullets
        for i in range(num_bullets):
            angle = angle_increment * i
            dx = math.cos(angle) * (4 + phase)
            dy = math.sin(angle) * (4 + phase)
            bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
            self.bullets.append(bullet)

    def spiral_burst(self, player, phase):
        num_bullets = 10 + phase * 4
        angle_increment = math.pi / 6
        for i in range(num_bullets):
            angle = self.spiral_angle + angle_increment * i
            dx = math.cos(angle) * (4.5 + phase)
            dy = math.sin(angle) * (4.5 + phase)
            bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
            self.bullets.append(bullet)
        self.spiral_angle += math.radians(20)

    def arc_burst(self, player, phase):
        num_bullets = 7 + phase * 2
        spread_angle = math.radians(70)
        base_angle = math.atan2(player.y - self.y, player.x - self.x)
        start_angle = base_angle - spread_angle / 2
        angle_increment = spread_angle / (num_bullets - 1)
        for i in range(num_bullets):
            angle = start_angle + angle_increment * i
            dx = math.cos(angle) * (5 + phase)
            dy = math.sin(angle) * (5 + phase)
            bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
            self.bullets.append(bullet)

    def shockwave_burst(self, phase):
        num_bullets = 18 + phase * 6
        angle_increment = 2 * math.pi / num_bullets
        for i in range(num_bullets):
            angle = angle_increment * i
            dx = math.cos(angle) * (5 + phase)
            dy = math.sin(angle) * (5 + phase)
            bullet = Bullet(self.x, self.y, dx, dy, 2 + phase, 'boss')
            self.bullets.append(bullet)

    def move(self):
        # Move bullets
        pass  # Movement is handled in the main game loop

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        center = (int(self.x), int(self.y))
        glow_color = lighten_color(self.color_outer, 0.4)
        draw_glow_circle(surface, glow_color, center, self.radius_outer, glow_radius=18, alpha=160)

        pulse_radius = int(self.radius_outer * (1.2 + 0.08 * math.sin(current_time / 200)))
        pulse_color = (*lighten_color(self.color_outer, 0.5), 120)
        pulse_surface = pygame.Surface((pulse_radius * 2 + 4, pulse_radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(pulse_surface, pulse_color, (pulse_radius + 2, pulse_radius + 2), pulse_radius, width=3)
        surface.blit(pulse_surface, (self.x - pulse_radius - 2, self.y - pulse_radius - 2))

        if self.charging:
            charge_ratio = min((current_time - self.charge_start_time) / self.charge_duration, 1)
            charge_radius = int(self.radius_outer * (1.4 + charge_ratio))
            charge_surface = pygame.Surface((charge_radius * 2 + 4, charge_radius * 2 + 4), pygame.SRCALPHA)
            charge_color = (*lighten_color(self.color_inner, 0.6), int(180 * charge_ratio))
            pygame.draw.circle(charge_surface, charge_color, (charge_radius + 2, charge_radius + 2), charge_radius, width=4)
            surface.blit(charge_surface, (self.x - charge_radius - 2, self.y - charge_radius - 2))

        outer_ring = darken_color(self.color_outer, 0.2)
        pygame.draw.circle(surface, self.color_outer, center, self.radius_outer)
        pygame.draw.circle(surface, outer_ring, center, self.radius_outer, width=4)

        mid_radius = int(self.radius_outer * 0.7)
        mid_color = lighten_color(self.color_outer, 0.2)
        pygame.draw.circle(surface, mid_color, center, mid_radius)

        core_color = lighten_color(self.color_inner, 0.4)
        pygame.draw.circle(surface, core_color, center, self.radius_inner)
        pygame.draw.circle(surface, self.color_inner, center, int(self.radius_inner * 0.6))

        spoke_color = darken_color(self.color_outer, 0.4)
        for i in range(6):
            angle = i * (math.pi / 3)
            end_x = self.x + math.cos(angle) * self.radius_outer
            end_y = self.y + math.sin(angle) * self.radius_outer
            pygame.draw.line(surface, spoke_color, center, (end_x, end_y), width=3)

    def draw_health_bar(self, surface):
        # Draw the health bar above the boss
        bar_width = self.radius_outer * 2
        bar_height = 10
        health_ratio = self.health / self.max_health
        health_bar_width = bar_width * health_ratio
        bar_x = self.x - bar_width / 2
        bar_y = self.y - self.radius_outer - 20
        pygame.draw.rect(
            surface,
            (60, 60, 60),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=6,
        )
        pygame.draw.rect(
            surface,
            (0, 220, 140),
            (bar_x, bar_y, health_bar_width, bar_height),
            border_radius=6,
        )
