"""
DARK SANCTUM - Gothic UI Theme
Matrix Team: UI/UX Designer + Creative Director

Sprint 24: Professional gothic UI design system
"""

import pygame

# === GOTHIC COLOR PALETTE ===

# Primary Colors
GOTHIC_BLACK = (15, 10, 20)  # Deep shadow black
GOTHIC_PURPLE = (75, 45, 95)  # Royal dark purple
GOTHIC_BLOOD = (120, 20, 30)  # Deep blood red
GOTHIC_GOLD = (200, 160, 60)  # Antique gold

# Secondary Colors
GOTHIC_SILVER = (180, 180, 190)  # Weathered silver
GOTHIC_BONE = (220, 210, 190)  # Aged bone
GOTHIC_SHADOW = (30, 20, 35)  # Shadow purple
GOTHIC_MIST = (100, 95, 110)  # Misty gray

# Accent Colors
GLOW_PURPLE = (150, 100, 200)  # Magical purple glow
GLOW_CRIMSON = (200, 50, 70)  # Crimson glow
GLOW_ARCANE = (100, 180, 255)  # Arcane blue glow
GLOW_TOXIC = (120, 200, 80)  # Toxic green glow

# UI State Colors
UI_HOVER = (100, 70, 120)  # Hover state
UI_SELECTED = (140, 90, 160)  # Selected state
UI_DISABLED = (60, 55, 65)  # Disabled state
UI_DANGER = (180, 40, 50)  # Danger/warning

# Transparency
OVERLAY_DARK = (10, 5, 15, 200)  # Dark overlay with alpha
OVERLAY_LIGHT = (40, 30, 50, 150)  # Light overlay


# === FONT SIZES ===

FONT_TINY = 16
FONT_SMALL = 20
FONT_MEDIUM = 28
FONT_LARGE = 40
FONT_HUGE = 56
FONT_TITLE = 72


# === UI ELEMENT SIZES ===

# Borders
BORDER_THIN = 1
BORDER_MEDIUM = 2
BORDER_THICK = 3
BORDER_ORNATE = 5

# Padding
PADDING_SMALL = 8
PADDING_MEDIUM = 16
PADDING_LARGE = 24
PADDING_HUGE = 32

# Spacing
SPACING_TINY = 4
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 24

# Corners
CORNER_RADIUS_SMALL = 4
CORNER_RADIUS_MEDIUM = 8
CORNER_RADIUS_LARGE = 12


# === ANIMATION TIMING ===

ANIM_FAST = 0.1  # Fast transition (100ms)
ANIM_NORMAL = 0.2  # Normal transition (200ms)
ANIM_SLOW = 0.3  # Slow transition (300ms)
ANIM_PULSE = 1.5  # Pulse cycle duration


# === UI COMPONENTS ===

class GothicPanel:
    """Gothic-styled panel with ornate borders"""

    @staticmethod
    def draw(surface: pygame.Surface, rect: pygame.Rect,
             bg_color=GOTHIC_SHADOW, border_color=GOTHIC_GOLD,
             border_width=BORDER_MEDIUM, alpha=255):
        """Draw gothic panel with decorative border"""

        # Create surface with alpha if needed
        if alpha < 255:
            panel_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            panel_surf.fill((*bg_color, alpha))
            surface.blit(panel_surf, rect)
        else:
            pygame.draw.rect(surface, bg_color, rect)

        # Outer border
        pygame.draw.rect(surface, border_color, rect, border_width)

        # Inner shadow line
        inner_rect = rect.inflate(-border_width * 2, -border_width * 2)
        pygame.draw.rect(surface, GOTHIC_BLACK, inner_rect, 1)

        # Corner ornaments (small triangles)
        corner_size = 8
        corners = [
            (rect.left + border_width, rect.top + border_width),  # Top-left
            (rect.right - border_width, rect.top + border_width),  # Top-right
            (rect.left + border_width, rect.bottom - border_width),  # Bottom-left
            (rect.right - border_width, rect.bottom - border_width),  # Bottom-right
        ]

        for i, (cx, cy) in enumerate(corners):
            # Draw small ornamental diamond
            if i == 0:  # Top-left
                points = [(cx, cy + corner_size), (cx + corner_size, cy), (cx, cy - corner_size), (cx - corner_size, cy)]
            elif i == 1:  # Top-right
                points = [(cx, cy + corner_size), (cx + corner_size, cy), (cx, cy - corner_size), (cx - corner_size, cy)]
            elif i == 2:  # Bottom-left
                points = [(cx, cy + corner_size), (cx + corner_size, cy), (cx, cy - corner_size), (cx - corner_size, cy)]
            else:  # Bottom-right
                points = [(cx, cy + corner_size), (cx + corner_size, cy), (cx, cy - corner_size), (cx - corner_size, cy)]

            pygame.draw.polygon(surface, border_color, points, 1)


