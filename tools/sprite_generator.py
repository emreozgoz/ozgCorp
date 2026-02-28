"""
DARK SANCTUM - Pixel Art Sprite Generator
Matrix Team: UI/UX Designer + Creative Director

Generates 32x32 pixel art sprites for all game entities
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Sprite size
SPRITE_SIZE = 32
BOSS_SPRITE_SIZE = 64

def create_shadow_knight():
    """Dark armored knight with sword"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)

    # Helmet (dark gray)
    pygame.draw.rect(surf, (40, 40, 50), (10, 6, 12, 8))
    # Visor slit (purple glow)
    pygame.draw.rect(surf, (150, 100, 200), (12, 9, 8, 2))

    # Body armor (dark purple-gray)
    pygame.draw.rect(surf, (60, 50, 80), (8, 14, 16, 12))
    # Shoulder pauldrons
    pygame.draw.rect(surf, (50, 40, 70), (6, 14, 6, 4))
    pygame.draw.rect(surf, (50, 40, 70), (20, 14, 6, 4))

    # Arms
    pygame.draw.rect(surf, (40, 40, 50), (6, 18, 4, 8))
    pygame.draw.rect(surf, (40, 40, 50), (22, 18, 4, 8))

    # Sword (silver blade)
    pygame.draw.rect(surf, (180, 180, 200), (26, 12, 4, 12))
    pygame.draw.rect(surf, (100, 80, 120), (25, 18, 6, 2))  # Hilt

    # Legs
    pygame.draw.rect(surf, (45, 40, 60), (10, 26, 5, 6))
    pygame.draw.rect(surf, (45, 40, 60), (17, 26, 5, 6))

    # Purple glow outline
    pygame.draw.rect(surf, (100, 70, 130), (0, 0, SPRITE_SIZE, SPRITE_SIZE), 1)

    return surf

def create_blood_mage():
    """Red-robed mage with staff"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)

    # Hood (dark red)
    pygame.draw.circle(surf, (80, 20, 30), (16, 10), 8)
    # Face shadow
    pygame.draw.circle(surf, (60, 15, 25), (16, 12), 5)
    # Eyes (crimson glow)
    pygame.draw.circle(surf, (200, 50, 70), (14, 11), 1)
    pygame.draw.circle(surf, (200, 50, 70), (18, 11), 1)

    # Robes (blood red)
    pygame.draw.polygon(surf, (120, 30, 40), [
        (16, 16), (8, 32), (24, 32)
    ])
    # Robe trim (gold)
    pygame.draw.lines(surf, (200, 160, 60), False, [(9, 31), (16, 16), (23, 31)], 1)

    # Staff (wooden with crystal)
    pygame.draw.rect(surf, (100, 70, 40), (4, 8, 2, 20))
    # Crystal (red glow)
    pygame.draw.circle(surf, (200, 50, 70), (5, 6), 3)
    pygame.draw.circle(surf, (255, 100, 120), (5, 6), 2)

    # Arms
    pygame.draw.rect(surf, (100, 25, 35), (10, 18, 3, 8))
    pygame.draw.rect(surf, (100, 25, 35), (19, 18, 3, 8))

    return surf

def create_void_guardian():
    """Heavy armored tank with shield"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)

    # Helmet (steel blue)
    pygame.draw.rect(surf, (50, 60, 90), (10, 6, 12, 9))
    # Visor (blue glow)
    pygame.draw.rect(surf, (100, 180, 255), (12, 10, 8, 2))

    # Massive body armor (blue-steel)
    pygame.draw.rect(surf, (60, 75, 110), (6, 15, 20, 14))
    # Chest plate detail
    pygame.draw.rect(surf, (80, 100, 140), (8, 17, 16, 2))

    # Shield (large, left side)
    pygame.draw.rect(surf, (70, 85, 120), (2, 12, 8, 16))
    pygame.draw.circle(surf, (100, 180, 255), (6, 20), 2)

    # Arms (thick)
    pygame.draw.rect(surf, (50, 60, 90), (11, 20, 5, 9))
    pygame.draw.rect(surf, (50, 60, 90), (16, 20, 5, 9))

    # Legs (wide stance)
    pygame.draw.rect(surf, (55, 65, 95), (8, 29, 6, 3))
    pygame.draw.rect(surf, (55, 65, 95), (18, 29, 6, 3))

    return surf

