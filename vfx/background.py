# vfx/background.py
import pygame
from config import *


class ParallaxBackground:
    """Quản lý nền ô vuông Tiled, trần và mặt đất với hiệu ứng chuyển màu mượt mà."""

    def __init__(self):
        self.scroll_x = 0.0
        self.bg_color = list(MENU_BG_BLUE)
        self.target_bg_color = list(MENU_BG_BLUE)
        self.ground_color = list(MENU_GROUND_BLUE)
        self.target_ground_color = list(MENU_GROUND_BLUE)
        self.classic_ground_style = False

    def set_theme(self, mode):
        self.classic_ground_style = False
        if mode == STATE_MENU:
            self.target_bg_color = list(MENU_BG_BLUE)
            self.target_ground_color = list(MENU_GROUND_BLUE)
        elif mode == MODE_CUBE:
            self.target_bg_color = list(CUBE_BG_COLOR)
            self.target_ground_color = [8, 2, 20]
        elif mode == MODE_WAVE:
            self.target_bg_color = list(WAVE_BG_COLOR)
            self.target_ground_color = [8, 2, 20]

    def set_custom_theme(self, bg_rgb, ground_rgb, classic_ground=True):
        self.target_bg_color = list(bg_rgb)
        self.target_ground_color = list(ground_rgb)
        self.classic_ground_style = classic_ground

    def update(self, dt, speed=SCROLL_SPEED):
        self.scroll_x += speed * 0.25 * dt
        lerp_factor = min(1.0, dt * 3.2)
        for i in range(3):
            self.bg_color[i] += (self.target_bg_color[i] - self.bg_color[i]) * lerp_factor
            self.ground_color[i] += (self.target_ground_color[i] - self.ground_color[i]) * lerp_factor

    def draw(self, surface, camera_x, mode=STATE_MENU, draw_ground=True, draw_ceiling=False):
        cur_bg = tuple(max(0, min(255, int(c))) for c in self.bg_color)
        surface.fill(cur_bg)

        grid_color = tuple(max(0, min(255, int(c * 0.84))) for c in self.bg_color)
        border_color = tuple(max(0, min(255, int(c * 0.68))) for c in self.bg_color)

        box_size = 160
        offset_x = int(self.scroll_x) % box_size
        for x in range(-offset_x, SCREEN_WIDTH + box_size, box_size):
            for y in range(10, GROUND_Y, box_size):
                rect = pygame.Rect(x + 8, y + 8, box_size - 16, box_size - 16)
                pygame.draw.rect(surface, grid_color, rect)
                pygame.draw.rect(surface, border_color, rect, 3)

        cur_gnd = tuple(max(0, min(255, int(c))) for c in self.ground_color)

        # Vẽ trần khi ở chế độ Máy bay hoặc khi Đảo ngược trọng lực
        if draw_ceiling:
            ceil_rect = pygame.Rect(0, 0, SCREEN_WIDTH, CEILING_Y)
            pygame.draw.rect(surface, cur_gnd, ceil_rect)
            pygame.draw.line(surface, WHITE, (0, CEILING_Y), (SCREEN_WIDTH, CEILING_Y), 3)

        if not draw_ground:
            return

        ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        if mode == STATE_MENU or self.classic_ground_style:
            pygame.draw.rect(surface, cur_gnd, ground_rect)
            g_tile = 128
            g_off = int(camera_x) % g_tile
            panel_col = tuple(max(0, min(255, int(c * 0.72))) for c in cur_gnd)
            for x in range(-g_off, SCREEN_WIDTH + g_tile, g_tile):
                r = pygame.Rect(x + 5, GROUND_Y + 6, g_tile - 10, SCREEN_HEIGHT - GROUND_Y - 12)
                pygame.draw.rect(surface, panel_col, r, 3)

            shadow_surf = pygame.Surface((SCREEN_WIDTH, 20), pygame.SRCALPHA)
            for i in range(20):
                pygame.draw.line(shadow_surf, (0, 0, 0, int(130 * (1 - i / 20.0))), (0, i), (SCREEN_WIDTH, i))
            surface.blit(shadow_surf, (0, GROUND_Y))
            pygame.draw.line(surface, WHITE, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        else:
            pygame.draw.rect(surface, (8, 2, 20), ground_rect)
            tooth_w = 24
            g_off = int(camera_x) % tooth_w
            for x in range(-g_off, SCREEN_WIDTH + tooth_w, tooth_w):
                pygame.draw.rect(surface, (255, 110, 60), (x, GROUND_Y, tooth_w // 2, 7))
            pygame.draw.line(surface, (255, 60, 140), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)