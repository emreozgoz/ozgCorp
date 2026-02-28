#!/usr/bin/env python3
"""
Test weapon icon visibility on simulated level-up screen background
Sprint 28: Verify icons are visible against dark gothic UI
"""

import pygame
import sys
sys.path.insert(0, '.')

from src.core.asset_manager import asset_manager
from config.ui_theme import (
    GOTHIC_BLACK, GOTHIC_PURPLE, GOTHIC_BONE, GOTHIC_GOLD,
    GOTHIC_SHADOW, UI_SELECTED, PADDING_LARGE
)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Sprint 28: Level-Up Icon Visibility Test")

# Gothic fonts
title_font = pygame.font.Font(None, 72)
header_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 36)

def draw_gothic_card(surface, x, y, width, height, selected=False):
    """Draw a gothic weapon card background (same as in main.py)"""
    border_color = GOTHIC_GOLD if selected else GOTHIC_PURPLE
    border_width = 6 if selected else 3

    # Card background (dark shadow)
    pygame.draw.rect(surface, GOTHIC_SHADOW, (x, y, width, height), border_radius=8)

    # Card border
    pygame.draw.rect(surface, border_color, (x, y, width, height), border_width, border_radius=8)

def render_level_up_screen_test():
    """Render a simulated level-up screen with weapon icons"""

    # Dark overlay (same as actual game)
    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Header
    header_surf = title_font.render("LEVEL UP!", True, GOTHIC_GOLD)
    header_rect = header_surf.get_rect(center=(640, 100))
    screen.blit(header_surf, header_rect)

    # Weapon cards (3 cards side-by-side)
    weapon_ids = ['arcane_seeker', 'blood_whip', 'lightning_orb']
    weapon_names = ['Arcane Seeker', 'Blood Whip', 'Lightning Orb']

    card_width = 280
    card_height = 350
    card_spacing = 40
    total_width = (card_width * 3) + (card_spacing * 2)
    start_x = (1280 - total_width) // 2
    start_y = 200

    for i, (weapon_id, weapon_name) in enumerate(zip(weapon_ids, weapon_names)):
        x = start_x + (i * (card_width + card_spacing))

        # Draw card background
        selected = (i == 1)  # Middle card selected
        draw_gothic_card(screen, x, start_y, card_width, card_height, selected)

        # WEAPON ICON (Sprint 28: Pixel art sprite)
        weapon_icon = asset_manager.get_sprite(f'weapon_{weapon_id}')
        if weapon_icon:
            # Scale up 2x for visibility (32x32 → 64x64)
            scaled_icon = pygame.transform.scale(weapon_icon, (64, 64))
            icon_rect = scaled_icon.get_rect(center=(x + card_width // 2, start_y + 80))
            screen.blit(scaled_icon, icon_rect)

            # Debug info
            icon_status = "✅ VISIBLE"
        else:
            # Fallback: emoji
            icon_surf = header_font.render("❌", True, (255, 100, 100))
            icon_rect = icon_surf.get_rect(center=(x + card_width // 2, start_y + 80))
            screen.blit(icon_surf, icon_rect)
            icon_status = "❌ MISSING"

        # Weapon name
        name_surf = text_font.render(weapon_name, True, GOTHIC_BONE)
        name_rect = name_surf.get_rect(center=(x + card_width // 2, start_y + 160))
        screen.blit(name_surf, name_rect)

        # Level indicator
        level_text = "Lv 1 → 2" if i == 0 else "NEW!"
        level_surf = text_font.render(level_text, True, GOTHIC_PURPLE)
        level_rect = level_surf.get_rect(center=(x + card_width // 2, start_y + 200))
        screen.blit(level_surf, level_rect)

        # Status label (for debugging)
        status_surf = text_font.render(icon_status, True, (100, 255, 100) if "✅" in icon_status else (255, 100, 100))
        status_rect = status_surf.get_rect(center=(x + card_width // 2, start_y + 280))
        screen.blit(status_surf, status_rect)

    # Instructions
    instructions = "If you can see weapon icons above, brightness fix worked!"
    instr_surf = text_font.render(instructions, True, GOTHIC_GOLD)
    instr_rect = instr_surf.get_rect(center=(640, 600))
    screen.blit(instr_surf, instr_rect)

    # Controls
    controls = "Press SPACE to see all 5 weapon icons | ESC to quit"
    controls_surf = text_font.render(controls, True, GOTHIC_BONE)
    controls_rect = controls_surf.get_rect(center=(640, 650))
    screen.blit(controls_surf, controls_rect)

def render_all_weapons_test():
    """Show all 5 weapon icons in a grid for visibility testing"""

    # Dark background
    screen.fill(GOTHIC_BLACK)

    # Header
    header_surf = title_font.render("All 5 Weapon Icons - Visibility Test", True, GOTHIC_GOLD)
    header_rect = header_surf.get_rect(center=(640, 80))
    screen.blit(header_surf, header_rect)

    # All weapons
    weapon_ids = ['arcane_seeker', 'blood_whip', 'lightning_orb', 'toxic_cloud', 'holy_barrier']
    weapon_names = ['Arcane Seeker', 'Blood Whip', 'Lightning Orb', 'Toxic Cloud', 'Holy Barrier']
    weapon_colors = ['Purple', 'Red', 'Yellow', 'Green', 'Gold']

    # Draw in a horizontal row
    card_width = 200
    card_spacing = 30
    total_width = (card_width * 5) + (card_spacing * 4)
    start_x = (1280 - total_width) // 2
    start_y = 200

    for i, (weapon_id, weapon_name, color) in enumerate(zip(weapon_ids, weapon_names, weapon_colors)):
        x = start_x + (i * (card_width + card_spacing))

        # Card background
        draw_gothic_card(screen, x, start_y, card_width, 300, False)

        # Weapon icon
        weapon_icon = asset_manager.get_sprite(f'weapon_{weapon_id}')
        if weapon_icon:
            # Scale up 2x
            scaled_icon = pygame.transform.scale(weapon_icon, (64, 64))
            icon_rect = scaled_icon.get_rect(center=(x + card_width // 2, start_y + 70))
            screen.blit(scaled_icon, icon_rect)
            status = "✅"
        else:
            status = "❌"

        # Weapon name (split into two lines if needed)
        words = weapon_name.split()
        for j, word in enumerate(words):
            word_surf = text_font.render(word, True, GOTHIC_BONE)
            word_rect = word_surf.get_rect(center=(x + card_width // 2, start_y + 150 + (j * 35)))
            screen.blit(word_surf, word_rect)

        # Color label
        color_surf = text_font.render(f"({color})", True, GOTHIC_PURPLE)
        color_rect = color_surf.get_rect(center=(x + card_width // 2, start_y + 220))
        screen.blit(color_surf, color_rect)

        # Status
        status_surf = header_font.render(status, True, (100, 255, 100) if status == "✅" else (255, 100, 100))
        status_rect = status_surf.get_rect(center=(x + card_width // 2, start_y + 260))
        screen.blit(status_surf, status_rect)

    # Instructions
    instructions = "ESC to go back | Q to quit test"
    instr_surf = text_font.render(instructions, True, GOTHIC_GOLD)
    instr_rect = instr_surf.get_rect(center=(640, 600))
    screen.blit(instr_surf, instr_rect)

def main():
    """Main test loop"""
    clock = pygame.time.Clock()
    running = True
    show_all = False

    print("🎨 Sprint 28: Level-Up Icon Visibility Test")
    print("=" * 70)
    print("Testing weapon icon visibility on dark gothic backgrounds...")
    print()

    # Check if all icons loaded
    weapon_ids = ['arcane_seeker', 'blood_whip', 'lightning_orb', 'toxic_cloud', 'holy_barrier']
    for weapon_id in weapon_ids:
        icon = asset_manager.get_sprite(f'weapon_{weapon_id}')
        if icon:
            print(f"✅ {weapon_id}: Icon loaded ({icon.get_width()}x{icon.get_height()})")
        else:
            print(f"❌ {weapon_id}: Icon MISSING!")

    print()
    print("Controls:")
    print("  SPACE - Toggle between level-up screen and all weapons")
    print("  ESC/Q - Quit test")
    print("=" * 70)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    show_all = not show_all

        # Render test screen
        if show_all:
            render_all_weapons_test()
        else:
            render_level_up_screen_test()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("\n✅ Test complete!")

if __name__ == '__main__':
    main()