def create_necromancer():
    """Dark robed summoner with skull staff"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)

    # Hood (black)
    pygame.draw.circle(surf, (20, 15, 25), (16, 10), 8)
    # Deep shadow face
    pygame.draw.circle(surf, (10, 5, 15), (16, 12), 5)
    # Eyes (toxic green glow)
    pygame.draw.circle(surf, (120, 200, 80), (14, 11), 1)
    pygame.draw.circle(surf, (120, 200, 80), (18, 11), 1)

    # Robes (black with purple trim)
    pygame.draw.polygon(surf, (25, 20, 35), [
        (16, 16), (7, 32), (25, 32)
    ])
    # Purple arcane symbols
    pygame.draw.circle(surf, (100, 70, 130), (16, 22), 2, 1)

    # Skull staff
    pygame.draw.rect(surf, (80, 70, 60), (26, 10, 2, 18))
    # Skull (bone white)
    pygame.draw.circle(surf, (220, 210, 190), (27, 7), 3)
    pygame.draw.circle(surf, (0, 0, 0), (26, 6), 1)  # Eye socket
    pygame.draw.circle(surf, (0, 0, 0), (28, 6), 1)

    # Green mist effect at feet
    pygame.draw.circle(surf, (100, 180, 70, 100), (12, 30), 4)
    pygame.draw.circle(surf, (100, 180, 70, 100), (20, 30), 4)

    return surf

def create_tempest_ranger():
    """Light armored archer with wind effects"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)

    # Hood (light blue-gray)
    pygame.draw.circle(surf, (70, 90, 110), (16, 10), 7)
    # Face
    pygame.draw.circle(surf, (180, 150, 130), (16, 12), 4)
    # Eyes
    pygame.draw.circle(surf, (80, 120, 160), (14, 11), 1)
    pygame.draw.circle(surf, (80, 120, 160), (18, 11), 1)

    # Light armor (blue-green)
    pygame.draw.rect(surf, (60, 100, 120), (10, 16, 12, 12))
    # Chest piece
    pygame.draw.rect(surf, (70, 110, 130), (11, 17, 10, 3))

    # Bow (held to side)
    pygame.draw.arc(surf, (100, 80, 60), (2, 10, 10, 18), 0.5, 2.6, 2)
    # Arrow
    pygame.draw.line(surf, (150, 130, 100), (6, 18), (12, 18), 1)

    # Legs (agile stance)
    pygame.draw.rect(surf, (50, 85, 105), (11, 28, 4, 4))
    pygame.draw.rect(surf, (50, 85, 105), (17, 28, 4, 4))

    # Wind effect (light blue swirls)
    pygame.draw.circle(surf, (150, 200, 255, 80), (24, 14), 3)
    pygame.draw.circle(surf, (150, 200, 255, 80), (8, 24), 2)

    return surf

# === ENEMIES ===

def create_basic_enemy():
    """Small demon creature"""
    surf = pygame.Surface((24, 24), pygame.SRCALPHA)

    # Body (dark red)
    pygame.draw.circle(surf, (100, 30, 40), (12, 14), 8)

    # Head/horns
    pygame.draw.circle(surf, (110, 35, 45), (12, 8), 6)
    # Horns
    pygame.draw.polygon(surf, (80, 20, 30), [(8, 5), (7, 2), (9, 5)])
    pygame.draw.polygon(surf, (80, 20, 30), [(16, 5), (17, 2), (15, 5)])

    # Eyes (yellow glow)
    pygame.draw.circle(surf, (255, 200, 50), (10, 8), 1)
    pygame.draw.circle(surf, (255, 200, 50), (14, 8), 1)

    # Claws
    pygame.draw.line(surf, (60, 20, 25), (6, 16), (3, 19), 2)
    pygame.draw.line(surf, (60, 20, 25), (18, 16), (21, 19), 2)

    return surf

