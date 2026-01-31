# ui/ship_builder.py

import pygame


def get_builder_panels(screen_width, screen_height):
    left_panel = pygame.Rect(30, 130, 420, screen_height - 200)
    center_panel = pygame.Rect(470, 130, 500, screen_height - 200)
    right_panel = pygame.Rect(screen_width - 370, 130, 340, screen_height - 200)
    return left_panel, center_panel, right_panel


def layout_builder_buttons(
    screen_width,
    screen_height,
    right_panel,
    left_panel,
    center_panel,
    buttons,
):
    row_specs = [
        ("hull", right_panel.y + 140),
        ("color", right_panel.y + 200),
        ("nozzle", right_panel.y + 260),
    ]
    button_x = right_panel.x + 20
    for key, y in row_specs:
        left_button = buttons[f"{key}_prev"]
        right_button = buttons[f"{key}_next"]
        left_button.position = (button_x, y)
        left_button.rect.topleft = left_button.position
        right_button.position = (button_x + 230, y)
        right_button.rect.topleft = right_button.position

    buttons["weapon"].position = (left_panel.x + 20, left_panel.y + 510)
    buttons["weapon"].rect.topleft = buttons["weapon"].position
    buttons["wing"].position = (left_panel.x + 20, left_panel.y + 570)
    buttons["wing"].rect.topleft = buttons["wing"].position
    buttons["confirm"].position = (center_panel.x + 90, center_panel.y + 520)
    buttons["confirm"].rect.topleft = buttons["confirm"].position
    buttons["back"].position = (screen_width - 260, screen_height - 90)
    buttons["back"].rect.topleft = buttons["back"].position


