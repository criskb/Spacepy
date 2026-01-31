# effects/effects.py

import pygame
import random

class Effects:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shake_duration = 0
        self.shake_intensity = 5
        self.flash_duration = 0
        self.flash_alpha = 0
        self.flash_center = (screen_width // 2, screen_height // 2)
        self.flash_color = (255, 120, 120)

    def start_shake(self, duration=15):
        self.shake_duration = duration

    def apply_shake(self, surface):
        if self.shake_duration > 0:
            dx = random.randint(-self.shake_intensity, self.shake_intensity)
            dy = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1
            shaken_surface = pygame.Surface((self.screen_width, self.screen_height))
            shaken_surface.blit(surface, (dx, dy))
            return shaken_surface
        else:
            return surface

    def start_flash(self, center, duration=12, color=(255, 120, 120)):
        self.flash_duration = duration
        self.flash_alpha = 255
        self.flash_center = center
        self.flash_color = color

    def apply_flash(self, surface):
        if self.flash_duration > 0:
            flash_overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            radius = int(max(self.screen_width, self.screen_height) * 0.35)
            step_count = 3
            alpha_step = max(int(self.flash_alpha / step_count), 1)
            for i in range(step_count):
                step_radius = int(radius * (1 - i * 0.25))
                color = (*self.flash_color, max(self.flash_alpha - i * alpha_step, 0))
                pygame.draw.circle(flash_overlay, color, self.flash_center, step_radius)
            self.flash_alpha -= int(255 / self.flash_duration)
            self.flash_duration -= 1
            surface.blit(flash_overlay, (0, 0))
        return surface

    def update(self):
        pass  # Placeholder for any future updates to effects
