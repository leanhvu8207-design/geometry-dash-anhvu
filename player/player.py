# player/player.py
import pygame
from config import *
from .modes import CubeMode, ShipMode, WaveMode
from .skins import CutePinkSkin, ClassicGreenSkin


class Player:
    """Lớp Nhân vật chính kết hợp Strategy Pattern cho Chế độ di chuyển (Mode) và Ngoại hình (Skin)."""

    def __init__(self, start_x, start_y):
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.w = 46
        self.h = 46

        # Khởi tạo kho chế độ chơi và kho Skin
        self._modes = {
            MODE_CUBE: CubeMode(),
            MODE_SHIP: ShipMode(),
            MODE_WAVE: WaveMode(),
        }
        self._skins = {
            "PINK": CutePinkSkin(self.w, self.h),
            "GREEN_CONCENTRIC": ClassicGreenSkin(self.w, self.h),
        }

        self.skin = self._skins["PINK"]
        self.current_mode = self._modes[MODE_CUBE]
        self.reset()

    def set_skin(self, skin_name):
        if skin_name in self._skins:
            self.skin = self._skins[skin_name]

    def set_mode(self, mode_name, wave_trail=None, ship_trail=None):
        if mode_name in self._modes and self.current_mode.mode_name != mode_name:
            self.current_mode = self._modes[mode_name]
            self.vel_y = 0.0
            if wave_trail is not None and ship_trail is not None:
                self.current_mode.on_enter(self, wave_trail, ship_trail)

    @property
    def mode(self):
        return self.current_mode.mode_name

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel_y = 0.0
        self.angle = 0.0
        self.gravity_dir = 1  # +1: Bình thường, -1: Đảo ngược trọng lực lên trần
        self.current_mode = self._modes[MODE_CUBE]
        self.on_ground = False
        self.is_dead = False
        self.victory = False
        self.pulse_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, is_holding, just_pressed, blocks, triggers, portals, corridors, wave_trail, ship_trail, particles):
        if self.is_dead or self.victory:
            return

        self.pulse_timer += dt
        self.x += SCROLL_SPEED * dt

        # Ủy quyền tính toán vật lý cho Mode hiện tại (Cube / Ship / Wave)
        self.current_mode.update_physics(
            self, dt, is_holding, just_pressed, blocks, triggers, corridors, wave_trail, ship_trail, particles
        )

        if self.is_dead:
            return

        # Kiểm tra va chạm với các Cổng dịch chuyển (ModePortal & GravityPortal)
        for portal in portals:
            if not portal.triggered and self.rect.colliderect(portal.rect):
                portal.apply_portal_effect(self, wave_trail, ship_trail, particles)

    def draw(self, surface, camera_x):
        if not self.is_dead:
            self.skin.draw(surface, self, camera_x)