# main.py

import pygame
import sys
import os
import random
import math
import json

from utils import get_random_dark_color, get_opposite_color, is_collision, load_sound
from entities.player import Player
from entities.enemy import Enemy
from entities.boss import Boss
from entities.bullet import Bullet
from entities.asteroid import Asteroid
from entities.health_item import HealthItem
from entities.power_up import PowerUp
from effects.effects import Effects
from ui.ui import Button, HealthBar, ScoreDisplay, DialogBubble
from ui.ship_builder import draw_ship_builder

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.Font(None, 40)
FONT.set_bold(True)
GAME_OVER_FONT = pygame.font.Font(None, 72)
GAME_OVER_FONT.set_bold(True)
COUNTDOWN_FONT = pygame.font.Font(None, 150)
COUNTDOWN_FONT.set_bold(True)

# Load sounds
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
SHOOT_SOUND = load_sound(os.path.join(ASSETS_PATH, 'shoot.wav'))
EXPLOSION_SOUND = load_sound(os.path.join(ASSETS_PATH, 'explosion.wav'))
SHAKE_SOUND = load_sound(os.path.join(ASSETS_PATH, 'shake.wav'))
LEVELUP_SOUND = load_sound(os.path.join(ASSETS_PATH, 'levelup.wav'))
PICKUP_SOUND = load_sound(os.path.join(ASSETS_PATH, 'pickup.wav'))
COUNTDOWN_SOUND = load_sound(os.path.join(ASSETS_PATH, 'countdown.wav'))
COUNTDOWN_FINAL_SOUND = load_sound(os.path.join(ASSETS_PATH, 'countdown_final.wav'))

# Adjust sound volume if necessary
if SHOOT_SOUND:
    SHOOT_SOUND.set_volume(0.5)  # Adjust volume between 0.0 and 1.0
if COUNTDOWN_SOUND:
    COUNTDOWN_SOUND.set_volume(0.7)
if COUNTDOWN_FINAL_SOUND:
    COUNTDOWN_FINAL_SOUND.set_volume(0.8)

# Background music
try:
    pygame.mixer.music.load(os.path.join(ASSETS_PATH, 'bgm.wav'))
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading background music: {e}")

