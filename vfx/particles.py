# vfx/particles.py
import math
import random
import pygame
from config import *


class Particle:
    """Hạt hiệu ứng mịn có độ trong suốt giảm dần mượt mà."""

    def __init__(self, x, y, vx, vy, size, color, lifetime, shape="SQUARE"):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.size = float(size)
        self.color = color
        self.lifetime = float(lifetime)
        self.max_lifetime = float(lifetime)
        self.shape = shape

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        self.size = max(0.0, self.size - 5.5 * dt)

    def draw(self, surface, camera_x):
        if self.lifetime <= 0 or self.size <= 1.0:
            return
        sx = self.x - camera_x
        if -30 <= sx <= SCREEN_WIDTH + 30:
            ratio = max(0.0, min(1.0, self.lifetime / self.max_lifetime))
            alpha = int(230 * (ratio ** 1.3))
            s = max(2, int(self.size))
            surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
            if self.shape == "CIRCLE":
                pygame.draw.circle(surf, (*self.color, alpha // 3), (s, s), s)
                pygame.draw.circle(surf, (*self.color, alpha), (s, s), max(1, s // 2))
            else:
                rect = pygame.Rect(s // 2, s // 2, s, s)
                pygame.draw.rect(surf, (*self.color, alpha), rect, border_radius=2)
            surface.blit(surf, (int(sx - s), int(self.y - s)))


class ParticleSystem:
    """Quản lý toàn bộ các hạt hiệu ứng trong màn chơi."""

    def __init__(self):
        self.particles = []

    def clear(self):
        self.particles.clear()

    def spawn_trail(self, x, y, color):
        vx = random.uniform(-90, -20)
        vy = random.uniform(-65, -10)
        size = random.uniform(4.0, 7.5)
        self.particles.append(Particle(x, y, vx, vy, size, color, random.uniform(0.22, 0.38), shape="SQUARE"))

    def spawn_ship_sparks(self, x, y):
        col = random.choice([PLAYER_GREEN_OUTER, (255, 210, 40), (255, 110, 20)])
        vx = random.uniform(-170, -50)
        vy = random.uniform(-55, 55)
        size = random.uniform(3.5, 6.5)
        self.particles.append(Particle(x, y, vx, vy, size, col, random.uniform(0.18, 0.35), shape="CIRCLE"))

    def spawn_explosion(self, x, y, color, count=40):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(80, 480)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(4.5, 10.0)
            shape = "CIRCLE" if random.random() < 0.5 else "SQUARE"
            self.particles.append(Particle(x, y, vx, vy, size, color, random.uniform(0.35, 0.75), shape=shape))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0 and p.size > 1.0]

    def draw(self, surface, camera_x):
        for p in self.particles:
            p.draw(surface, camera_x)