def draw_ship_builder(
    surface,
    screen_width,
    screen_height,
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
    buttons,
    font,
    selection_font,
    info_font,
    detail_font,
    draw_background,
):
    draw_background(surface)

    title_font = pygame.font.Font(None, 70)
    title_font.set_bold(True)
    title_text = title_font.render("Ship Builder", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, 70))
    surface.blit(title_text, title_rect)

    credits_text = font.render(f"Credits: {player.credits}", True, (255, 255, 255))
    surface.blit(credits_text, (40, 40))

    panel_color = (20, 20, 30)
    panel_border = (120, 120, 140)
    left_panel, center_panel, right_panel = get_builder_panels(screen_width, screen_height)
    for panel in [left_panel, center_panel, right_panel]:
        pygame.draw.rect(surface, panel_color, panel, border_radius=16)
        pygame.draw.rect(surface, panel_border, panel, width=2, border_radius=16)

    layout_builder_buttons(screen_width, screen_height, right_panel, left_panel, center_panel, buttons)

    preview_x = center_panel.centerx
    preview_y = center_panel.y + 170
    preview_player = player.clone_for_preview(preview_x, preview_y)
    preview_player.hull_type = selected_hull
    preview_player.nozzle_type = selected_nozzle
    preview_player.color = get_option(color_options, selected_color)["color"]
    preview_player.draw(surface)

    hull_option = get_option(hull_options, selected_hull)
    color_option = get_option(color_options, selected_color)
    nozzle_option = get_option(nozzle_options, selected_nozzle)
    hull_owned = selected_hull in owned_hulls
    color_owned = selected_color in owned_colors
    nozzle_owned = selected_nozzle in owned_nozzles

    hull_status = "Owned" if hull_owned else f"{hull_option['cost']}c"
    color_status = "Owned" if color_owned else f"{color_option['cost']}c"
    nozzle_status = "Owned" if nozzle_owned else f"{nozzle_option['cost']}c"

    selection_color = (255, 255, 255)
    label_color = (200, 200, 220)
    status_color = (200, 200, 200)

    label_y = center_panel.y + 250
    option_x = center_panel.x + 140
    label_x = center_panel.x + 30
    status_x = center_panel.x + 360
    labels = [("Hull", hull_option["label"], hull_status), ("Color", color_option["label"], color_status), ("Nozzle", nozzle_option["label"], nozzle_status)]
    for idx, (label, option_label, status) in enumerate(labels):
        y = label_y + idx * 40
        label_text = selection_font.render(label, True, label_color)
        option_text = selection_font.render(option_label, True, selection_color)
        status_text = pygame.font.Font(None, 24).render(status, True, status_color)
        surface.blit(label_text, (label_x, y))
        surface.blit(option_text, (option_x, y))
        surface.blit(status_text, (status_x, y + 5))

    detail_lines = [
        "Hull: Balanced core frame.",
        "Nozzle: Exhaust profile.",
        "Color: Cosmetic paint coat.",
    ]
    for idx, line in enumerate(detail_lines):
        detail_text = detail_font.render(line, True, (180, 180, 200))
        surface.blit(detail_text, (center_panel.x + 30, center_panel.y + 415 + idx * 25))

    pending_cost = 0
    if not hull_owned:
        pending_cost += hull_option["cost"]
    if not color_owned:
        pending_cost += color_option["cost"]
    if not nozzle_owned:
        pending_cost += nozzle_option["cost"]
    confirm_label = f"Confirm ({pending_cost}c)" if pending_cost else "Confirm (Owned)"
    confirm_text = selection_font.render(confirm_label, True, (255, 255, 255))
    surface.blit(confirm_text, (center_panel.x + 30, center_panel.y + 390))

    left_header_font = pygame.font.Font(None, 36)
    left_header_font.set_bold(True)
    upgrades_title = left_header_font.render("Upgrades", True, (255, 255, 255))
    surface.blit(upgrades_title, (left_panel.x + 20, left_panel.y + 20))

    weapon_cost = 6 * player.weapon_level if player.weapon_level < 3 else None
    wing_cost = 5 * player.wing_level if player.wing_level < 3 else None
    weapon_info = (
        f"Weapon Mk {player.weapon_level} -> {player.weapon_level + 1} ({weapon_cost}c)"
        if weapon_cost
        else "Weapon Mk 3 (Max)"
    )
    wing_info = (
        f"Wings Mk {player.wing_level} -> {player.wing_level + 1} ({wing_cost}c)"
        if wing_cost
        else "Wings Mk 3 (Max)"
    )
    weapon_info_text = info_font.render(weapon_info, True, (255, 255, 255))
    wing_info_text = info_font.render(wing_info, True, (255, 255, 255))
    surface.blit(weapon_info_text, (left_panel.x + 20, left_panel.y + 80))
    surface.blit(wing_info_text, (left_panel.x + 20, left_panel.y + 120))

    tips_font = pygame.font.Font(None, 26)
    tips = [
        "Weapon modes: Z (Basic), X (Spread)",
        "Select parts, then confirm to buy/apply.",
        "Owned items are free to swap.",
    ]
    for idx, tip in enumerate(tips):
        tip_text = tips_font.render(tip, True, (255, 255, 255))
        surface.blit(tip_text, (left_panel.x + 20, left_panel.y + 200 + idx * 26))

    stats_title = left_header_font.render("Current Build", True, (255, 255, 255))
    surface.blit(stats_title, (left_panel.x + 20, left_panel.y + 300))

    current_color_id = next((c["id"] for c in color_options if c["color"] == player.color), selected_color)
    stats_text = [
        f"Hull: {get_option(hull_options, player.hull_type)['label']}",
        f"Nozzle: {get_option(nozzle_options, player.nozzle_type)['label']}",
        f"Color: {get_option(color_options, current_color_id)['label']}",
        f"Weapon Mk {player.weapon_level}",
        f"Wings Mk {player.wing_level}",
    ]
    for idx, line in enumerate(stats_text):
        line_text = info_font.render(line, True, (255, 255, 255))
        surface.blit(line_text, (left_panel.x + 20, left_panel.y + 330 + idx * 26))

    stat_label_font = pygame.font.Font(None, 26)
    stat_bar_x = center_panel.x + 30
    stat_bar_y = center_panel.y + 500
    stat_width = center_panel.width - 60
    stat_height = 12
    agility = min(player.wing_level / 3, 1)
    firepower = min(player.weapon_level / 3, 1)
    for label, value, offset in [("Agility", agility, 0), ("Firepower", firepower, 28)]:
        label_text = stat_label_font.render(label, True, (255, 255, 255))
        surface.blit(label_text, (stat_bar_x, stat_bar_y + offset - 18))
        pygame.draw.rect(surface, (60, 60, 60), (stat_bar_x, stat_bar_y + offset, stat_width, stat_height), border_radius=6)
        pygame.draw.rect(
            surface,
            (0, 200, 160),
            (stat_bar_x, stat_bar_y + offset, stat_width * value, stat_height),
            border_radius=6,
        )

    right_header_font = pygame.font.Font(None, 36)
    right_header_font.set_bold(True)
    options_title = right_header_font.render("Options", True, (255, 255, 255))
    surface.blit(options_title, (right_panel.x + 20, right_panel.y + 20))

    swatch_y = right_panel.y + 520
    swatch_x = right_panel.x + 20
    swatch_size = 24
    swatch_spacing = 10
    swatch_label = pygame.font.Font(None, 24).render("Colors", True, (255, 255, 255))
    surface.blit(swatch_label, (swatch_x, swatch_y - 26))
    swatch_rects = []
    for color_option in color_options:
        color_rect = pygame.Rect(swatch_x, swatch_y, swatch_size, swatch_size)
        pygame.draw.rect(surface, color_option["color"], color_rect, border_radius=4)
        is_selected = color_option["id"] == selected_color
        border = (255, 255, 255) if is_selected else (120, 120, 120)
        pygame.draw.rect(surface, border, color_rect, width=2, border_radius=4)
        swatch_rects.append((color_rect, color_option["id"]))
        swatch_x += swatch_size + swatch_spacing

    option_font = pygame.font.Font(None, 28)
    for idx, label in enumerate([hull_option["label"], color_option["label"], nozzle_option["label"]]):
        y = right_panel.y + 146 + idx * 60
        label_text = option_font.render(label, True, (255, 255, 255))
        surface.blit(label_text, (right_panel.x + 100, y))

    for button in [
        buttons["hull_prev"],
        buttons["hull_next"],
        buttons["color_prev"],
        buttons["color_next"],
        buttons["nozzle_prev"],
        buttons["nozzle_next"],
        buttons["weapon"],
        buttons["wing"],
        buttons["confirm"],
        buttons["back"],
    ]:
        button.draw(surface)

    return swatch_rects


def get_option(options, option_id):
    for option in options:
        if option["id"] == option_id:
            return option
    return options[0]
