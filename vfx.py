# vfx.py
import math
import random
import pygame
from config import *


class DrawUtils:
    """Bộ công cụ vẽ hiệu ứng Neon Glow, Gradient và Chữ có viền chuẩn Geometry Dash."""

    @staticmethod
    def draw_glow_circle(surface, color, center, radius, glow_layers=4):
        """Vẽ hình tròn phát sáng nhiều lớp alpha."""
        max_r = int(radius * 1.8)
        glow_surf = pygame.Surface((max_r * 2, max_r * 2), pygame.SRCALPHA)
        for i in range(glow_layers, 0, -1):
            r = int(radius + (max_r - radius) * (i / glow_layers))
            alpha = int(85 * (1 - (i / (glow_layers + 1))))
            pygame.draw.circle(glow_surf, (*color, alpha), (max_r, max_r), r)
        surface.blit(glow_surf, (int(center[0] - max_r), int(center[1] - max_r)), special_flags=pygame.BLEND_RGBA_ADD)

    @staticmethod
    def draw_glow_line(surface, color, start_pos, end_pos, width=4, glow_width=14):
        """Vẽ đường thẳng phát sáng Neon (dùng cho hành lang Wave và vệt sáng)."""
        # Lớp hào quang bên ngoài
        glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, (*color, 70), start_pos, end_pos, glow_width)
        pygame.draw.line(glow_surf, (*color, 140), start_pos, end_pos, glow_width // 2)
        surface.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        # Lõi trắng sáng ở giữa
        pygame.draw.line(surface, color, start_pos, end_pos, width + 2)
        pygame.draw.line(surface, WHITE, start_pos, end_pos, max(2, width - 2))

    @staticmethod
    def draw_outlined_text(surface, text, font, pos, text_color, outline_color=BLACK, outline_width=3, center=True):
        """Vẽ chữ có viền đen dày và bóng đổ giống hệt font Pusab của Geometry Dash."""
        base = font.render(text, True, text_color)
        outline = font.render(text, True, outline_color)
        w, h = base.get_size()
        target_x = pos[0] - w // 2 if center else pos[0]
        target_y = pos[1] - h // 2 if center else pos[1]

        # Vẽ bóng đổ phía dưới
        surface.blit(outline, (target_x + outline_width, target_y + outline_width + 2))

        # Vẽ viền xung quanh
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width + 1:
                    surface.blit(outline, (target_x + dx, target_y + dy))

        # Vẽ chữ chính
        surface.blit(base, (target_x, target_y))


class Particle:
    """Hạt hiệu ứng (bụi khi trượt trên đất, tia sáng ở cổng, mảnh vỡ khi nổ)."""

    def __init__(self, x, y, vx, vy, size, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        self.size = max(0.0, self.size - 8.0 * dt)

    def draw(self, surface, camera_x):
        if self.lifetime <= 0 or self.size <= 1:
            return
        screen_x = self.x - camera_x
        if -20 <= screen_x <= SCREEN_WIDTH + 20:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            s = int(self.size)
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            surf.fill((*self.color, max(0, min(255, alpha))))
            surface.blit(surf, (int(screen_x - s // 2), int(self.y - s // 2)))


class ParticleSystem:
    """Quản lý toàn bộ các hạt hiệu ứng trong màn chơi."""

    def __init__(self):
        self.particles = []

    def clear(self):
        self.particles.clear()

    def spawn_trail(self, x, y, color):
        """Tạo hạt bụi vuông nhỏ phía sau Cube khi tiếp đất."""
        vx = random.uniform(-60, -10)
        vy = random.uniform(-90, -20)
        size = random.uniform(6, 11)
        self.particles.append(Particle(x, y, vx, vy, size, color, random.uniform(0.25, 0.45)))

    def spawn_explosion(self, x, y, color, count=35):
        """Tạo vụ nổ hạt khi nhân vật va vào gai hoặc tường."""
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(80, 480)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(7, 16)
            self.particles.append(Particle(x, y, vx, vy, size, color, random.uniform(0.4, 0.8)))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0 and p.size > 1]

    def draw(self, surface, camera_x):
        for p in self.particles:
            p.draw(surface, camera_x)


class WaveTrail:
    """Vệt sáng zíc-zắc màu hồng phát sáng nối liền phía sau nhân vật ở chế độ Wave."""

    def __init__(self):
        self.points = []  # Danh sách các tọa độ (world_x, world_y)

    def clear(self):
        self.points.clear()

    def add_point(self, x, y):
        self.points.append((x, y))
        # Giới hạn số điểm để tối ưu bộ nhớ
        if len(self.points) > 160:
            self.points.pop(0)

    def draw(self, surface, camera_x):
        if len(self.points) < 2:
            return
        screen_pts = [(int(px - camera_x), int(py)) for px, py in self.points if px - camera_x > -100]
        if len(screen_pts) < 2:
            return

        # Vẽ lớp Glow hồng tím bên ngoài
        glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(glow_surf, (*WAVE_TRAIL_PINK, 95), False, screen_pts, 18)
        pygame.draw.lines(glow_surf, (*WAVE_TRAIL_PINK, 180), False, screen_pts, 10)
        surface.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Vẽ lõi trắng hồng sắc nét ở giữa
        pygame.draw.lines(surface, WAVE_TRAIL_PINK, False, screen_pts, 6)
        pygame.draw.lines(surface, WHITE, False, screen_pts, 3)


class ParallaxBackground:
    """Quản lý nền ô vuông Tiled và mặt đất, tự động đổi màu giữa Menu, Cube và Wave."""

    def __init__(self):
        self.scroll_x = 0.0
        self.bg_color = list(MENU_BG_BLUE)
        self.target_bg_color = list(MENU_BG_BLUE)

    def set_theme(self, mode):
        if mode == STATE_MENU:
            self.target_bg_color = list(MENU_BG_BLUE)
        elif mode == MODE_CUBE:
            self.target_bg_color = list(CUBE_BG_COLOR)
        elif mode == MODE_WAVE:
            self.target_bg_color = list(WAVE_BG_COLOR)

    def update(self, dt, speed=SCROLL_SPEED):
        self.scroll_x += speed * 0.25 * dt
        # Chuyển màu mượt mà (Color Lerp) khi qua cổng Portal
        for i in range(3):
            self.bg_color[i] += (self.target_bg_color[i] - self.bg_color[i]) * min(1.0, dt * 5.0)

    def draw(self, surface, camera_x, mode=STATE_MENU, draw_ground=True):
        cur_bg = tuple(int(c) for c in self.bg_color)
        surface.fill(cur_bg)

        # Màu ô lưới nhạt/đậm hơn màu nền một chút
        grid_color = tuple(max(0, min(255, int(c * 1.35) + 8)) for c in self.bg_color)
        border_color = tuple(max(0, min(255, int(c * 0.75))) for c in self.bg_color)

        # Vẽ các khối vuông lớn trang trí nền giống bản gốc
        box_size = 160
        offset_x = int(self.scroll_x) % box_size
        for x in range(-offset_x, SCREEN_WIDTH + box_size, box_size):
            for y in range(20, GROUND_Y, box_size):
                rect = pygame.Rect(x + 8, y + 8, box_size - 16, box_size - 16)
                pygame.draw.rect(surface, grid_color, rect)
                pygame.draw.rect(surface, border_color, rect, 3)

        if not draw_ground:
            return

        # Vẽ mặt đất (Ground)
        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        if mode == STATE_MENU:
            pygame.draw.rect(surface, MENU_GROUND_BLUE, ground_rect)
            g_tile = 120
            g_off = int(camera_x) % g_tile
            for x in range(-g_off, SCREEN_WIDTH + g_tile, g_tile):
                r = pygame.Rect(x + 4, GROUND_Y + 6, g_tile - 8, SCREEN_HEIGHT - GROUND_Y - 12)
                pygame.draw.rect(surface, (0, 28, 85), r, 3)
            # Đường kẻ ngang màu trắng sáng phân cách mặt đất
            pygame.draw.line(surface, WHITE, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        else:
            # Mặt đất trong màn chơi có viền răng cưa cam/hồng phát sáng giống hình mẫu 3
            pygame.draw.rect(surface, (8, 2, 20), ground_rect)
            tooth_w = 24
            g_off = int(camera_x) % tooth_w
            for x in range(-g_off, SCREEN_WIDTH + tooth_w, tooth_w):
                pygame.draw.rect(surface, (255, 110, 60), (x, GROUND_Y, tooth_w // 2, 7))
            pygame.draw.line(surface, (255, 60, 140), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)