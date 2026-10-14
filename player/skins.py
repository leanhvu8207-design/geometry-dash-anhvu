# player/skins.py
import math
import pygame
from config import *


class PlayerSkin:
    """Lớp cơ sở quản lý ngoại hình (Skin) của nhân vật cho cả 3 chế độ Cube, Ship, Wave."""

    trail_color = PLAYER_PINK

    def __init__(self, w=46, h=46):
        self.w = w
        self.h = h
        self.cube_surf = self._bake_cube()
        self.ship_surf = self._bake_ship()
        self.wave_surf = self._bake_wave()

    def _bake_cube(self):
        raise NotImplementedError

    def _bake_ship(self):
        w, h = 68, 46
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pilot = pygame.transform.smoothscale(self.cube_surf, (24, 24))
        surf.blit(pilot, (24, 2))

        nozzle_pts = [(4, 24), (14, 20), (14, 38), (4, 34)]
        pygame.draw.polygon(surf, WHITE, [(p[0] - 1, p[1]) for p in nozzle_pts], 3)
        pygame.draw.polygon(surf, self.trail_color, nozzle_pts)
        pygame.draw.polygon(surf, BLACK, nozzle_pts, 2)

        hull_pts = [(12, 18), (44, 18), (65, 30), (62, 41), (14, 41)]
        pygame.draw.polygon(surf, WHITE, hull_pts, 4)
        pygame.draw.polygon(surf, self.trail_color, hull_pts)
        pygame.draw.polygon(surf, BLACK, hull_pts, 2)

        wing_pts = [(18, 25), (42, 25), (50, 35), (18, 35)]
        pygame.draw.polygon(surf, tuple(max(0, c - 45) for c in self.trail_color), wing_pts)
        pygame.draw.polygon(surf, BLACK, wing_pts, 2)
        return surf

    def _bake_wave(self):
        surf = pygame.Surface((52, 52), pygame.SRCALPHA)
        pts = [(48, 26), (8, 8), (18, 26), (8, 44)]
        pygame.draw.polygon(surf, WAVE_PLAYER_PURPLE, pts)
        pygame.draw.polygon(surf, WHITE, pts, 3)
        return surf

    def draw(self, surface, player, camera_x):
        sx = int(player.x - camera_x)
        sy = int(player.y)
        cx = sx + player.w // 2
        cy = sy + player.h // 2

        if player.mode == MODE_CUBE:
            rotated = pygame.transform.rotate(self.cube_surf, player.angle)
            surface.blit(rotated, rotated.get_rect(center=(cx, cy)).topleft)
        elif player.mode == MODE_SHIP:
            ship_img = pygame.transform.flip(self.ship_surf, False, player.gravity_dir < 0)
            rotated = pygame.transform.rotate(ship_img, player.angle)
            surface.blit(rotated, rotated.get_rect(center=(cx, cy)).topleft)
        elif player.mode == MODE_WAVE:
            ring_r = int(26 + math.sin(player.pulse_timer * 10.0) * 5)
            pygame.draw.circle(surface, WAVE_TRAIL_PINK, (cx - 18, cy + 12), ring_r, 2)
            rotated = pygame.transform.rotate(self.wave_surf, player.angle)
            surface.blit(rotated, rotated.get_rect(center=(cx, cy)).topleft)


class CutePinkSkin(PlayerSkin):
    """Skin Khối vuông Hồng Kawaii dành cho Map 1."""

    trail_color = PLAYER_PINK

    def _bake_cube(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, BLACK, (0, 0, self.w, self.h), border_radius=6)
        pygame.draw.rect(surf, PLAYER_YELLOW, (2, 2, self.w - 4, self.h - 4), border_radius=5)
        pygame.draw.rect(surf, PLAYER_PINK, (6, 6, self.w - 12, self.h - 12), border_radius=4)
        pygame.draw.ellipse(surf, (255, 130, 90), (11, self.h - 16, self.w - 22, 12))
        pygame.draw.circle(surf, BLACK, (14, 19), 4)
        pygame.draw.circle(surf, WHITE, (13, 18), 1)
        pygame.draw.circle(surf, BLACK, (self.w - 14, 19), 4)
        pygame.draw.circle(surf, WHITE, (self.w - 15, 18), 1)
        pygame.draw.arc(surf, BLACK, (19, 17, 8, 7), math.pi, math.tau, 2)
        return surf


class ClassicGreenSkin(PlayerSkin):
    """Skin Khối vuông Xanh lá đồng tâm dành cho Map 2."""

    trail_color = PLAYER_GREEN_OUTER

    def _bake_cube(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, WHITE, (0, 0, self.w, self.h), border_radius=3)
        pygame.draw.rect(surf, BLACK, (2, 2, self.w - 4, self.h - 4), border_radius=2)
        pygame.draw.rect(surf, PLAYER_GREEN_OUTER, (4, 4, self.w - 8, self.h - 8))
        pygame.draw.rect(surf, BLACK, (11, 11, self.w - 22, self.h - 22))
        pygame.draw.rect(surf, PLAYER_PURPLE_MID, (13, 13, self.w - 26, self.h - 26))
        pygame.draw.rect(surf, BLACK, (17, 17, self.w - 34, self.h - 34))
        pygame.draw.rect(surf, (165, 255, 35), (19, 19, self.w - 38, self.h - 38))
        return surf