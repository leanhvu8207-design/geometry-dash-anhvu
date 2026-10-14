# entities/portals.py
import math
import pygame
from config import *
from vfx import DrawUtils
from .base import BasePortal


class ModePortal(BasePortal):
    """
    Cổng chuyển đổi Chế độ chơi thực sự (Cube / Ship / Wave).
    Hỗ trợ kiểu cổng 3D ống trụ kẻ sọc phát sáng (Hình mẫu 15, 19).
    """

    def __init__(self, x, y, target_mode=MODE_SHIP, style_3d=False):
        super().__init__(x, y, 74, 170)
        self.target_mode = target_mode
        self.style_3d = style_3d

    def apply_portal_effect(self, player, wave_trail, ship_trail, particles):
        self.triggered = True
        player.set_mode(self.target_mode, wave_trail, ship_trail)
        particles.spawn_explosion(player.x + player.w // 2, player.y + player.h // 2, CYAN_LIGHT, count=28)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        cx, cy = sx + self.w // 2, sy + self.h // 2

        # Chọn màu đặc trưng theo chế độ đích để người chơi dễ nhận biết
        if self.target_mode == MODE_SHIP:
            main_col = (255, 70, 215)   # Hồng tím: Cổng biến thành Máy bay
        elif self.target_mode == MODE_WAVE:
            main_col = CYAN_LIGHT       # Xanh Cyan: Cổng biến thành Tên lửa Wave
        else:
            main_col = (70, 255, 95)    # Xanh lá / Cam: Cổng biến về Khối vuông Cube

        if self.style_3d:
            barrel_w = 34
            back_rect = pygame.Rect(sx + barrel_w, sy + 6, self.w - 20, self.h - 12)
            pygame.draw.ellipse(surface, BLACK, back_rect)
            for row_y in range(sy + 18, sy + self.h - 16, 18):
                pygame.draw.line(surface, (190, 25, 45), (sx + 24, row_y), (sx + self.w - 10, row_y), 5)
            pygame.draw.ellipse(surface, BLACK, back_rect, 6)

            front_rect = pygame.Rect(sx, sy, self.w - 22, self.h)
            DrawUtils.draw_glow_circle(surface, main_col, (front_rect.centerx, cy), 58)
            pygame.draw.ellipse(surface, main_col, front_rect, 8)
            pygame.draw.ellipse(surface, WHITE, front_rect.inflate(-6, -6), 3)

            for i in range(5):
                ang = self.timer * 2.6 + i * 1.25
                px = front_rect.centerx + int(math.cos(ang) * 30)
                py = cy + int(math.sin(ang * 1.3) * 65)
                pygame.draw.rect(surface, main_col, (px - 3, py - 3, 6, 6))
        else:
            DrawUtils.draw_glow_circle(surface, main_col, (cx, cy), 56)
            rect_outer = pygame.Rect(sx, sy, self.w - 14, self.h)
            rect_inner = pygame.Rect(sx + 10, sy + 16, self.w - 34, self.h - 32)
            pygame.draw.ellipse(surface, main_col, rect_outer, 6)
            pygame.draw.ellipse(surface, WHITE, rect_inner, 3)


class GravityPortal(BasePortal):
    """
    Cổng Đảo Ngược Trọng Lực:
    - target_gravity = -1 (Cổng Xanh Lam): Hút nhân vật bay lên chạy lộn ngược trên trần!
    - target_gravity = +1 (Cổng Vàng Kim): Đưa trọng lực trở lại mặt đất bình thường!
    """

    def __init__(self, x, y, target_gravity=-1):
        super().__init__(x, y, 66, 160)
        self.target_gravity = target_gravity

    def apply_portal_effect(self, player, wave_trail, ship_trail, particles):
        self.triggered = True
        if player.gravity_dir != self.target_gravity:
            player.gravity_dir = self.target_gravity
            player.vel_y = 260.0 * self.target_gravity
            player.on_ground = False
        col = (40, 180, 255) if self.target_gravity < 0 else GOLD_YELLOW
        particles.spawn_explosion(player.x + player.w // 2, player.y + player.h // 2, col, count=26)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        cx, cy = sx + self.w // 2, sy + self.h // 2

        col = (30, 175, 255) if self.target_gravity < 0 else GOLD_YELLOW
        DrawUtils.draw_glow_circle(surface, col, (cx, cy), 52)

        outer = pygame.Rect(sx, sy, self.w, self.h)
        inner = pygame.Rect(sx + 10, sy + 16, self.w - 20, self.h - 32)
        pygame.draw.ellipse(surface, col, outer, 6)
        pygame.draw.ellipse(surface, WHITE, inner, 3)

        # Vẽ mũi tên chỉ hướng trọng lực (Lên trần hoặc Xuống đất) ở giữa cổng
        dir_y = -1 if self.target_gravity < 0 else 1
        arrow_pts = [
            (cx, cy + dir_y * 22),
            (cx - 14, cy - dir_y * 8),
            (cx + 14, cy - dir_y * 8),
        ]
        pygame.draw.polygon(surface, WHITE, arrow_pts)