# entities/triggers.py
import math
import pygame
from config import *
from vfx import DrawUtils
from .base import Trigger


class JumpOrb(Trigger):
    """
    Vòng tròn tương tác trên không (Yêu cầu bấm phím để bật):
    - orb_type: 'PURPLE_RING', 'CYAN_ORB', 'GREEN_POST_RING', 'YELLOW_ORB'
    """

    def __init__(self, x, y, orb_type="PURPLE_RING", post_height=0, boost_scale=1.0):
        super().__init__(x - 24, y - 24, 48, 48, auto_trigger=False)
        self.orb_type = orb_type
        self.post_height = post_height
        self.boost_scale = boost_scale

    def apply_effect(self, player, particles):
        self.activated = True
        player.vel_y = ORB_JUMP_VEL * self.boost_scale * player.gravity_dir
        player.on_ground = False
        particles.spawn_explosion(self.x + 24, self.y + 24, CYAN_LIGHT, count=18)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        cx = int(self.x - camera_x + self.w // 2)
        cy = int(self.y + self.h // 2)
        pulse = math.sin(self.anim_timer * 7.0) * 2.5

        if self.post_height > 0:
            pygame.draw.line(surface, BLACK, (cx, cy + 14), (cx, cy + self.post_height), 4)
            pygame.draw.rect(surface, BLACK, (cx - 7, cy + self.post_height - 4, 14, 5))

        if self.orb_type == "PURPLE_RING":
            DrawUtils.draw_glow_circle(surface, (180, 30, 255), (cx, cy), int(20 + pulse))
            pygame.draw.circle(surface, (165, 20, 245), (cx, cy), int(16 + pulse * 0.5), 5)
            pygame.draw.circle(surface, (230, 140, 255), (cx, cy), int(16 + pulse * 0.5), 2)
        elif self.orb_type == "GREEN_POST_RING":
            DrawUtils.draw_glow_circle(surface, (90, 255, 90), (cx, cy), int(22 + pulse))
            pygame.draw.circle(surface, WHITE, (cx, cy), 16, 5)
            pygame.draw.circle(surface, (80, 255, 90), (cx, cy), 12, 4)
        elif self.orb_type == "YELLOW_ORB":
            DrawUtils.draw_glow_circle(surface, GOLD_YELLOW, (cx, cy), int(22 + pulse))
            pygame.draw.circle(surface, WHITE, (cx, cy), 17)
            pygame.draw.circle(surface, GOLD_YELLOW, (cx, cy), 13)
        else:  # CYAN_ORB
            DrawUtils.draw_glow_circle(surface, CYAN_LIGHT, (cx, cy), int(26 + pulse))
            pygame.draw.circle(surface, (140, 40, 235), (cx, cy), 23, 3)
            for i in range(4):
                ang = self.anim_timer * 3.2 + i * (math.pi / 2)
                ox = cx + int(math.cos(ang) * 24)
                oy = cy + int(math.sin(ang) * 24)
                pygame.draw.circle(surface, (165, 50, 255), (ox, oy), 5)
            pygame.draw.circle(surface, WHITE, (cx, cy), 18)
            pygame.draw.circle(surface, CYAN_LIGHT, (cx, cy), 14)


class JumpPad(Trigger):
    """
    Đệm lò xo phát sáng đặt trên mặt đất hoặc mặt bục (auto_trigger=True):
    Khi nhân vật chạm vào sẽ tự động bật vọt lên cao mà không cần bấm phím!
    """

    def __init__(self, x, y_bottom, pad_color=GOLD_YELLOW, boost_scale=1.0):
        super().__init__(x + 4, y_bottom - 14, TILE_SIZE - 8, 14, auto_trigger=True)
        self.pad_color = pad_color
        self.boost_scale = boost_scale

    def apply_effect(self, player, particles):
        self.activated = True
        player.vel_y = PAD_JUMP_VEL * self.boost_scale * player.gravity_dir
        player.on_ground = False
        particles.spawn_explosion(self.x + self.w // 2, self.y, self.pad_color, count=22)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx, sy = int(self.x - camera_x), int(self.y)
        cx = sx + self.w // 2
        DrawUtils.draw_glow_circle(surface, self.pad_color, (cx, sy + 6), 20)
        pts = [(sx, sy + self.h), (sx + 8, sy), (sx + self.w - 8, sy), (sx + self.w, sy + self.h)]
        pygame.draw.polygon(surface, self.pad_color, pts)
        pygame.draw.polygon(surface, WHITE, pts, 2)