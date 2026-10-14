# entities/base.py
import pygame
from config import *


class GameObject:
    """Lớp cha gốc của mọi đối tượng trong màn chơi."""

    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = int(w)
        self.h = int(h)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def is_visible(self, camera_x):
        return (self.x + self.w >= camera_x - 140) and (self.x <= camera_x + SCREEN_WIDTH + 140)

    def update(self, dt):
        pass

    def draw(self, surface, camera_x):
        raise NotImplementedError


class SolidBlock(GameObject):
    """
    Lớp cơ sở cho mọi khối địa hình rắn (Player có thể đứng lên mặt trên,
    hoặc đứng lộn ngược dưới đáy khi đảo trọng lực, nhưng đâm ngang hông sẽ nổ).
    Khi đổi hình ảnh bên ngoài (Neon, Classic Dark, Grid), logic va chạm vẫn giữ nguyên 100%.
    """

    def __init__(self, x, y, w=TILE_SIZE, h=TILE_SIZE, ring_attach=None):
        super().__init__(x, y, w, h)
        self.ring_attach = ring_attach  # 'DOWN', 'UP', 'RIGHT'

    def draw_attached_ring(self, surface, sx, sy):
        if self.ring_attach == "DOWN":
            cx = sx + self.w // 2
            cy = sy + self.h + 26
            pygame.draw.line(surface, BLACK, (cx, sy + self.h), (cx, cy - 12), 4)
            pygame.draw.circle(surface, WHITE, (cx, cy), 13, 4)
        elif self.ring_attach == "UP":
            cx = sx + self.w // 2
            cy = sy - 26
            pygame.draw.line(surface, BLACK, (cx, sy), (cx, cy + 12), 4)
            pygame.draw.circle(surface, WHITE, (cx, cy), 13, 4)
        elif self.ring_attach == "RIGHT":
            cx = sx + self.w + 46
            cy = sy + self.h // 2
            pygame.draw.line(surface, BLACK, (sx + self.w, cy), (cx - 14, cy), 3)
            pygame.draw.circle(surface, (215, 165, 135), (cx, cy), 14, 5)


class Hazard(GameObject):
    """
    Lớp cơ sở cho mọi chướng ngại vật gây sát thương (Gai đơn, Thảm gai, Cưa máy).
    Mọi lớp kế thừa chỉ cần định nghĩa thuộc tính `hitbox` và hàm `draw`.
    """

    @property
    def hitbox(self):
        return self.rect

    def check_collision(self, player_rect):
        return player_rect.colliderect(self.hitbox)


class Trigger(GameObject):
    """
    Lớp cơ sở cho các vật thể tương tác lực (JumpOrb cần bấm phím, JumpPad tự động bật).
    """

    def __init__(self, x, y, w, h, auto_trigger=False):
        super().__init__(x, y, w, h)
        self.auto_trigger = auto_trigger
        self.activated = False
        self.anim_timer = 0.0

    def reset(self):
        self.activated = False

    def update(self, dt):
        self.anim_timer += dt

    def apply_effect(self, player, particles):
        raise NotImplementedError


class BasePortal(GameObject):
    """
    Lớp cơ sở cho mọi loại Cổng biến đổi (Cổng đổi Chế độ chơi & Cổng đảo Trọng lực).
    """

    def __init__(self, x, y, w=72, h=165):
        super().__init__(x, y, w, h)
        self.triggered = False
        self.timer = 0.0

    def reset(self):
        self.triggered = False

    def update(self, dt):
        self.timer += dt

    def apply_portal_effect(self, player, wave_trail, ship_trail, particles):
        raise NotImplementedError