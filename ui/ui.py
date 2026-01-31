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

class DialogBubble:
    def __init__(self, font, position, size, text_color=(255, 255, 255)):
        self.font = font
        self.position = position
        self.size = size
        self.text_color = text_color
        self.padding = 14
        self.speaker = ""
        self.full_text = ""
        self.current_text = ""
        self.char_index = 0
        self.typing_speed = 40  # chars per second
        self.start_time = 0
        self.last_tick = 0
        self.hold_time = 2500
        self.finish_time = None
        self.visible = False

    def start(self, speaker, text, start_time, typing_speed=40, hold_time=2500):
        self.speaker = speaker
        self.full_text = text
        self.current_text = ""
        self.char_index = 0
        self.typing_speed = typing_speed
        self.start_time = start_time
        self.last_tick = start_time
        self.hold_time = hold_time
        self.finish_time = None
        self.visible = True

    def update(self, current_time):
        if not self.visible:
            return
        if self.finish_time is not None:
            if current_time - self.finish_time > self.hold_time:
                self.visible = False
            return
        elapsed = current_time - self.last_tick
        if elapsed <= 0:
            return
        chars_to_add = int(elapsed / 1000 * self.typing_speed)
        if chars_to_add > 0:
            self.char_index = min(self.char_index + chars_to_add, len(self.full_text))
            self.current_text = self.full_text[:self.char_index]
            self.last_tick = current_time
        if self.char_index >= len(self.full_text):
            self.finish_time = current_time

    def is_active(self):
        return self.visible

    def _wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def draw(self, surface):
        if not self.visible:
            return
        rect = pygame.Rect(self.position, self.size)
        bubble_color = (25, 25, 35)
        border_color = lighten_color(bubble_color, 0.3)
        pygame.draw.rect(surface, bubble_color, rect, border_radius=16)
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=16)
        tail = [
            (rect.left + 60, rect.bottom),
            (rect.left + 90, rect.bottom),
            (rect.left + 75, rect.bottom + 18),
        ]
        pygame.draw.polygon(surface, bubble_color, tail)
        pygame.draw.polygon(surface, border_color, tail, width=2)

        speaker_font = pygame.font.Font(None, 26)
        speaker_font.set_bold(True)
        speaker_surface = speaker_font.render(self.speaker, True, lighten_color(self.text_color, 0.2))
        surface.blit(speaker_surface, (rect.x + self.padding, rect.y + self.padding))

        text_area_width = rect.width - self.padding * 2
        lines = self._wrap_text(self.current_text, text_area_width)
        y_offset = rect.y + self.padding + 28
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            surface.blit(text_surface, (rect.x + self.padding, y_offset))
            y_offset += text_surface.get_height() + 4
