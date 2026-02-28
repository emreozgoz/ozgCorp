#!/usr/bin/env python3
"""
Debug weapon icons - check if they're loading and visible
"""

import pygame
import sys
sys.path.insert(0, '.')

from src.core.asset_manager import asset_manager

pygame.init()

print("🔍 Weapon Icon Debug Test")
print("=" * 70)

weapon_ids = ['arcane_seeker', 'blood_whip', 'lightning_orb', 'toxic_cloud', 'holy_barrier']

for weapon_id in weapon_ids:
    sprite_key = f'weapon_{weapon_id}'
    icon = asset_manager.get_sprite(sprite_key)

    if icon:
        print(f"✅ {weapon_id:20s} - Loaded ({icon.get_width()}x{icon.get_height()})")

        # Check if icon has any non-transparent pixels
        has_visible_pixels = False
        for x in range(icon.get_width()):
            for y in range(icon.get_height()):
                r, g, b, a = icon.get_at((x, y))
                if a > 0:  # Has alpha
                    has_visible_pixels = True
                    break
            if has_visible_pixels:
                break

        if has_visible_pixels:
            print(f"   └─ Has visible pixels ✅")
        else:
            print(f"   └─ ALL TRANSPARENT ❌")
    else:
        print(f"❌ {weapon_id:20s} - NOT FOUND")

print("=" * 70)
print("\nTesting sprite blitting to screen...")

screen = pygame.display.set_mode((640, 480))
screen.fill((30, 20, 40))  # Dark background like game

# Try to blit all icons
x_offset = 50
for weapon_id in weapon_ids:
    icon = asset_manager.get_sprite(f'weapon_{weapon_id}')
    if icon:
        scaled = pygame.transform.scale(icon, (64, 64))
        screen.blit(scaled, (x_offset, 200))
        x_offset += 80

pygame.display.flip()

print("✅ Icons blitted to screen")
print("   If you see colored icons, they're working!")
print("   Press any key to close...")

# Wait for key press
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False

pygame.quit()
print("\n✅ Debug test complete")