def create_imp_enemy():
    """Flying imp with wings"""
    surf = pygame.Surface((28, 28), pygame.SRCALPHA)

    # Wings (leathery)
    pygame.draw.polygon(surf, (60, 40, 50), [
        (4, 10), (2, 14), (6, 16)
    ])
    pygame.draw.polygon(surf, (60, 40, 50), [
        (24, 10), (26, 14), (22, 16)
    ])

    # Body (purple-red)
    pygame.draw.circle(surf, (90, 40, 70), (14, 16), 7)

    # Head
    pygame.draw.circle(surf, (100, 45, 75), (14, 10), 5)
    # Horns
    pygame.draw.circle(surf, (70, 30, 50), (11, 7), 2)
    pygame.draw.circle(surf, (70, 30, 50), (17, 7), 2)

    # Eyes (red glow)
    pygame.draw.circle(surf, (200, 50, 50), (12, 10), 1)
    pygame.draw.circle(surf, (200, 50, 50), (16, 10), 1)

    # Tail
    pygame.draw.line(surf, (80, 35, 60), (14, 22), (16, 26), 2)

    return surf

def create_golem_enemy():
    """Large stone golem"""
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)

    # Body (stone gray, large)
    pygame.draw.rect(surf, (80, 75, 70), (10, 18, 20, 20))

    # Head (blocky)
    pygame.draw.rect(surf, (85, 80, 75), (12, 8, 16, 12))

    # Eyes (orange glow)
    pygame.draw.rect(surf, (255, 150, 50), (14, 12, 3, 4))
    pygame.draw.rect(surf, (255, 150, 50), (23, 12, 3, 4))

    # Shoulders (massive)
    pygame.draw.rect(surf, (75, 70, 65), (6, 18, 8, 8))
    pygame.draw.rect(surf, (75, 70, 65), (26, 18, 8, 8))

    # Arms (thick)
    pygame.draw.rect(surf, (70, 65, 60), (4, 26, 6, 10))
    pygame.draw.rect(surf, (70, 65, 60), (30, 26, 6, 10))

    # Cracks (battle damage)
    pygame.draw.line(surf, (50, 45, 40), (15, 10), (17, 18), 1)
    pygame.draw.line(surf, (50, 45, 40), (22, 24), (26, 28), 1)

    return surf

def create_wraith_enemy():
    """Ghostly floating wraith"""
    surf = pygame.Surface((32, 36), pygame.SRCALPHA)

    # Hood (dark ethereal)
    pygame.draw.circle(surf, (40, 40, 60, 200), (16, 12), 9)

    # Face (skull-like, translucent)
    pygame.draw.circle(surf, (60, 60, 80, 150), (16, 14), 6)

    # Eyes (ghostly blue)
    pygame.draw.circle(surf, (100, 180, 255), (13, 13), 2)
    pygame.draw.circle(surf, (100, 180, 255), (19, 13), 2)

    # Tattered robes (flowing, translucent)
    pygame.draw.polygon(surf, (50, 50, 70, 180), [
        (16, 20), (8, 32), (12, 30), (16, 25)
    ])
    pygame.draw.polygon(surf, (50, 50, 70, 180), [
        (16, 20), (24, 32), (20, 30), (16, 25)
    ])

    # Wispy trails (very translucent)
    pygame.draw.circle(surf, (60, 60, 90, 80), (10, 28), 3)
    pygame.draw.circle(surf, (60, 60, 90, 80), (22, 28), 3)
    pygame.draw.circle(surf, (60, 60, 90, 60), (16, 32), 2)

    return surf

# === BOSSES ===

def create_blood_titan():
    """Massive demon boss"""
    surf = pygame.Surface((BOSS_SPRITE_SIZE, BOSS_SPRITE_SIZE), pygame.SRCALPHA)

    # Massive body (crimson)
    pygame.draw.circle(surf, (120, 20, 30), (32, 40), 20)

    # Head (demonic)
    pygame.draw.circle(surf, (140, 25, 35), (32, 20), 14)

    # Horns (large, curved)
    pygame.draw.polygon(surf, (80, 15, 20), [
        (20, 14), (15, 4), (22, 12)
    ])
    pygame.draw.polygon(surf, (80, 15, 20), [
        (44, 14), (49, 4), (42, 12)
    ])

    # Eyes (burning yellow)
    pygame.draw.circle(surf, (255, 200, 50), (26, 18), 3)
    pygame.draw.circle(surf, (255, 200, 50), (38, 18), 3)
    pygame.draw.circle(surf, (255, 100, 0), (26, 18), 2)
    pygame.draw.circle(surf, (255, 100, 0), (38, 18), 2)

    # Massive arms
    pygame.draw.rect(surf, (110, 20, 28), (8, 30, 10, 24))
    pygame.draw.rect(surf, (110, 20, 28), (46, 30, 10, 24))

    # Claws
    for i in range(3):
        pygame.draw.line(surf, (60, 10, 15), (10 + i*3, 54), (8 + i*3, 60), 2)
        pygame.draw.line(surf, (60, 10, 15), (48 + i*3, 54), (50 + i*3, 60), 2)

    # Glowing aura (red)
    pygame.draw.circle(surf, (200, 50, 70, 100), (32, 32), 28, 2)

    return surf