def main():
    # Game setup
    current_bg_color = get_random_dark_color()
    game_state = "menu"
    clock = pygame.time.Clock()

    # Ensure the background color is not black
    if current_bg_color == (0, 0, 0):
        current_bg_color = (10, 10, 10)  # Slightly off-black

    # Player color opposite of background
    player_color = get_opposite_color(current_bg_color)
    # Player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, player_color, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Health bar
    health_bar = HealthBar(player)

    # Score display
    score_display = ScoreDisplay(SCREEN_WIDTH)

    # Effects
    effects = Effects(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Dialogue bubble
    dialog_font = pygame.font.Font(None, 28)
    dialog_width = max(360, int(SCREEN_WIDTH * 0.33))
    dialog_bubble = DialogBubble(
        dialog_font,
        (30, SCREEN_HEIGHT - 170),
        (dialog_width, 130),
    )
    dialog_queue = []
    intro_dialog_shown = False

    # Buttons
    button_font = pygame.font.Font(None, 52)
    button_font.set_bold(True)

    play_button = Button(
        "Play",
        button_font,
        (34, 139, 34),       # Forest Green
        (50, 205, 50),       # Lime Green
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100),
        (200, 50),
        WHITE
    )

    ship_builder_button = Button(
        "Ship Builder",
        button_font,
        (72, 61, 139),       # Dark Slate Blue
        (106, 90, 205),      # Slate Blue
        (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 170),
        (280, 50),
        WHITE
    )

    quit_button = Button(
        "Quit",
        button_font,
        (178, 34, 34),       # Firebrick
        (220, 20, 60),       # Crimson
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 240),
        (200, 50),
        WHITE
    )

    # Game Over Buttons
    retry_button = Button(
        "Retry",
        button_font,
        (70, 130, 180),      # Steel Blue
        (100, 149, 237),     # Cornflower Blue
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150 + 100),
        (200, 50),
        WHITE
    )
    game_over_quit_button = Button(
        "Quit",
        button_font,
        (178, 34, 34),       # Firebrick
        (220, 20, 60),       # Crimson
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 220 + 100),
        (200, 50),
        WHITE
    )

    builder_back_button = Button(
        "Back",
        button_font,
        (70, 130, 180),
        (100, 149, 237),
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 120),
        (200, 50),
        WHITE
    )

    builder_weapon_button = Button(
        "Upgrade Weapon",
        button_font,
        (46, 139, 87),
        (60, 179, 113),
        (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 40),
        (320, 50),
        WHITE
    )

    builder_wing_button = Button(
        "Upgrade Wings",
        button_font,
        (46, 139, 87),
        (60, 179, 113),
        (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 40),
        (320, 50),
        WHITE
    )

    builder_confirm_button = Button(
        "Confirm Loadout",
        button_font,
        (72, 61, 139),
        (106, 90, 205),
        (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 140),
        (320, 50),
        WHITE
    )

    builder_hull_prev = Button(
        "<",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 40),
        (60, 45),
        WHITE
    )
    builder_hull_next = Button(
        ">",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 - 40),
        (60, 45),
        WHITE
    )
    builder_color_prev = Button(
        "<",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 10),
        (60, 45),
        WHITE
    )
    builder_color_next = Button(
        ">",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 + 10),
        (60, 45),
        WHITE
    )
    builder_nozzle_prev = Button(
        "<",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 60),
        (60, 45),
        WHITE
    )
    builder_nozzle_next = Button(
        ">",
        button_font,
        (90, 90, 90),
        (120, 120, 120),
        (SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT // 2 + 60),
        (60, 45),
        WHITE
    )

    SAVE_FILE = "save.json"
    hull_options = [
        {"id": "arrow", "label": "Arrow", "cost": 0},
        {"id": "diamond", "label": "Diamond", "cost": 12},
        {"id": "delta", "label": "Delta", "cost": 18},
    ]
    color_options = [
        {"id": "ember", "label": "Ember", "color": (255, 120, 120), "cost": 0},
        {"id": "azure", "label": "Azure", "color": (120, 180, 255), "cost": 6},
        {"id": "lilac", "label": "Lilac", "color": (190, 120, 255), "cost": 8},
        {"id": "mint", "label": "Mint", "color": (120, 255, 200), "cost": 7},
    ]
    nozzle_options = [
        {"id": "classic", "label": "Classic", "cost": 0},
        {"id": "dual", "label": "Dual", "cost": 10},
        {"id": "vector", "label": "Vector", "cost": 14},
    ]

    def get_option(options, option_id):
        for option in options:
            if option["id"] == option_id:
                return option
        return options[0]

    def load_save():
        if not os.path.exists(SAVE_FILE):
            return {}
        try:
            with open(SAVE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_game(data):
        try:
            with open(SAVE_FILE, "w") as file:
                json.dump(data, file, indent=2)
        except OSError:
            pass

    save_data = load_save()
    player.credits = save_data.get("credits", 0)
    player.wing_level = save_data.get("wing_level", 1)
    player.weapon_level = save_data.get("weapon_level", 1)
    player.weapon_mode = save_data.get("weapon_mode", "basic")
    if player.weapon_mode not in {"basic", "spread"}:
        player.weapon_mode = "basic"
    player.hull_type = save_data.get("hull_type", "arrow")
    player.nozzle_type = save_data.get("nozzle_type", "classic")
    player.custom_color = save_data.get("custom_color", False)
    saved_color = save_data.get("ship_color")
    if isinstance(saved_color, list) and len(saved_color) == 3:
        player.color = tuple(saved_color)
        player.custom_color = True
    owned_hulls = set(save_data.get("owned_hulls", ["arrow"]))
    owned_colors = set(save_data.get("owned_colors", ["ember"]))
    owned_nozzles = set(save_data.get("owned_nozzles", ["classic"]))
    owned_hulls.add(player.hull_type)
    owned_nozzles.add(player.nozzle_type)

    selected_hull = player.hull_type
    selected_nozzle = player.nozzle_type
    selected_color = next((c["id"] for c in color_options if c["color"] == player.color), "ember")
    owned_colors.add(selected_color)

    def persist_save():
        save_game(
            {
                "credits": player.credits,
                "wing_level": player.wing_level,
                "weapon_level": player.weapon_level,
                "weapon_mode": player.weapon_mode,
                "hull_type": player.hull_type,
                "nozzle_type": player.nozzle_type,
                "ship_color": list(player.color),
                "custom_color": player.custom_color,
                "owned_hulls": sorted(owned_hulls),
                "owned_colors": sorted(owned_colors),
                "owned_nozzles": sorted(owned_nozzles),
            }
        )

    # Stars for background
    stars = []
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        speed = random.uniform(1, 4)
        radius = random.randint(1, 3)
        stars.append([x, y, speed, radius])

    def draw_background(surface):
        surface.fill(current_bg_color)
        # Stars
        for star in stars:
            pygame.draw.circle(surface, WHITE, (int(star[0]), int(star[1])), star[3])
            star[1] += star[2]
            if star[1] > SCREEN_HEIGHT:
                star[0] = random.randint(0, SCREEN_WIDTH)
                star[1] = 0
                star[2] = random.uniform(1, 4)
                star[3] = random.randint(1, 3)

    # Load top scores
    score_file = "scores.txt"
    top_scores = []
    if os.path.exists(score_file):
        with open(score_file, "r") as file:
            lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[0].isdigit():
                score = int(parts[0])
                level_achieved = int(parts[1])
                try:
                    time_sec = float(parts[2])
                    top_scores.append((score, level_achieved, time_sec))
                except ValueError:
                    continue

    # Game variables
    enemies = []
    asteroids = []
    health_items = []
    power_ups = []
    enemy_bullets = []
    boss_bullets = []
    level = 1
    boss_spawn_level_interval = 5  # Every 5 levels
    boss = None
    boss_active = False
    boss_defeated_current_level = False  # Initialize the flag
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    score_added = False  # Initialize the flag to prevent multiple score additions
    countdown_start_ticks = None  # For countdown timer
    countdown_number = 3  # Start countdown from 3
    story_events = {
        2: ("Mission Control", "Scans are spiking. Expect denser fire from the swarm."),
        4: ("Mission Control", "We traced the signal to an asteroid belt. Stay sharp."),
        6: ("Mission Control", "Bosses are adapting. Watch for charge-up patterns."),
    }

    # Function to spawn initial enemies
    def spawn_enemies(initial=False):
        if initial:
            count = 3
        else:
            # Increase the number of enemies with each level
            count = 3 + (level - 1) * 2  # Adjust the multiplier as needed

        attempts = 0
        max_attempts = 500  # Increased attempts to ensure enough enemies spawn
        spawned_enemies = 0
        while spawned_enemies < count and attempts < max_attempts:
            enemy_x = random.randint(20, SCREEN_WIDTH - 20)
            enemy_y = random.randint(50, 150)  # Random Y position near the top
            # Check for overlap with existing enemies
            overlap = False
            for existing_enemy in enemies:
                if is_collision(enemy_x, enemy_y, existing_enemy.x, existing_enemy.y, 40, 40):  # Using radius 20 for both
                    overlap = True
                    break
            if not overlap:
                enemy_color_outer = get_opposite_color(current_bg_color)
                enemy_color_inner = (255, 0, 0)  # Red core
                enemy = Enemy(enemy_x, enemy_y, enemy_color_outer, enemy_color_inner, SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.append(enemy)
                spawned_enemies += 1
            attempts += 1

    # Function to spawn the boss
    def spawn_boss():
        nonlocal boss, boss_active
        boss_color_outer = get_opposite_color(current_bg_color)
        boss_color_inner = (255, 0, 0)  # Red core
        boss = Boss(SCREEN_WIDTH // 2, 100, boss_color_outer, boss_color_inner, SCREEN_WIDTH, SCREEN_HEIGHT)
        boss_active = True
        boss_dialogs = {
            5: ("Warden-01", "You made it this far? Cute. Let's see you dodge this."),
            10: ("Warden-02", "Your ship is fast. Mine is relentless."),
            15: ("Warden-03", "Every pulse brings you closer to oblivion."),
        }
        dialog = boss_dialogs.get(level, ("Warden", "The abyss answers."))
        dialog_queue.append(dialog)

    def enqueue_intro_dialog():
        dialog_queue.extend(
            [
                ("Mission Control", "Pilot, you're our last line of defense."),
                ("Mission Control", "Break through the swarm and stop the Wardens."),
            ]
        )

    def update_dialog(current_time):
        if not dialog_bubble.is_active() and dialog_queue:
            speaker, text = dialog_queue.pop(0)
            dialog_bubble.start(speaker, text, current_time)
        dialog_bubble.update(current_time)

    builder_swatch_rects = []

    # Function to spawn an asteroid
    def spawn_asteroid():
        asteroid_x = random.randint(50, SCREEN_WIDTH - 50)
        asteroid_y = -50
        asteroid_speed = random.uniform(2, 5)
        # 20% chance to spawn a large asteroid
        if random.random() < 0.2:
            size_multiplier = 2  # 2x size
        else:
            size_multiplier = 1
        asteroid = Asteroid(asteroid_x, asteroid_y, asteroid_speed, SCREEN_WIDTH, SCREEN_HEIGHT, current_bg_color, size_multiplier)
        asteroids.append(asteroid)

    # Function to update asteroid colors
    def update_asteroid_colors():
        for asteroid in asteroids:
            asteroid.update_colors(current_bg_color)

    # Function to spawn a health item
    def spawn_health_item():
        health_x = random.randint(15, SCREEN_WIDTH - 15)
        health_y = -15
        health_speed = 5
        health_item = HealthItem(health_x, health_y, health_speed)
        health_items.append(health_item)

    # Function to spawn a power-up
    def spawn_power_up():
        power_x = random.randint(15, SCREEN_WIDTH - 15)
        power_y = -15
        power_speed = 3
        power_type = random.choice(['rapid_fire', 'shotgun'])
        power_up = PowerUp(power_x, power_y, power_speed, power_type)
        power_ups.append(power_up)

    # Function to save top scores
    def save_scores(scores):
        with open(score_file, "w") as file:
            for score, level_achieved, time_sec in scores[:10]:
                file.write(f"{score},{level_achieved},{time_sec}\n")

    # Function to add a new score and update top scores
    def add_score(new_score, new_level, new_time, scores):
        scores.append((new_score, new_level, new_time))
        # Sort scores by score descending, then time ascending
        scores.sort(key=lambda x: (-x[0], x[2]))
        scores = scores[:10]
        save_scores(scores)
        return scores

    # Initialize game by spawning initial enemies
    spawn_enemies(initial=True)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "menu":
                if play_button.is_clicked(event):
                    game_state = "countdown"
                    countdown_start_ticks = pygame.time.get_ticks()
                    countdown_number = 3  # Reset countdown
                    # Play countdown sound
                    if COUNTDOWN_SOUND:
                        COUNTDOWN_SOUND.play()
                    # Reset game variables
                    current_bg_color = get_random_dark_color()
                    if current_bg_color == (0, 0, 0):
                        current_bg_color = (10, 10, 10)  # Slightly off-black
                    player_color = get_opposite_color(current_bg_color)
                    player.reset()
                    if not player.custom_color:
                        player.color = player_color
                    health_bar = HealthBar(player)
                    score_display = ScoreDisplay(SCREEN_WIDTH)
                    enemies.clear()
                    asteroids.clear()
                    health_items.clear()
                    power_ups.clear()
                    enemy_bullets.clear()
                    boss_bullets.clear()
                    level = 1
                    boss = None
                    boss_active = False
                    boss_defeated_current_level = False
                    start_time = pygame.time.get_ticks()
                    elapsed_time = 0
                    score_added = False  # Reset the flag
                    dialog_queue.clear()
                    dialog_bubble.visible = False
                    # Spawn initial enemies
                    spawn_enemies(initial=True)
                if ship_builder_button.is_clicked(event):
                    game_state = "ship_builder"
                if quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

            elif game_state == "countdown":
                pass  # No input handling during countdown

            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player.shoot():
                            if SHOOT_SOUND:
                                SHOOT_SOUND.play()
                    if event.key == pygame.K_z:
                        player.set_weapon_mode("basic")
                    if event.key == pygame.K_x:
                        player.set_weapon_mode("spread")
                # No need to handle movement here; it's handled in the main loop

            elif game_state == "game_over":
                if retry_button.is_clicked(event):
                    game_state = "countdown"
                    countdown_start_ticks = pygame.time.get_ticks()
                    countdown_number = 3  # Reset countdown
                    # Play countdown sound
                    if COUNTDOWN_SOUND:
                        COUNTDOWN_SOUND.play()
                    # Reset game variables
                    current_bg_color = get_random_dark_color()
                    if current_bg_color == (0, 0, 0):
                        current_bg_color = (10, 10, 10)  # Slightly off-black
                    player_color = get_opposite_color(current_bg_color)
                    player.reset()
                    if not player.custom_color:
                        player.color = player_color
                    health_bar = HealthBar(player)
                    score_display = ScoreDisplay(SCREEN_WIDTH)
                    enemies.clear()
                    asteroids.clear()
                    health_items.clear()
                    power_ups.clear()
                    enemy_bullets.clear()
                    boss_bullets.clear()
                    level = 1
                    boss = None
                    boss_active = False
                    boss_defeated_current_level = False
                    start_time = pygame.time.get_ticks()
                    elapsed_time = 0
                    score_added = False  # Reset the flag
                    dialog_queue.clear()
                    dialog_bubble.visible = False
                    # Spawn initial enemies
                    spawn_enemies(initial=True)
                if game_over_quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()
            elif game_state == "ship_builder":
                if builder_back_button.is_clicked(event):
                    persist_save()
                    game_state = "menu"
                if builder_weapon_button.is_clicked(event):
                    if player.buy_weapon_upgrade():
                        persist_save()
                if builder_wing_button.is_clicked(event):
                    if player.buy_wing_upgrade():
                        persist_save()
                if builder_hull_prev.is_clicked(event):
                    current_index = [h["id"] for h in hull_options].index(selected_hull)
                    selected_hull = hull_options[current_index - 1]["id"]
                if builder_hull_next.is_clicked(event):
                    current_index = [h["id"] for h in hull_options].index(selected_hull)
                    selected_hull = hull_options[(current_index + 1) % len(hull_options)]["id"]
                if builder_color_prev.is_clicked(event):
                    current_index = [c["id"] for c in color_options].index(selected_color)
                    selected_color = color_options[current_index - 1]["id"]
                if builder_color_next.is_clicked(event):
                    current_index = [c["id"] for c in color_options].index(selected_color)
                    selected_color = color_options[(current_index + 1) % len(color_options)]["id"]
                if builder_nozzle_prev.is_clicked(event):
                    current_index = [n["id"] for n in nozzle_options].index(selected_nozzle)
                    selected_nozzle = nozzle_options[current_index - 1]["id"]
                if builder_nozzle_next.is_clicked(event):
                    current_index = [n["id"] for n in nozzle_options].index(selected_nozzle)
                    selected_nozzle = nozzle_options[(current_index + 1) % len(nozzle_options)]["id"]
                if builder_confirm_button.is_clicked(event):
                    pending_hull = get_option(hull_options, selected_hull)
                    pending_color = get_option(color_options, selected_color)
                    pending_nozzle = get_option(nozzle_options, selected_nozzle)
                    total_cost = 0
                    if selected_hull not in owned_hulls:
                        total_cost += pending_hull["cost"]
                    if selected_color not in owned_colors:
                        total_cost += pending_color["cost"]
                    if selected_nozzle not in owned_nozzles:
                        total_cost += pending_nozzle["cost"]
                    if player.can_afford(total_cost):
                        player.credits -= total_cost
                        owned_hulls.add(selected_hull)
                        owned_colors.add(selected_color)
                        owned_nozzles.add(selected_nozzle)
                        player.hull_type = selected_hull
                        player.nozzle_type = selected_nozzle
                        player.color = pending_color["color"]
                        player.custom_color = True
                        persist_save()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, color_id in builder_swatch_rects:
                        if rect.collidepoint(event.pos):
                            selected_color = color_id
                            break

        if game_state == "countdown":
            # Calculate countdown number based on time elapsed
            time_since_countdown_start = (pygame.time.get_ticks() - countdown_start_ticks) / 1000  # in seconds
            current_countdown_number = 3 - int(time_since_countdown_start)

            if current_countdown_number != countdown_number:
                countdown_number = current_countdown_number
                if countdown_number > 0:
                    # Play countdown sound
                    if COUNTDOWN_SOUND:
                        COUNTDOWN_SOUND.play()
                elif countdown_number == 0:
                    # Play final countdown sound with higher pitch
                    if COUNTDOWN_FINAL_SOUND:
                        COUNTDOWN_FINAL_SOUND.play()
                else:
                    game_state = "playing"
                    start_time = pygame.time.get_ticks()  # Reset start time
                    if not intro_dialog_shown:
                        enqueue_intro_dialog()
                        intro_dialog_shown = True
                    continue  # Skip to next iteration to prevent drawing countdown at -1

            # Draw countdown screen
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            draw_background(temp_surface)

            # Determine what to display
            if countdown_number > 0:
                display_text = str(countdown_number)
            else:
                display_text = "Go!"

            # Draw countdown number or "Go!"
            countdown_text = COUNTDOWN_FONT.render(display_text, True, WHITE)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            temp_surface.blit(countdown_text, countdown_rect)

            SCREEN.blit(temp_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            continue  # Skip rest of the loop until countdown is over

        if game_state == "playing":
            keys = pygame.key.get_pressed()
            direction_x = 0
            direction_y = 0
            if keys[pygame.K_LEFT]:
                direction_x = -1
            elif keys[pygame.K_RIGHT]:
                direction_x = 1

            if keys[pygame.K_UP]:
                direction_y = -1
            elif keys[pygame.K_DOWN]:
                direction_y = 1

            player.move(direction_x, direction_y)

            # Shooting when space is held down
            if keys[pygame.K_SPACE]:
                if player.shoot():
                    if SHOOT_SOUND:
                        SHOOT_SOUND.play()

            # Update player's position
            player.update_position()

            # Update power-up status
            player.update_power_up()

            # Update timer
            current_ticks = pygame.time.get_ticks()
            elapsed_time = (current_ticks - start_time) / 1000  # Elapsed time in seconds
            update_dialog(current_ticks)

            # Spawn asteroids
            if random.random() < 0.002:
                spawn_asteroid()

            # Spawn health items
            if random.random() < 0.001:
                spawn_health_item()

            # Spawn power-ups
            if random.random() < 0.0005:
                spawn_power_up()

            # Spawn boss
            if level % boss_spawn_level_interval == 0 and not boss_active and not boss_defeated_current_level:
                spawn_boss()

            # Update player bullets
            for bullet in player.bullets[:]:
                bullet.move()
                # Remove bullet if it goes off-screen
                if bullet.y < -bullet.radius:
                    player.bullets.remove(bullet)

            # Update enemies
            for enemy in enemies[:]:
                enemy.update(player.x, player.y, enemies)
                # Update enemy bullets
                for bullet in enemy.bullets[:]:
                    bullet.move()
                    if bullet.y > SCREEN_HEIGHT + bullet.radius or bullet.x < -bullet.radius or bullet.x > SCREEN_WIDTH + bullet.radius:
                        enemy.bullets.remove(bullet)
                    else:
                        enemy_bullets.append(bullet)
                        enemy.bullets.remove(bullet)
                enemy.move()
                # Remove enemies that move off the bottom of the screen
                if enemy.y - enemy.radius_outer > SCREEN_HEIGHT:
                    enemies.remove(enemy)

            # Update enemy bullets
            for bullet in enemy_bullets[:]:
                bullet.move()
                # Remove bullet if it goes off-screen
                if bullet.y > SCREEN_HEIGHT + bullet.radius or bullet.x < -bullet.radius or bullet.x > SCREEN_WIDTH + bullet.radius:
                    enemy_bullets.remove(bullet)

            # Update boss if active
            if boss_active and boss:
                boss_special = boss.update(player)
                if boss_special:
                    effects.start_shake(duration=20)
                    effects.start_flash((int(boss.x), int(boss.y)), color=(255, 80, 180))
                # Update boss bullets
                for bullet in boss.bullets[:]:
                    bullet.move()
                    if bullet.y > SCREEN_HEIGHT + bullet.radius or bullet.y < -bullet.radius or bullet.x < -bullet.radius or bullet.x > SCREEN_WIDTH + bullet.radius:
                        boss.bullets.remove(bullet)
                    else:
                        boss_bullets.append(bullet)
                        boss.bullets.remove(bullet)
                boss.move()

            # Update boss bullets
            for bullet in boss_bullets[:]:
                bullet.move()
                # Remove bullet if it goes off-screen
                if bullet.y > SCREEN_HEIGHT + bullet.radius or bullet.y < -bullet.radius or bullet.x < -bullet.radius or bullet.x > SCREEN_WIDTH + bullet.radius:
                    boss_bullets.remove(bullet)

            # Update asteroids
            for asteroid in asteroids[:]:
                asteroid.move()
                asteroid.rotate()
                if asteroid.y - asteroid.radius_outer > SCREEN_HEIGHT:
                    asteroids.remove(asteroid)

            # Update health items
            for health_item in health_items[:]:
                health_item.move()
                health_item.update_hue()
                if health_item.y - health_item.radius > SCREEN_HEIGHT:
                    health_items.remove(health_item)

            # Update power-ups
            for power_up in power_ups[:]:
                power_up.move()
                if power_up.y - power_up.radius > SCREEN_HEIGHT:
                    power_ups.remove(power_up)

            # Handle player collision with power-ups
            for power_up in power_ups[:]:
                if is_collision(power_up.x, power_up.y, player.x, player.y, power_up.radius, player.radius):
                    if PICKUP_SOUND:
                        PICKUP_SOUND.play()
                    player.activate_power_up(power_up.type)
                    power_ups.remove(power_up)
                    break

            # Handle collisions
            # Player bullets with enemies and boss
            for bullet in player.bullets[:]:
                collision_occurred = False
                # Check collision with enemies
                for enemy in enemies[:]:
                    if is_collision(bullet.x, bullet.y, enemy.x, enemy.y, bullet.radius, enemy.radius_outer):
                        if EXPLOSION_SOUND:
                            EXPLOSION_SOUND.play()
                        score_display.add_score(1)
                        player.add_credits(1)
                        enemies.remove(enemy)
                        # 5% chance to drop health item
                        if random.random() < 0.05:
                            spawn_health_item()
                        collision_occurred = True
                        break  # Exit the enemy loop

                # If collision occurred with enemy, remove bullet and continue to next bullet
                if collision_occurred:
                    player.bullets.remove(bullet)
                    continue  # Move to the next bullet

                # Check collision with boss
                if boss_active and boss:
                    if is_collision(bullet.x, bullet.y, boss.x, boss.y, bullet.radius, boss.radius_outer):
                        if EXPLOSION_SOUND:
                            EXPLOSION_SOUND.play()
                        score_display.add_score(5)
                        player.add_credits(5)
                        boss.health -= 1
                        if boss.health <= 0:
                            player.add_credits(15)
                            boss_active = False
                            boss = None
                            boss_bullets.clear()
                            boss_defeated_current_level = True  # Boss defeated this level
                            # 10% chance to drop health item
                            if random.random() < 0.1:
                                spawn_health_item()
                        # Remove bullet after hitting the boss
                        player.bullets.remove(bullet)
                        continue  # Move to the next bullet

            # Enemy bullets with player
            for bullet in enemy_bullets[:]:
                if is_collision(bullet.x, bullet.y, player.x, player.y, bullet.radius, player.radius):
                    if EXPLOSION_SOUND:
                        EXPLOSION_SOUND.play()
                    player.health -= bullet.damage
                    # Activate shake and flash effects
                    effects.start_shake()
                    effects.start_flash((int(player.x), int(player.y)))
                    enemy_bullets.remove(bullet)
                    if player.health <= 0:
                        game_state = "game_over"
                    continue

            # Boss bullets with player
            for bullet in boss_bullets[:]:
                if is_collision(bullet.x, bullet.y, player.x, player.y, bullet.radius, player.radius):
                    if EXPLOSION_SOUND:
                        EXPLOSION_SOUND.play()
                    player.health -= bullet.damage
                    # Activate shake and flash effects
                    effects.start_shake()
                    effects.start_flash((int(player.x), int(player.y)))
                    boss_bullets.remove(bullet)
                    if player.health <= 0:
                        game_state = "game_over"
                    continue

            # Player with asteroids
            for asteroid in asteroids[:]:
                if is_collision(asteroid.x, asteroid.y, player.x, player.y, asteroid.radius_outer, player.radius):
                    if EXPLOSION_SOUND:
                        EXPLOSION_SOUND.play()
                    player.health -= 2
                    # Activate shake and flash effects
                    effects.start_shake()
                    effects.start_flash((int(player.x), int(player.y)))
                    asteroids.remove(asteroid)
                    if player.health <= 0:
                        game_state = "game_over"

            # Player with health items
            for health_item in health_items[:]:
                if is_collision(health_item.x, health_item.y, player.x, player.y, health_item.radius, player.radius):
                    if PICKUP_SOUND:
                        PICKUP_SOUND.play()
                    player.health = min(player.health + 1, player.max_health)
                    health_items.remove(health_item)

            # Update effects
            effects.update()

            # Draw everything on a temporary surface
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            draw_background(temp_surface)

            # Draw player
            player.draw(temp_surface)

            # Draw enemies
            for enemy in enemies:
                enemy.draw(temp_surface)

            # Draw enemy bullets
            for bullet in enemy_bullets:
                bullet.draw(temp_surface)

            # Draw player bullets
            for bullet in player.bullets:
                bullet.draw(temp_surface)

            # Draw boss
            if boss_active and boss:
                boss.draw(temp_surface)
                boss.draw_health_bar(temp_surface)

            # Draw boss bullets
            for bullet in boss_bullets:
                bullet.draw(temp_surface)

            # Draw asteroids
            for asteroid in asteroids:
                asteroid.draw(temp_surface)

            # Draw health items
            for health_item in health_items:
                health_item.draw(temp_surface)

            # Draw power-ups
            for power_up in power_ups:
                power_up.draw(temp_surface)

            # Draw UI elements
            health_bar.draw(temp_surface)
            score_display.draw(temp_surface)

            # Draw credits and weapon hints
            credits_text = FONT.render(f"Credits: {player.credits}", True, WHITE)
            temp_surface.blit(credits_text, (20, 110))
            upgrade_font = pygame.font.Font(None, 24)
            mode_label = f"Weapon: {player.weapon_mode.title()} [Z/X]"
            mode_text = upgrade_font.render(mode_label, True, WHITE)
            temp_surface.blit(mode_text, (20, 135))

            # Weapon hotbar
            hotbar_width = 120
            hotbar_height = 44
            hotbar_x = SCREEN_WIDTH - hotbar_width - 20
            hotbar_y = SCREEN_HEIGHT - hotbar_height - 20
            pygame.draw.rect(temp_surface, (30, 30, 30), (hotbar_x, hotbar_y, hotbar_width, hotbar_height), border_radius=10)
            pygame.draw.rect(temp_surface, (200, 200, 200), (hotbar_x, hotbar_y, hotbar_width, hotbar_height), width=2, border_radius=10)
            slot_width = (hotbar_width - 12) / 2
            slot_height = hotbar_height - 12
            slot_positions = [
                (hotbar_x + 6, hotbar_y + 6, slot_width, slot_height, "Z", "basic"),
                (hotbar_x + 6 + slot_width, hotbar_y + 6, slot_width, slot_height, "X", "spread"),
            ]
            for x, y, w, h, key_label, mode in slot_positions:
                is_active = player.weapon_mode == mode
                fill_color = (80, 180, 255) if is_active else (50, 50, 50)
                pygame.draw.rect(temp_surface, fill_color, (x, y, w, h), border_radius=8)
                pygame.draw.rect(temp_surface, (220, 220, 220), (x, y, w, h), width=2, border_radius=8)
                label = upgrade_font.render(key_label, True, WHITE)
                label_rect = label.get_rect(center=(x + w / 2, y + h / 2))
                temp_surface.blit(label, label_rect)
                icon_center_x = x + w / 2
                icon_top = y + 6
                icon_bottom = y + h - 6
                if mode == "basic":
                    pygame.draw.line(
                        temp_surface,
                        (255, 255, 255),
                        (icon_center_x, icon_bottom),
                        (icon_center_x, icon_top),
                        width=2,
                    )
                elif mode == "spread":
                    pygame.draw.line(
                        temp_surface,
                        (255, 255, 255),
                        (icon_center_x, icon_bottom),
                        (icon_center_x, icon_top),
                        width=2,
                    )
                    pygame.draw.line(
                        temp_surface,
                        (255, 255, 255),
                        (icon_center_x - 6, icon_bottom),
                        (icon_center_x - 12, icon_top),
                        width=2,
                    )
                    pygame.draw.line(
                        temp_surface,
                        (255, 255, 255),
                        (icon_center_x + 6, icon_bottom),
                        (icon_center_x + 12, icon_top),
                        width=2,
                    )

            # Draw timer
            minutes = int(elapsed_time) // 60
            seconds = int(elapsed_time) % 60
            timer_text = FONT.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
            temp_surface.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 10))

            # Draw power-up cooldown bar
            if player.power_up_active:
                remaining_time = (player.power_up_end_time - pygame.time.get_ticks()) / 1000  # In seconds
                bar_width = 200
                bar_height = 20
                bar_x = (SCREEN_WIDTH - bar_width) / 2
                bar_y = 10
                ratio = remaining_time / 30
                current_bar_width = bar_width * ratio
                pygame.draw.rect(temp_surface, (128, 128, 128), (bar_x, bar_y, bar_width, bar_height))  # Background
                pygame.draw.rect(temp_surface, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))  # Foreground
                # Display power-up type
                font = pygame.font.Font(None, 24)
                text = font.render(player.power_up_active.replace('_', ' ').title(), True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, bar_y + bar_height / 2))
                temp_surface.blit(text, text_rect)

            # Apply effects to the temporary surface
            temp_surface = effects.apply_shake(temp_surface)
            temp_surface = effects.apply_flash(temp_surface)

            # Blit the temporary surface onto the main screen
            SCREEN.blit(temp_surface, (0, 0))

            # Draw dialog bubble on top
            dialog_bubble.draw(SCREEN)

            # Check for level progression
            if not enemies and not boss_active and game_state == "playing":
                level += 1
                score_display.add_score(10)  # Bonus for completing level
                score_display.update_level(level)  # Update the level display
                boss_defeated_current_level = False  # Reset for the new level
                if level in story_events:
                    dialog_queue.append(story_events[level])
                # Change background color
                current_bg_color = get_random_dark_color()
                if current_bg_color == (0, 0, 0):
                    current_bg_color = (10, 10, 10)  # Slightly off-black
                # Update player and enemy colors
                if not player.custom_color:
                    player.color = get_opposite_color(current_bg_color)
                # Play level-up sound
                if LEVELUP_SOUND:
                    LEVELUP_SOUND.play()
                # Spawn new enemies with increased count
                enemies.clear()  # Clear any residual enemies
                spawn_enemies(initial=False)
                # Update asteroid colors
                update_asteroid_colors()

        elif game_state == "menu":
            # Ensure background color is not black
            if current_bg_color == (0, 0, 0):
                current_bg_color = (10, 10, 10)  # Slightly off-black

            # Draw menu on a temporary surface
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            draw_background(temp_surface)
            # Draw title
            title_font = pygame.font.Font(None, 80)
            title_font.set_bold(True)
            title_text = title_font.render("Space Shooter", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
            temp_surface.blit(title_text, title_rect)
            # Draw buttons
            play_button.draw(temp_surface)
            ship_builder_button.draw(temp_surface)
            quit_button.draw(temp_surface)

            # Blit the temporary surface onto the main screen
            SCREEN.blit(temp_surface, (0, 0))

        elif game_state == "game_over":
            if not score_added:
                # Add the final score to top scores before displaying
                top_scores = add_score(score_display.score, level, elapsed_time, top_scores)
                score_added = True  # Set the flag to prevent multiple additions
                persist_save()
            # Draw game over screen on a temporary surface
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 180))  # Semi-transparent black overlay

            # Draw Game Over text
            game_over_text = GAME_OVER_FONT.render("GAME OVER", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            temp_surface.blit(game_over_text, game_over_rect)

            # Draw Top Scores
            scores_title = FONT.render("Top 10 Scores:", True, WHITE)
            scores_title_rect = scores_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            temp_surface.blit(scores_title, scores_title_rect)
            for idx, (score, lvl, time_sec) in enumerate(top_scores):
                minutes = int(time_sec) // 60
                seconds = int(time_sec) % 60
                time_formatted = f"{minutes:02}:{seconds:02}"
                ordinal = f"{idx+1}{'st' if idx==0 else 'nd' if idx==1 else 'rd' if idx==2 else 'th'}"
                score_text = FONT.render(f"{ordinal} Score: {score} LVL {lvl} Time: {time_formatted}", True, WHITE)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70 + idx * 30))
                temp_surface.blit(score_text, score_rect)
            # Draw buttons
            retry_button.draw(temp_surface)
            game_over_quit_button.draw(temp_surface)

            # Blit the temporary surface onto the main screen
            SCREEN.blit(temp_surface, (0, 0))

        elif game_state == "ship_builder":
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            builder_swatch_rects = draw_ship_builder(
                temp_surface,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                player,
                selected_hull,
                selected_color,
                selected_nozzle,
                owned_hulls,
                owned_colors,
                owned_nozzles,
                hull_options,
                color_options,
                nozzle_options,
                {
                    "hull_prev": builder_hull_prev,
                    "hull_next": builder_hull_next,
                    "color_prev": builder_color_prev,
                    "color_next": builder_color_next,
                    "nozzle_prev": builder_nozzle_prev,
                    "nozzle_next": builder_nozzle_next,
                    "weapon": builder_weapon_button,
                    "wing": builder_wing_button,
                    "confirm": builder_confirm_button,
                    "back": builder_back_button,
                },
                FONT,
                pygame.font.Font(None, 30),
                pygame.font.Font(None, 28),
                pygame.font.Font(None, 26),
                draw_background,
            )
            SCREEN.blit(temp_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
