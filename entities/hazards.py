# entities/hazards.py
import math
import pygame
from config import *
from vfx import DrawUtils
from .base import Hazard


class Spike(Hazard):
    """
    Gai nhọn đơn lẻ (Hỗ trợ 4 hướng 'UP', 'DOWN', 'LEFT', 'RIGHT' và kích thước nhỏ/lớn):
    - style='CLASSIC_BLACK': Gai đen viền trắng phát sáng (Map 2)
    - style='BLUE' / 'WHITE_STAR': Gai Neon xanh dương hoặc gai trắng có sao ở mũi (Map 1)
    """

    def __init__(self, x, y, direction="UP", style="CLASSIC_BLACK", scale=1.0):
        size = int(TILE_SIZE * scale)
        super().__init__(x, y, size, size)
        self.direction = direction
        self.style = style

    @property
    def hitbox(self):
        pad_x = int(self.w * 0.28)
        pad_y = int(self.h * 0.26)
        return pygame.Rect(
            int(self.x + pad_x),
            int(self.y + pad_y),
            max(8, self.w - pad_x * 2),
            max(8, self.h - pad_y * 2),
        )

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        w, h = self.w, self.h

        if self.direction == "UP":
            pts = [(sx, sy + h), (sx + w // 2, sy + 3), (sx + w, sy + h)]
            tip = (sx + w // 2, sy + 2)
        elif self.direction == "DOWN":
            pts = [(sx, sy), (sx + w // 2, sy + h - 3), (sx + w, sy)]
            tip = (sx + w // 2, sy + h - 2)
        elif self.direction == "LEFT":
            pts = [(sx + w, sy + 5), (sx + 5, sy + h // 2), (sx + w, sy + h - 5)]
            tip = (sx + 4, sy + h // 2)
        else:
            pts = [(sx, sy + 5), (sx + w - 5, sy + h // 2), (sx, sy + h - 5)]
            tip = (sx + w - 4, sy + h // 2)

        if self.style == "CLASSIC_BLACK":
            pygame.draw.polygon(surface, (205, 215, 235), pts, 4)
            pygame.draw.polygon(surface, BLACK, pts)
            pygame.draw.polygon(surface, WHITE, pts, 2)
        elif self.style == "WHITE_STAR":
            pygame.draw.polygon(surface, (235, 240, 255), pts)
            pygame.draw.polygon(surface, (160, 175, 210), pts, 2)
            tx, ty = tip
            pygame.draw.line(surface, WHITE, (tx - 5, ty), (tx + 5, ty), 2)
            pygame.draw.line(surface, WHITE, (tx, ty - 5), (tx, ty + 5), 2)
        else:
            pygame.draw.polygon(surface, (10, 165, 255), pts)
            pygame.draw.polygon(surface, (80, 220, 255), pts, 2)


class SpikeStrip(Hazard):
    """
    Thảm gai nhọn trải dài dưới hố sâu (Hình mẫu 11, 15, 17).
    Hitbox bao phủ toàn bộ chiều ngang (width) của thảm gai, khắc phục triệt để lỗi đi xuyên gai!
    """

    def __init__(self, x, width, y_bottom=GROUND_Y):
        height = 46
        super().__init__(x, y_bottom - height, width, height)
        self.y_bottom = y_bottom

    @property
    def hitbox(self):
        # Phủ kín từ đầu thảm gai đến cuối thảm gai (chỉ trừ 6px mép ngoài cùng)
        return pygame.Rect(int(self.x + 6), int(self.y_bottom - 34), max(12, self.w - 12), 34)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx = int(self.x - camera_x)
        end_x = sx + self.w
        by = int(self.y_bottom)

        cur_x = sx
        idx = 0
        while cur_x < end_x - 10:
            if idx % 6 == 1:
                pts = [(cur_x, by), (cur_x + 14, by - 48), (cur_x + 28, by)]
                pygame.draw.polygon(surface, (235, 245, 225), pts)
                pygame.draw.polygon(surface, WHITE, pts, 2)
            elif idx % 4 == 2:
                pts = [(cur_x, by), (cur_x + 12, by - 35), (cur_x + 24, by)]
                pygame.draw.polygon(surface, (210, 220, 195), pts)

            b_pts = [(cur_x, by), (cur_x + 10, by - 24), (cur_x + 20, by)]
            pygame.draw.polygon(surface, BLACK, b_pts)
            pygame.draw.polygon(surface, (80, 40, 110), b_pts, 1)
            cur_x += 18
            idx += 1


class Sawblade(Hazard):
    """Bánh răng cưa xoay tròn tốc độ cao dùng trong phân đoạn nâng cao của Map 2."""

    def __init__(self, cx, cy, radius=42, color=(220, 35, 95)):
        super().__init__(cx - radius, cy - radius, radius * 2, radius * 2)
        self.cx = float(cx)
        self.cy = float(cy)
        self.radius = int(radius)
        self.color = color
        self.angle = 0.0

    @property
    def hitbox(self):
        r = int(self.radius * 0.72)
        return pygame.Rect(int(self.cx - r), int(self.cy - r), r * 2, r * 2)

    def update(self, dt):
        self.angle = (self.angle + 260.0 * dt) % 360.0

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx = int(self.cx - camera_x)
        sy = int(self.cy)

        DrawUtils.draw_glow_circle(surface, self.color, (sx, sy), self.radius)

        # Vẽ 12 răng cưa xoay
        teeth = 12
        pts = []
        base_rad = math.radians(self.angle)
        for i in range(teeth * 2):
            ang = base_rad + i * (math.pi / teeth)
            r = self.radius if i % 2 == 0 else int(self.radius * 0.74)
            pts.append((sx + math.cos(ang) * r, sy + math.sin(ang) * r))

        pygame.draw.polygon(surface, BLACK, pts)
        pygame.draw.polygon(surface, WHITE, pts, 2)
        pygame.draw.circle(surface, self.color, (sx, sy), int(self.radius * 0.48))
        pygame.draw.circle(surface, WHITE, (sx, sy), int(self.radius * 0.22))


class WaveCorridor(Hazard):
    """Hành lang zíc-zắc chế độ Wave."""

    def __init__(self, start_x, end_x, top_vertices, bottom_vertices, guide_dots):
        super().__init__(start_x, 0, end_x - start_x, SCREEN_HEIGHT)
        self.start_x = start_x
        self.end_x = end_x
        self.top_vertices = top_vertices
        self.bottom_vertices = bottom_vertices
        self.guide_dots = guide_dots

    def check_collision(self, player_rect):
        px = player_rect.centerx
        if px < self.start_x or px > self.end_x:
            return False

        top_y = 0
        for i in range(len(self.top_vertices) - 1):
            x1, y1 = self.top_vertices[i]
            x2, y2 = self.top_vertices[i + 1]
            if x1 <= px <= x2:
                t = (px - x1) / max(1.0, (x2 - x1))
                top_y = y1 + t * (y2 - y1)
                break

        bot_y = SCREEN_HEIGHT
        for i in range(len(self.bottom_vertices) - 1):
            x1, y1 = self.bottom_vertices[i]
            x2, y2 = self.bottom_vertices[i + 1]
            if x1 <= px <= x2:
                t = (px - x1) / max(1.0, (x2 - x1))
                bot_y = y1 + t * (y2 - y1)
                break

        return (player_rect.top + 6 <= top_y) or (player_rect.bottom - 6 >= bot_y)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        vis_top = [(int(x - camera_x), int(y)) for x, y in self.top_vertices if -250 <= x - camera_x <= SCREEN_WIDTH + 250]
        vis_bot = [(int(x - camera_x), int(y)) for x, y in self.bottom_vertices if -250 <= x - camera_x <= SCREEN_WIDTH + 250]
        if len(vis_top) < 2 or len(vis_bot) < 2:
            return

        top_poly = [(vis_top[0][0], 0)] + vis_top + [(vis_top[-1][0], 0)]
        bot_poly = [(vis_bot[0][0], SCREEN_HEIGHT)] + vis_bot + [(vis_bot[-1][0], SCREEN_HEIGHT)]

        wall_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(wall_surf, (68, 10, 95, 255), top_poly)
        pygame.draw.polygon(wall_surf, (68, 10, 95, 255), bot_poly)

        brick_off_x = int(camera_x) % 64
        for y in range(0, SCREEN_HEIGHT, 32):
            pygame.draw.line(wall_surf, (30, 3, 45, 255), (0, y), (SCREEN_WIDTH, y), 3)
            row_shift = 32 if (y // 32) % 2 == 1 else 0
            for x in range(-brick_off_x + row_shift, SCREEN_WIDTH, 64):
                pygame.draw.line(wall_surf, (30, 3, 45, 255), (x, y), (x, y + 32), 3)

        corridor_poly = vis_top + list(reversed(vis_bot))
        pygame.draw.polygon(wall_surf, (0, 0, 0, 0), corridor_poly)
        surface.blit(wall_surf, (0, 0))

        for gx, gy in self.guide_dots:
            sx = int(gx - camera_x)
            if -30 <= sx <= SCREEN_WIDTH + 30:
                DrawUtils.draw_glow_circle(surface, (255, 20, 140), (sx, int(gy)), 13)
                pygame.draw.circle(surface, (255, 45, 160), (sx, int(gy)), 9)

        glow_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_RED, 80), False, vis_top, 20)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_ORANGE, 150), False, vis_top, 10)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_RED, 80), False, vis_bot, 20)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_ORANGE, 150), False, vis_bot, 10)
        surface.blit(glow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        pygame.draw.lines(surface, WAVE_NEON_ORANGE, False, vis_top, 5)
        pygame.draw.lines(surface, (255, 240, 150), False, vis_top, 2)
        pygame.draw.lines(surface, WAVE_NEON_ORANGE, False, vis_bot, 5)
        pygame.draw.lines(surface, (255, 240, 150), False, vis_bot, 2)