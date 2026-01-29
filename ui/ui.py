# ui/ui.py

import pygame
from utils import lighten_color, darken_color

class Button:
    def __init__(self, text, font, color, hover_color, position, size, text_color):
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.position = position
        self.size = size
        self.text_color = text_color
        self.rect = pygame.Rect(position, size)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=10)
        if self.rect.collidepoint(mouse_pos):
            button_color = self.hover_color
        else:
            button_color = self.color
        pygame.draw.rect(surface, button_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, lighten_color(button_color, 0.2), self.rect, width=2, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class HealthBar:
    def __init__(self, player):
        self.player = player

    def draw(self, surface):
        # Draw the health bar
        health_ratio = self.player.health / self.player.max_health
        bar_width = 200
        bar_height = 20
        x = 20
        y = 20
        pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_width, bar_height), border_radius=8)
        pygame.draw.rect(surface, (0, 220, 140), (x, y, bar_width * health_ratio, bar_height), border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), width=2, border_radius=8)

class ScoreDisplay:
    def __init__(self, screen_width):
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.screen_width = screen_width

    def add_score(self, points):
        self.score += points

    def update_level(self, level):
        self.level = level

    def draw(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        shadow_color = darken_color((255, 255, 255), 0.7)
        score_shadow = self.font.render(f"Score: {self.score}", True, shadow_color)
        level_shadow = self.font.render(f"Level: {self.level}", True, shadow_color)
        surface.blit(score_shadow, (22, 52))
        surface.blit(level_shadow, (22, 82))
        surface.blit(score_text, (20, 50))
        surface.blit(level_text, (20, 80))
