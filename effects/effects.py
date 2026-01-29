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

    def start_flash(self, duration=10):
        self.flash_duration = duration
        self.flash_alpha = 255

    def apply_flash(self, surface):
        if self.flash_duration > 0:
            flash_overlay = pygame.Surface((self.screen_width, self.screen_height))
            flash_overlay.fill((255, 255, 255))
            flash_overlay.set_alpha(self.flash_alpha)
            self.flash_alpha -= int(255 / self.flash_duration)
            self.flash_duration -= 1
            surface.blit(flash_overlay, (0, 0))
        return surface

    def update(self):
        pass  # Placeholder for any future updates to effects
