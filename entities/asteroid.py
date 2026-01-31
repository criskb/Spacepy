# entities/asteroid.py

import pygame
import math
import random
from utils import get_opposite_color

class Asteroid:
    def __init__(self, x, y, speed, screen_width, screen_height, bg_color, size_multiplier=1):
        """
        Initialize an Asteroid instance.

        :param x: Initial x-position.
        :param y: Initial y-position.
        :param speed: Movement speed.
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param bg_color: Current background color for tinting.
        :param size_multiplier: Multiplier for asteroid size (1x or 2x).
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = bg_color

        # Size configuration
        self.size_multiplier = size_multiplier
        self.base_radius = 30  # Base radius for 1x size
        self.radius_outer = self.base_radius * self.size_multiplier
        self.radius_inner = 20 * self.size_multiplier

        # Rotation
        self.angle = 0  # Current rotation angle in degrees
        self.rotation_speed = random.uniform(-2, 2)  # Degrees per frame

        # Colors
        self.color_outer = self.apply_tint((20, 20, 20), self.bg_color)  # Dark gray with background tint
        self.color_inner = self.apply_tint((80, 80, 80), self.bg_color)  # Gray with background tint

        # Generate irregular polygon points
        self.num_vertices = random.randint(8, 12)
        self.vertex_angles = self.generate_vertex_angles()
        self.vertex_radii = self.generate_vertex_radii()
        self.vertices = self.generate_irregular_polygon()

        # Craters configuration
        self.craters = []
        self.num_craters = random.randint(3, 5) * self.size_multiplier  # Adjusted for aesthetics
        self.generate_craters()

        # Movement direction (randomized)
        self.direction_angle = math.radians(random.uniform(0, 360))
        self.dx = math.cos(self.direction_angle) * self.speed
        self.dy = math.sin(self.direction_angle) * self.speed

    def apply_tint(self, base_color, tint_color):
        """
        Apply a tint to the base color based on the background color.

        :param base_color: Tuple representing the base RGB color.
        :param tint_color: Tuple representing the background RGB color.
        :return: Tuple representing the tinted RGB color.
        """
        tinted_color = tuple(
            max(min(int((base + bg) / 2), 255), 0) for base, bg in zip(base_color, tint_color)
        )
        return tinted_color

    def generate_irregular_polygon(self):
        """
        Generate points for an irregular polygon to represent the asteroid.

        :return: List of (x, y) tuples representing the polygon vertices.
        """
        points = []
        for angle_deg, radius in zip(self.vertex_angles, self.vertex_radii):
            angle_rad = math.radians(angle_deg + self.angle)
            px = self.x + radius * math.cos(angle_rad)
            py = self.y + radius * math.sin(angle_rad)
            points.append((px, py))
        return points

    def generate_vertex_angles(self):
        """
        Generate stable vertex angles for the asteroid silhouette.
        """
        angle_between_vertices = 360 / self.num_vertices
        return [
            angle_between_vertices * i + random.uniform(-angle_between_vertices / 4, angle_between_vertices / 4)
            for i in range(self.num_vertices)
        ]

    def generate_vertex_radii(self):
        """
        Generate stable radius offsets for each vertex to avoid shape jitter.
        """
        return [random.uniform(0.75, 1.25) * self.radius_outer for _ in range(self.num_vertices)]

    def generate_craters(self):
        """
        Generate craters on the asteroid's surface.
        """
        for _ in range(int(self.num_craters)):
            # Crater size proportional to asteroid size
            crater_size = random.randint(8, 15) * self.size_multiplier  # Larger craters

            # Random position on the asteroid's circumference
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(self.radius_inner + crater_size, self.radius_outer - crater_size)
            crater_x = self.x + distance * math.cos(angle)
            crater_y = self.y + distance * math.sin(angle)

            self.craters.append({
                'x': crater_x,
                'y': crater_y,
                'size': crater_size,
                'angle': angle,  # For potential future use (e.g., animation)
                'distance': distance,
            })

    def move(self):
        """
        Update the asteroid's position based on its velocity.
        """
        self.x += self.dx
        self.y += self.dy

        # Wrap around the screen edges
        if self.x < -self.radius_outer:
            self.x = self.screen_width + self.radius_outer
        elif self.x > self.screen_width + self.radius_outer:
            self.x = -self.radius_outer

        if self.y < -self.radius_outer:
            self.y = self.screen_height + self.radius_outer
        elif self.y > self.screen_height + self.radius_outer:
            self.y = -self.radius_outer

        # Update vertices positions relative to new position
        self.update_vertices()

        # Update crater positions relative to new position
        self.update_craters()

    def update_vertices(self):
        """
        Update the positions of the polygon vertices based on the current rotation angle.
        """
        self.vertices = []
        for angle_deg, radius in zip(self.vertex_angles, self.vertex_radii):
            angle_rad = math.radians(angle_deg + self.angle)
            px = self.x + radius * math.cos(angle_rad)
            py = self.y + radius * math.sin(angle_rad)
            self.vertices.append((px, py))

    def update_craters(self):
        """
        Update the positions of the craters based on the asteroid's new position.
        """
        for crater in self.craters:
            angle = crater['angle']
            distance = crater['distance']
            crater['x'] = self.x + distance * math.cos(angle + math.radians(self.angle))
            crater['y'] = self.y + distance * math.sin(angle + math.radians(self.angle))

    def rotate(self):
        """
        Rotate the asteroid by updating its angle.
        """
        self.angle = (self.angle + self.rotation_speed) % 360
        self.update_vertices()
        self.update_craters()

    def update_colors(self, new_bg_color):
        """
        Update the asteroid's colors if the background color changes.
        """
        self.bg_color = new_bg_color
        self.color_outer = self.apply_tint((20, 20, 20), self.bg_color)  # Dark gray with background tint
        self.color_inner = self.apply_tint((80, 80, 80), self.bg_color)  # Gray with background tint

    def draw(self, surface):
        """
        Draw the asteroid on the given surface.

        :param surface: Pygame surface to draw on.
        """
        # Draw the main asteroid body as an irregular polygon
        if len(self.vertices) >= 3:
            pygame.draw.polygon(surface, self.color_outer, self.vertices)
            pygame.draw.polygon(surface, self.color_inner, self.vertices, width=2)  # Inner outline for depth
            overlay = pygame.Surface((self.radius_outer * 4, self.radius_outer * 4), pygame.SRCALPHA)
            overlay_center = (overlay.get_width() // 2, overlay.get_height() // 2)
            shadow_color = (*self.apply_tint((10, 10, 10), self.bg_color), 90)
            shadow_offset = (int(self.radius_outer * 0.2), int(self.radius_outer * 0.2))
            shadow_vertices = [
                (
                    overlay_center[0] + (vx - self.x) + shadow_offset[0],
                    overlay_center[1] + (vy - self.y) + shadow_offset[1],
                )
                for vx, vy in self.vertices
            ]
            pygame.draw.polygon(overlay, shadow_color, shadow_vertices, width=0)
            highlight_color = (*self.apply_tint((180, 180, 180), self.bg_color), 110)
            pygame.draw.circle(
                overlay,
                highlight_color,
                (overlay_center[0] - int(self.radius_outer * 0.2), overlay_center[1] - int(self.radius_outer * 0.2)),
                int(self.radius_outer * 0.35),
            )
            surface.blit(overlay, (int(self.x - overlay_center[0]), int(self.y - overlay_center[1])))

        # Draw craters
        for crater in self.craters:
            # Crater color is gray with background tint
            crater_color = self.apply_tint((100, 100, 100), self.bg_color)
            pygame.draw.circle(surface, crater_color, (int(crater['x']), int(crater['y'])), int(crater['size']))

    def get_rect(self):
        """
        Get the rectangular area of the asteroid for collision purposes.

        :return: Pygame Rect representing the asteroid's bounds.
        """
        return pygame.Rect(
            self.x - self.radius_outer,
            self.y - self.radius_outer,
            self.radius_outer * 2,
            self.radius_outer * 2
        )