def create_void_reaver():
    """Dark armored boss"""
    surf = pygame.Surface((BOSS_SPRITE_SIZE, BOSS_SPRITE_SIZE), pygame.SRCALPHA)

    # Massive armor (void black with purple)
    pygame.draw.rect(surf, (25, 20, 35), (18, 24, 28, 32))

    # Helmet (menacing)
    pygame.draw.rect(surf, (20, 15, 30), (20, 12, 24, 14))
    # Visor (purple void glow)
    pygame.draw.rect(surf, (150, 100, 200), (24, 18, 16, 4))

    # Shoulder pauldrons (huge)
    pygame.draw.polygon(surf, (30, 25, 40), [
        (12, 24), (18, 24), (18, 32)
    ])
    pygame.draw.polygon(surf, (30, 25, 40), [
        (52, 24), (46, 24), (46, 32)
    ])

    # Giant sword
    pygame.draw.rect(surf, (100, 90, 120), (52, 16, 6, 40))
    pygame.draw.rect(surf, (60, 50, 80), (50, 36, 10, 4))  # Hilt

    # Legs (wide)
    pygame.draw.rect(surf, (22, 18, 32), (20, 56, 10, 7))
    pygame.draw.rect(surf, (22, 18, 32), (34, 56, 10, 7))

    # Purple energy emanating
    pygame.draw.circle(surf, (150, 100, 200, 120), (32, 32), 30, 2)

    return surf

def create_frost_colossus():
    """Ice giant boss"""
    surf = pygame.Surface((BOSS_SPRITE_SIZE, BOSS_SPRITE_SIZE), pygame.SRCALPHA)

    # Icy body (light blue)
    pygame.draw.circle(surf, (150, 200, 230), (32, 38), 22)

    # Head (ice)
    pygame.draw.circle(surf, (160, 210, 240), (32, 18), 12)

    # Eyes (frozen blue)
    pygame.draw.circle(surf, (100, 180, 255), (26, 16), 3)
    pygame.draw.circle(surf, (100, 180, 255), (38, 16), 3)
    pygame.draw.circle(surf, (200, 230, 255), (26, 16), 2)
    pygame.draw.circle(surf, (200, 230, 255), (38, 16), 2)

    # Ice beard
    pygame.draw.polygon(surf, (140, 190, 220), [
        (32, 22), (26, 26), (32, 28), (38, 26)
    ])

    # Massive arms
    pygame.draw.rect(surf, (145, 195, 225), (6, 32, 12, 26))
    pygame.draw.rect(surf, (145, 195, 225), (46, 32, 12, 26))

    # Ice crystals on shoulders
    pygame.draw.polygon(surf, (180, 220, 250), [(10, 30), (12, 26), (14, 30)])
    pygame.draw.polygon(surf, (180, 220, 250), [(54, 30), (52, 26), (50, 30)])

    # Frost aura
    pygame.draw.circle(surf, (150, 200, 255, 80), (32, 32), 28, 3)

    return surf

def create_plague_herald():
    """Diseased boss"""
    surf = pygame.Surface((BOSS_SPRITE_SIZE, BOSS_SPRITE_SIZE), pygame.SRCALPHA)

    # Diseased body (sickly green-brown)
    pygame.draw.circle(surf, (80, 100, 60), (32, 38), 20)

    # Head (bloated)
    pygame.draw.circle(surf, (90, 110, 70), (32, 18), 13)

    # Eyes (toxic green)
    pygame.draw.circle(surf, (120, 200, 80), (26, 17), 3)
    pygame.draw.circle(surf, (120, 200, 80), (38, 17), 3)

    # Mouth (grotesque)
    pygame.draw.line(surf, (60, 80, 40), (26, 24), (38, 24), 2)

    # Pustules/boils (gross details)
    pygame.draw.circle(surf, (100, 120, 80), (24, 14), 2)
    pygame.draw.circle(surf, (100, 120, 80), (40, 20), 2)
    pygame.draw.circle(surf, (100, 120, 80), (28, 40), 3)

    # Arms (thin, diseased)
    pygame.draw.rect(surf, (75, 95, 55), (12, 32, 8, 24))
    pygame.draw.rect(surf, (75, 95, 55), (44, 32, 8, 24))

    # Toxic gas cloud
    pygame.draw.circle(surf, (100, 180, 70, 100), (20, 52), 6)
    pygame.draw.circle(surf, (100, 180, 70, 100), (44, 52), 6)
    pygame.draw.circle(surf, (100, 180, 70, 80), (32, 56), 8)

    # Green aura
    pygame.draw.circle(surf, (120, 200, 80, 100), (32, 32), 26, 2)

    return surf

