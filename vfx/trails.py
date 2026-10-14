# vfx/trails.py
import pygame
from config import *


class BaseTrail:
    """Lớp cơ sở (Base Class) cho mọi vệt sáng nối đuôi nhân vật."""

    def __init__(self, max_points=100):
        self.points = []
        self.max_points = max_points

    def clear(self):
        self.points.clear()

    def add_point(self, x, y):
        self.points.append((float(x), float(y)))
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def get_screen_points(self, camera_x):
        return [(int(px - camera_x), int(py)) for px, py in self.points if px - camera_x > -100]

    def draw(self, surface, camera_x):
        pass


class WaveTrail(BaseTrail):
    """Vệt sáng laser hồng-trắng mượt mà của chế độ Wave."""

    def __init__(self):
        super().__init__(max_points=150)

    def draw(self, surface, camera_x):
        pts = self.get_screen_points(camera_x)
        if len(pts) < 2:
            return

        glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(glow_surf, (*WAVE_TRAIL_PINK, 65), False, pts, 14)
        pygame.draw.lines(glow_surf, (*WAVE_TRAIL_PINK, 140), False, pts, 8)
        surface.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        pygame.draw.lines(surface, WAVE_TRAIL_PINK, False, pts, 4)
        pygame.draw.lines(surface, WHITE, False, pts, 2)


class ShipFlameTrail(BaseTrail):
    """Vệt lửa phản lực uốn lượn mềm mại phía sau đuôi máy bay."""

    def __init__(self):
        super().__init__(max_points=45)

    def draw(self, surface, camera_x):
        pts = self.get_screen_points(camera_x)
        if len(pts) < 3:
            return

        trail_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        n = len(pts)
        for i in range(n - 1):
            ratio = (i + 1) / float(n)
            alpha = int(220 * (ratio ** 1.4))
            w_outer = max(2, int(13 * ratio))
            w_mid = max(1, int(8 * ratio))
            w_core = max(1, int(3 * ratio))
            p1, p2 = pts[i], pts[i + 1]
            pygame.draw.line(trail_surf, (240, 40, 15, alpha // 2), p1, p2, w_outer)
            pygame.draw.line(trail_surf, (255, 155, 10, alpha), p1, p2, w_mid)
            pygame.draw.line(trail_surf, (255, 245, 120, alpha), p1, p2, w_core)

        surface.blit(trail_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)