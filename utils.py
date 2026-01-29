# utils.py

import random
import pygame
import math

def get_random_dark_color():
    """Generate a random dark color that is not pure black."""
    while True:
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)
        if (r, g, b) != (0, 0, 0):
            return (r, g, b)

def get_opposite_color(color):
    """Get the opposite color."""
    r, g, b = color
    return (255 - r, 255 - g, 255 - b)

def is_collision(x1, y1, x2, y2, radius1, radius2):
    """Check if two circles are colliding."""
    distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return distance < (radius1 + radius2)

def load_sound(file_path):
    """Load a sound file, handling exceptions."""
    try:
        return pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Error loading sound: {e}")
        return None

def rotate_point(angle, x, y):
    """Rotate a point around the origin (0,0) by a given angle."""
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    x_new = x * cos_theta - y * sin_theta
    y_new = x * sin_theta + y * cos_theta
    return (x_new, y_new)

# utils.py

def blend_colors(color1, color2, ratio):
    """
    Blend two colors together by a given ratio.

    :param color1: Tuple representing the first color (R, G, B)
    :param color2: Tuple representing the second color (R, G, B)
    :param ratio: Float between 0 and 1 representing the weight of color2
    :return: Tuple representing the blended color (R, G, B)
    """
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)