def create_inferno_lord():
    """Fire demon boss"""
    surf = pygame.Surface((BOSS_SPRITE_SIZE, BOSS_SPRITE_SIZE), pygame.SRCALPHA)

    # Fiery body (orange-red)
    pygame.draw.circle(surf, (180, 60, 20), (32, 38), 21)

    # Head (demonic, aflame)
    pygame.draw.circle(surf, (200, 70, 25), (32, 18), 13)

    # Horns (burning)
    pygame.draw.polygon(surf, (140, 40, 10), [
        (20, 12), (16, 4), (22, 10)
    ])
    pygame.draw.polygon(surf, (140, 40, 10), [
        (44, 12), (48, 4), (42, 10)
    ])

    # Eyes (white-hot)
    pygame.draw.circle(surf, (255, 255, 200), (26, 17), 3)
    pygame.draw.circle(surf, (255, 255, 200), (38, 17), 3)
    pygame.draw.circle(surf, (255, 200, 100), (26, 17), 2)
    pygame.draw.circle(surf, (255, 200, 100), (38, 17), 2)

    # Flaming arms
    pygame.draw.rect(surf, (170, 55, 18), (10, 32, 10, 24))
    pygame.draw.rect(surf, (170, 55, 18), (44, 32, 10, 24))

    # Fire wisps around body
    pygame.draw.circle(surf, (255, 150, 50, 150), (18, 30), 4)
    pygame.draw.circle(surf, (255, 150, 50, 150), (46, 30), 4)
    pygame.draw.circle(surf, (255, 100, 30, 120), (32, 52), 5)

    # Flame aura (multi-layer)
    pygame.draw.circle(surf, (255, 150, 50, 100), (32, 32), 28, 2)
    pygame.draw.circle(surf, (255, 100, 30, 80), (32, 32), 30, 2)

    return surf

def generate_all_sprites():
    """Generate all sprite PNG files"""

    # Create output directories
    os.makedirs('assets/sprites/characters', exist_ok=True)
    os.makedirs('assets/sprites/enemies', exist_ok=True)
    os.makedirs('assets/sprites/bosses', exist_ok=True)

    print("🎨 Generating pixel art sprites...")

    # Characters
    sprites = {
        'characters/shadow_knight.png': create_shadow_knight(),
        'characters/blood_mage.png': create_blood_mage(),
        'characters/void_guardian.png': create_void_guardian(),
        'characters/necromancer.png': create_necromancer(),
        'characters/tempest_ranger.png': create_tempest_ranger(),

        # Enemies
        'enemies/basic.png': create_basic_enemy(),
        'enemies/imp.png': create_imp_enemy(),
        'enemies/golem.png': create_golem_enemy(),
        'enemies/wraith.png': create_wraith_enemy(),

        # Bosses
        'bosses/blood_titan.png': create_blood_titan(),
        'bosses/void_reaver.png': create_void_reaver(),
        'bosses/frost_colossus.png': create_frost_colossus(),
        'bosses/plague_herald.png': create_plague_herald(),
        'bosses/inferno_lord.png': create_inferno_lord(),
    }

    # Save all sprites
    for filename, surf in sprites.items():
        filepath = f'assets/sprites/{filename}'
        pygame.image.save(surf, filepath)
        print(f"✅ Created: {filepath}")

    print(f"\n🎉 Generated {len(sprites)} pixel art sprites!")
    print("📁 Saved to: assets/sprites/")

if __name__ == '__main__':
    generate_all_sprites()
