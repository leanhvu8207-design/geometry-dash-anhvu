# vfx/victory_vfx.py
import math
import random
import pygame
from config import *
from .draw_utils import DrawUtils


class VictoryWallEffect:
    """
    Hiệu ứng Bức tường Phá đảo cuối màn phiên bản đồ họa mịn (High-Definition Smooth Glow):
    - Viền tường phát sáng bằng dải Gradient Alpha 40 lớp mượt mà, không còn vạch trắng cứng
    - Chùm tia sáng (Volumetric Light Rays) đa lớp kèm viền khử răng cưa (Anti-aliased)
    - Hạt ánh sáng nhỏ mịn có hào quang nhẹ
    - Bảng thành tựu màu nâu 'Unlocked new Icon!' trượt êm từ đỉnh màn hình
    """

    def __init__(self, wall_x):
        self.wall_x = float(wall_x)
        self.triggered = False
        self.timer = 0.0
        self.impact_y = GROUND_Y - 120
        self.sparkles = []
        self.font_banner_title = pygame.font.SysFont("arialblack", 32)
        self.font_banner_sub = pygame.font.SysFont("segoeui", 24, bold=True)

        # Tạo sẵn dải Gradient ánh sáng mịn cho mép bức tường để không tốn CPU mỗi khung hình
        self._wall_glow_normal = self._bake_vertical_glow((255, 90, 110), width=48)
        self._wall_glow_active = self._bake_vertical_glow((140, 255, 130), width=84)

        self.beams = [
            (-0.27, 10, 42, (130, 255, 120)),
            (-0.17, 8, 30, (175, 255, 150)),
            (-0.05, 14, 52, (240, 210, 100)),
            (0.01, 18, 64, (165, 255, 140)),
            (0.13, 10, 38, (245, 220, 105)),
            (0.23, 8, 28, (230, 195, 90)),
        ]

    @staticmethod
    def _bake_vertical_glow(color, width):
        surf = pygame.Surface((width, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(width):
            # Độ sáng tăng theo hàm mũ mượt về phía mép phải (nơi tiếp giáp bức tường)
            ratio = (x / float(width)) ** 2.4
            alpha = int(165 * ratio)
            pygame.draw.line(surf, (*color, alpha), (x, 0), (x, SCREEN_HEIGHT))
        # Đường chỉ mảnh 2px ở sát mép tường
        pygame.draw.line(surf, (255, 255, 255, 210), (width - 2, 0), (width - 2, SCREEN_HEIGHT), 2)
        return surf

    def reset(self, wall_x):
        self.wall_x = float(wall_x)
        self.triggered = False
        self.timer = 0.0
        self.sparkles.clear()

    def trigger(self, impact_y):
        if self.triggered:
            return
        self.triggered = True
        self.timer = 0.0
        self.impact_y = impact_y
        # Tạo 80 hạt ánh sáng nhỏ mịn (kích thước chỉ 3px - 7px) kèm vòng glow mềm
        for _ in range(80):
            ang = random.uniform(math.pi * 0.58, math.pi * 1.42)
            spd = random.uniform(150, 760)
            self.sparkles.append(
                {
                    "x": float(SCREEN_WIDTH - 36),
                    "y": float(impact_y + random.uniform(-70, 70)),
                    "vx": math.cos(ang) * spd,
                    "vy": math.sin(ang) * spd + random.uniform(-90, 90),
                    "size": random.uniform(3.0, 6.5),
                    "col": random.choice([(110, 255, 115), (175, 255, 145), (250, 235, 130)]),
                }
            )

    def update(self, dt):
        if not self.triggered:
            return
        self.timer += dt
        for s in self.sparkles:
            s["x"] += s["vx"] * dt
            s["y"] += s["vy"] * dt
            s["vx"] *= 0.986
            s["vy"] *= 0.986

    def draw_wall(self, surface, camera_x):
        sx = int(self.wall_x - camera_x)
        if sx > SCREEN_WIDTH + 80:
            return

        # 1. Vẽ thân bức tường lưới tối màu sắc nét
        wall_w = 54
        for y in range(0, SCREEN_HEIGHT, 36):
            r = pygame.Rect(sx, y, wall_w, 36)
            pygame.draw.rect(surface, (16, 4, 8), r)
            pygame.draw.line(surface, (145, 20, 30), (sx + 18, y), (sx + 18, y + 36), 1)
            pygame.draw.line(surface, (145, 20, 30), (sx + 36, y), (sx + 36, y + 36), 1)
            pygame.draw.line(surface, (145, 20, 30), (sx, y + 18), (sx + wall_w, y + 18), 1)
            pygame.draw.rect(surface, (180, 35, 45), r, 1)

        # 2. Vẽ lớp hào quang Gradient mịn bên trái bức tường (không bị khối trắng cứng)
        glow_surf = self._wall_glow_active if self.triggered else self._wall_glow_normal
        surface.blit(glow_surf, (sx - glow_surf.get_width(), 0), special_flags=pygame.BLEND_RGBA_ADD)

    def draw_victory_overlay(self, surface, camera_x, level_name):
        if not self.triggered:
            return

        sx = min(SCREEN_WIDTH - 24, int(self.wall_x - camera_x))
        cy = int(self.impact_y)

        # 1. Vẽ các chùm tia sáng đa lớp mịn (3 lớp Feathering mỗi chùm tia + biên khử răng cưa)
        ray_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        length = SCREEN_WIDTH + 250
        wave = math.sin(self.timer * 3.8) * 0.02

        for base_angle, start_w, end_w, rgb in self.beams:
            ang = math.pi + base_angle + wave
            dx = math.cos(ang) * length
            dy = math.sin(ang) * length
            nx = -math.sin(ang)
            ny = math.cos(ang)

            # Vẽ 3 lớp từ rộng-mờ đến hẹp-sáng để rìa tia sáng mịn màng
            for scale, alpha in [(1.45, 38), (1.0, 75), (0.55, 115)]:
                sw = start_w * scale
                ew = end_w * scale
                pts = [
                    (sx + nx * sw, cy + ny * sw),
                    (sx - nx * sw, cy - ny * sw),
                    (sx + dx - nx * ew, cy + dy - ny * ew),
                    (sx + dx + nx * ew, cy + dy + ny * ew),
                ]
                pygame.draw.polygon(ray_surf, (*rgb, alpha), pts)
                pygame.draw.aalines(ray_surf, (*rgb, alpha // 2), True, pts)

        surface.blit(ray_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Tâm sáng mịn tại điểm va chạm
        DrawUtils.draw_glow_circle(surface, (180, 255, 160), (sx, cy), 85)

        # 2. Vẽ các hạt ánh sáng nhỏ mịn
        spark_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for s in self.sparkles:
            px, py = int(s["x"]), int(s["y"])
            if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                rad = max(2, int(s["size"]))
                pygame.draw.circle(spark_surf, (*s["col"], 75), (px, py), rad + 3)
                pygame.draw.rect(spark_surf, (*s["col"], 230), (px - rad // 2, py - rad // 2, rad, rad), border_radius=1)
                pygame.draw.rect(spark_surf, (255, 255, 255, 200), (px - rad // 2, py - rad // 2, rad, rad), 1, border_radius=1)
        surface.blit(spark_surf, (0, 0))

        # 3. Bảng thành tựu màu nâu trượt từ trên xuống
        slide_t = min(1.0, self.timer * 3.8)
        # Nội suy mượt (Ease-Out Cubic)
        ease_t = 1.0 - ((1.0 - slide_t) ** 3)
        banner_w, banner_h = 720, 132
        banner_x = (SCREEN_WIDTH - banner_w) // 2
        banner_y = int(-150 + 162 * ease_t)

        banner_rect = pygame.Rect(banner_x, banner_y, banner_w, banner_h)
        pygame.draw.rect(surface, WHITE, banner_rect.inflate(8, 8), border_radius=16)
        pygame.draw.rect(surface, BLACK, banner_rect.inflate(4, 4), border_radius=15)
        pygame.draw.rect(surface, (172, 104, 52), banner_rect, border_radius=13)
        pygame.draw.rect(surface, (195, 122, 66), banner_rect.inflate(-8, -8), 3, border_radius=11)

        # Icon Robot màu xám bạc bên trái bảng
        ic_x = banner_x + 56
        ic_y = banner_y + 28
        head_r = pygame.Rect(ic_x, ic_y, 66, 52)
        pygame.draw.rect(surface, BLACK, head_r.inflate(4, 4), border_radius=4)
        pygame.draw.rect(surface, (185, 190, 198), head_r, border_radius=3)
        pygame.draw.rect(surface, BLACK, (ic_x + 12, ic_y + 11, 14, 14))
        pygame.draw.rect(surface, WHITE, (ic_x + 15, ic_y + 14, 8, 8))
        pygame.draw.rect(surface, BLACK, (ic_x + 40, ic_y + 11, 14, 14))
        pygame.draw.rect(surface, WHITE, (ic_x + 43, ic_y + 14, 8, 8))
        pygame.draw.rect(surface, BLACK, (ic_x + 12, ic_y + 34, 10, 14))
        pygame.draw.rect(surface, BLACK, (ic_x + 44, ic_y + 34, 10, 14))

        base_r = pygame.Rect(ic_x, ic_y + 60, 66, 12)
        pygame.draw.rect(surface, BLACK, base_r.inflate(4, 4), border_radius=3)
        pygame.draw.rect(surface, (185, 190, 198), base_r, border_radius=2)

        DrawUtils.draw_outlined_text(
            surface,
            f"{level_name}!",
            self.font_banner_title,
            (banner_x + 165, banner_y + 40),
            WHITE,
            BLACK,
            4,
            center=False,
        )
        sub_surf = self.font_banner_sub.render("Unlocked new Icon!", True, WHITE)
        surface.blit(sub_surf, (banner_x + 165, banner_y + 72))