class GothicButton:
    """Gothic-styled button with hover effects"""

    @staticmethod
    def draw(surface: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font,
             is_hovered=False, is_selected=False, is_disabled=False):
        """Draw gothic button"""

        # Determine colors based on state
        if is_disabled:
            bg_color = UI_DISABLED
            border_color = GOTHIC_MIST
            text_color = GOTHIC_SHADOW
        elif is_selected:
            bg_color = UI_SELECTED
            border_color = GLOW_PURPLE
            text_color = GOTHIC_BONE
        elif is_hovered:
            bg_color = UI_HOVER
            border_color = GOTHIC_GOLD
            text_color = GOTHIC_GOLD
        else:
            bg_color = GOTHIC_SHADOW
            border_color = GOTHIC_PURPLE
            text_color = GOTHIC_SILVER

        # Draw panel
        GothicPanel.draw(surface, rect, bg_color, border_color, BORDER_MEDIUM)

        # Draw text centered
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)


class GothicProgressBar:
    """Gothic-styled progress bar"""

    @staticmethod
    def draw(surface: pygame.Surface, rect: pygame.Rect, progress: float,
             fg_color=GOTHIC_GOLD, bg_color=GOTHIC_BLACK, border_color=GOTHIC_SILVER):
        """Draw gothic progress bar (progress 0.0 to 1.0)"""

        # Background
        pygame.draw.rect(surface, bg_color, rect)

        # Foreground (filled portion)
        if progress > 0:
            fill_width = int(rect.width * progress)
            fill_rect = pygame.Rect(rect.left, rect.top, fill_width, rect.height)
            pygame.draw.rect(surface, fg_color, fill_rect)

        # Border
        pygame.draw.rect(surface, border_color, rect, BORDER_MEDIUM)


class GothicHeader:
    """Gothic-styled header text with decoration"""

    @staticmethod
    def draw(surface: pygame.Surface, text: str, y: int, font: pygame.font.Font,
             color=GOTHIC_GOLD, decoration=True):
        """Draw gothic header with optional decoration lines"""

        # Render text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(surface.get_width() // 2, y))
        surface.blit(text_surf, text_rect)

        if decoration:
            # Decorative lines on both sides
            line_y = text_rect.centery
            line_left_start = 50
            line_left_end = text_rect.left - 20
            line_right_start = text_rect.right + 20
            line_right_end = surface.get_width() - 50

            # Left line
            pygame.draw.line(surface, color,
                           (line_left_start, line_y),
                           (line_left_end, line_y), 2)

            # Right line
            pygame.draw.line(surface, color,
                           (line_right_start, line_y),
                           (line_right_end, line_y), 2)

            # Small diamonds at line ends
            diamond_size = 4
            for x in [line_left_start, line_left_end, line_right_start, line_right_end]:
                points = [
                    (x, line_y - diamond_size),
                    (x + diamond_size, line_y),
                    (x, line_y + diamond_size),
                    (x - diamond_size, line_y)
                ]
                pygame.draw.polygon(surface, color, points)


# === HELPER FUNCTIONS ===

def create_gothic_surface(width: int, height: int, alpha=True):
    """Create a surface with gothic background"""
    if alpha:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
    else:
        surface = pygame.Surface((width, height))

    surface.fill(GOTHIC_BLACK)
    return surface


def draw_ornate_border(surface: pygame.Surface, color=GOTHIC_GOLD, width=BORDER_ORNATE):
    """Draw ornate border around entire surface"""
    rect = surface.get_rect()

    # Outer border
    pygame.draw.rect(surface, color, rect, width)

    # Inner accent line
    inner_rect = rect.inflate(-width * 2, -width * 2)
    pygame.draw.rect(surface, GOTHIC_PURPLE, inner_rect, 1)


# === UI/UX DESIGNER NOTE ===
# Sprint 24: Gothic UI Theme
# - Professional AAA-quality UI design system
# - Consistent color palette inspired by gothic architecture
# - Reusable UI components for menus, buttons, panels
# - Animation timing constants for smooth transitions
# - Ornamental details without being overwhelming
# - Focus on readability and visual hierarchy


