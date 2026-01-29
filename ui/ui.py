# ui/ui.py

import pygame

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
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
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
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * health_ratio, bar_height))

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
        surface.blit(score_text, (20, 50))
        surface.blit(level_text, (20, 80))
