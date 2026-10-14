# entities/blocks.py
import pygame
from config import *
from .base import SolidBlock


class NeonBlock(SolidBlock):
    """Khối vuông phát sáng Neon dùng trong Map 1 (Hỗ trợ đinh tán trắng, dây xích và đèn đỉnh/đáy)."""

    def __init__(self, x, y, color=BLOCK_PURPLE, has_dot=False, top_glow=None, bottom_glow=None, has_chain=False):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.has_dot = has_dot
        self.top_glow = top_glow
        self.bottom_glow = bottom_glow
        self.has_chain = has_chain
        self.surf = self._bake()

    def _bake(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (15, 5, 30), (0, 0, self.w, self.h), border_radius=4)
        m = 4
        pygame.draw.rect(surf, self.color, (m, m, self.w - m * 2, self.h - m * 2), border_radius=4)
        bright = tuple(min(255, c + 45) for c in self.color)
        cm = 10
        pygame.draw.rect(surf, bright, (cm, cm, self.w - cm * 2, self.h - cm * 2), border_radius=3)
        pygame.draw.rect(surf, tuple(min(255, c + 70) for c in self.color), (m, m, self.w - m * 2, self.h - m * 2), 2, border_radius=4)
        if self.has_dot:
            c = (self.w // 2, self.h // 2)
            pygame.draw.circle(surf, (25, 10, 45), c, 9)
            pygame.draw.circle(surf, WHITE, c, 6)
        return surf

    def _draw_glow_bar(self, surface, sx, sy, glow_color, is_top=True):
        stripe_h = 6
        bar_y = sy - stripe_h if is_top else sy + self.h
        pygame.draw.rect(surface, WHITE, (sx, bar_y, self.w, stripe_h))
        for offset in range(0, self.w, 12):
            pygame.draw.rect(surface, BLACK, (sx + offset, bar_y, 6, stripe_h))

        glow_h = 28
        glow_surf = pygame.Surface((self.w, glow_h), pygame.SRCALPHA)
        for i in range(glow_h):
            ratio = (glow_h - i) / glow_h if not is_top else (i / glow_h)
            alpha = int(130 * (ratio ** 1.6))
            pygame.draw.line(glow_surf, (*glow_color, alpha), (0, i), (self.w, i))
        dest_y = bar_y - glow_h if is_top else bar_y + stripe_h
        surface.blit(glow_surf, (sx, dest_y), special_flags=pygame.BLEND_RGBA_ADD)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        if self.has_chain:
            cx = sx + self.w // 2
            pygame.draw.rect(surface, (10, 90, 240), (cx - 14, sy - 8, 28, 8), border_radius=3)
            curr_y, idx = sy - 16, 0
            while curr_y > -20:
                if idx % 2 == 0:
                    pygame.draw.rect(surface, (15, 115, 255), (cx - 6, curr_y - 12, 12, 18), 3, border_radius=4)
                else:
                    pygame.draw.line(surface, (60, 160, 255), (cx, curr_y - 10), (cx, curr_y + 4), 4)
                curr_y -= 14
                idx += 1

        surface.blit(self.surf, (sx, sy))
        if self.top_glow:
            self._draw_glow_bar(surface, sx, sy, self.top_glow, is_top=True)
        if self.bottom_glow:
            self._draw_glow_bar(surface, sx, sy, self.bottom_glow, is_top=False)


class ClassicDarkBlock(SolidBlock):
    """Khối đen chuyển sắc viền trắng phát sáng (Hình mẫu 11, 15, 16)."""

    def __init__(self, x, y, color=(220, 20, 25), height=TILE_SIZE, ring_attach=None):
        super().__init__(x, y, TILE_SIZE, height, ring_attach=ring_attach)
        self.color = color
        self.surf = self._bake()

    def _bake(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        for row in range(self.h):
            ratio = row / float(max(1, self.h - 1))
            r = int(self.color[0] * (ratio ** 1.8) * 0.65)
            g = int(self.color[1] * (ratio ** 1.8) * 0.65)
            b = int(self.color[2] * (ratio ** 1.8) * 0.65)
            pygame.draw.line(surf, (r, g, b, 245), (0, row), (self.w, row))
        pygame.draw.rect(surf, (255, 255, 255, 85), (2, 2, self.w - 4, self.h - 4), 3)
        pygame.draw.rect(surf, WHITE, (0, 0, self.w, self.h), 2)
        return surf

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        surface.blit(self.surf, (sx, sy))
        self.draw_attached_ring(surface, sx, sy)


class FloatingSlab(ClassicDarkBlock):
    """Thanh bục mỏng lơ lửng (cao 26px) dùng cho các pha bật nhảy trên không (Hình 11, 15)."""

    def __init__(self, x, y, color=(150, 35, 225), ring_attach=None):
        super().__init__(x, y, color=color, height=26, ring_attach=ring_attach)


class GridBlock(SolidBlock):
    """Khối kẻ lưới 3x3 màu tím/hồng đỏ có viền trắng phát sáng ở mặt tiếp xúc (Hình 12, 13, 14)."""

    def __init__(self, x, y, color=(140, 25, 215), white_edges=None, ring_attach=None):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, ring_attach=ring_attach)
        self.color = color
        self.white_edges = white_edges or []
        self.surf = self._bake()

    def _bake(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        surf.fill((8, 4, 16, 245))
        step = self.w / 3.0
        for i in range(4):
            pos = min(self.w - 1, int(i * step))
            pygame.draw.line(surf, self.color, (pos, 0), (pos, self.h), 2)
            pygame.draw.line(surf, self.color, (0, pos), (self.w, pos), 2)

        if "ALL" in self.white_edges:
            pygame.draw.rect(surf, WHITE, (0, 0, self.w, self.h), 3)
        else:
            if "TOP" in self.white_edges:
                pygame.draw.line(surf, WHITE, (0, 1), (self.w, 1), 3)
            if "BOT" in self.white_edges:
                pygame.draw.line(surf, WHITE, (0, self.h - 2), (self.w, self.h - 2), 3)
            if "LEFT" in self.white_edges:
                pygame.draw.line(surf, WHITE, (1, 0), (1, self.h), 3)
            if "RIGHT" in self.white_edges:
                pygame.draw.line(surf, WHITE, (self.w - 2, 0), (self.w - 2, self.h), 3)
        return surf

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        surface.blit(self.surf, (sx, sy))
        self.draw_attached_ring(surface, sx, sy)