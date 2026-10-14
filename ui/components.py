# ui/components.py
import math
import pygame
from config import *


class AudioSlider:
    """Thanh trượt âm lượng tương tác kéo-thả mượt mà cho Nhạc nền (♪) và Hiệu ứng (Loa)."""

    def __init__(self, x, y, width, height, icon_type="music", initial_val=0.92):
        self.rect = pygame.Rect(x, y, width, height)
        self.icon_type = icon_type
        self.value = max(0.0, min(1.0, float(initial_val)))
        self.dragging = False
        self.knob_radius = 19

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            knob_x = self.rect.x + int(self.value * self.rect.w)
            knob_y = self.rect.centery
            if math.hypot(mx - knob_x, my - knob_y) <= self.knob_radius + 6 or self.rect.inflate(10, 16).collidepoint(mx, my):
                self.dragging = True
                self._update_val(mx)
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val(event.pos[0])
            return True
        return False

    def _update_val(self, mouse_x):
        rel = (mouse_x - self.rect.x) / float(self.rect.w)
        self.value = max(0.0, min(1.0, rel))

    def draw(self, surface):
        ix = self.rect.x - 42
        iy = self.rect.centery
        if self.icon_type == "music":
            pygame.draw.circle(surface, WHITE, (ix - 6, iy + 8), 6)
            pygame.draw.circle(surface, WHITE, (ix + 10, iy + 6), 6)
            pygame.draw.line(surface, WHITE, (ix - 2, iy + 8), (ix - 2, iy - 12), 4)
            pygame.draw.line(surface, WHITE, (ix + 14, iy + 6), (ix + 14, iy - 14), 4)
            pygame.draw.line(surface, WHITE, (ix - 2, iy - 11), (ix + 14, iy - 13), 5)
        else:
            pts = [(ix - 12, iy - 5), (ix - 4, iy - 5), (ix + 5, iy - 13), (ix + 5, iy + 13), (ix - 4, iy + 5), (ix - 12, iy + 5)]
            pygame.draw.polygon(surface, WHITE, pts)
            pygame.draw.arc(surface, WHITE, (ix + 2, iy - 9, 12, 18), -math.pi / 3, math.pi / 3, 2)
            pygame.draw.arc(surface, WHITE, (ix + 5, iy - 14, 16, 28), -math.pi / 3, math.pi / 3, 2)

        pygame.draw.rect(surface, (15, 25, 45), self.rect, border_radius=8)

        fill_w = int(self.rect.w * self.value)
        if fill_w > 6:
            fill_surf = pygame.Surface((fill_w, self.rect.h), pygame.SRCALPHA)
            pygame.draw.rect(fill_surf, (0, 175, 240), (0, 0, fill_w, self.rect.h), border_radius=7)
            for sx in range(-20, fill_w + 20, 18):
                pygame.draw.line(fill_surf, (60, 225, 255), (sx, self.rect.h), (sx + 12, 0), 5)
            surface.blit(fill_surf, self.rect.topleft)

        pygame.draw.rect(surface, (215, 175, 35), self.rect, 3, border_radius=8)

        knob_x = self.rect.x + fill_w
        knob_y = self.rect.centery
        pygame.draw.circle(surface, BLACK, (knob_x, knob_y), self.knob_radius + 2)
        pygame.draw.circle(surface, (230, 190, 45), (knob_x, knob_y), self.knob_radius)
        pygame.draw.circle(surface, (165, 130, 20), (knob_x, knob_y), self.knob_radius - 4)
        pygame.draw.circle(surface, (245, 215, 90), (knob_x - 3, knob_y - 3), 4)


class CircleIconButton:
    """Nút bấm hình tròn màu xanh lá 3D dùng trong bảng Pause & Victory."""

    def __init__(self, center, radius, icon_type="PLAY"):
        self.center = center
        self.radius = radius
        self.icon_type = icon_type

    def is_hovered(self, mouse_pos):
        return math.hypot(mouse_pos[0] - self.center[0], mouse_pos[1] - self.center[1]) <= self.radius

    def draw(self, surface, mouse_pos):
        hover = self.is_hovered(mouse_pos)
        r = int(self.radius * (1.06 if hover else 1.0))
        cx, cy = self.center

        pygame.draw.circle(surface, BLACK, (cx, cy + 3), r + 6)
        pygame.draw.circle(surface, WHITE, (cx, cy), r + 4)
        pygame.draw.circle(surface, BLACK, (cx, cy), r)
        pygame.draw.circle(surface, LOGO_GREEN_BOT, (cx, cy), r - 4)

        hi_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(hi_surf, (*LOGO_GREEN_TOP, 210), (10, 6, (r - 5) * 2, int(r * 1.15)))
        surface.blit(hi_surf, (cx - r, cy - r))

        if self.icon_type == "REPLAY":
            arc_rect = pygame.Rect(cx - 28, cy - 28, 56, 56)
            pygame.draw.arc(surface, BLACK, arc_rect.inflate(6, 6), 0.4, math.tau - 0.5, 15)
            pygame.draw.arc(surface, CYAN_LIGHT, arc_rect, 0.4, math.tau - 0.5, 11)
            arrow_pts = [(cx + 12, cy - 2), (cx + 34, cy - 8), (cx + 26, cy + 16)]
            pygame.draw.polygon(surface, BLACK, [(p[0] + 2, p[1] + 2) for p in arrow_pts])
            pygame.draw.polygon(surface, CYAN_LIGHT, arrow_pts)

        elif self.icon_type == "PLAY":
            tri_pts = [(cx - 24, cy - 38), (cx - 24, cy + 38), (cx + 42, cy)]
            pygame.draw.polygon(surface, BLACK, [(p[0] + 3, p[1] + 3) for p in tri_pts])
            pygame.draw.polygon(surface, GOLD_YELLOW, tri_pts)
            pygame.draw.polygon(surface, BLACK, tri_pts, 4)

        elif self.icon_type == "MENU":
            for offset_y in [-18, 0, 18]:
                y_pos = cy + offset_y
                pygame.draw.circle(surface, BLACK, (cx - 24, y_pos), 8)
                pygame.draw.circle(surface, CYAN_LIGHT, (cx - 24, y_pos), 6)
                bar_r = pygame.Rect(cx - 10, y_pos - 6, 40, 12)
                pygame.draw.rect(surface, BLACK, bar_r.inflate(4, 4), border_radius=4)
                pygame.draw.rect(surface, CYAN_LIGHT, bar_r, border_radius=3)