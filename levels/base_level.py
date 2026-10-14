# levels/base_level.py
import pygame
from config import *
from vfx import ParticleSystem, WaveTrail, ShipFlameTrail, VictoryWallEffect, ParallaxBackground
from player import Player
from entities import NeonBlock, ClassicDarkBlock, GridBlock, FloatingSlab, WaveCorridor


class BaseLevel:
    """
    Lớp cơ sở (Base Class) cho mọi Màn chơi trong game.
    Các Map con chỉ cần ghi đè (override) phương thức `_build_map()` và `_update_theme()`.
    """

    def __init__(self, meta_info, length=8200.0, skin_name="PINK"):
        self.meta = meta_info
        self.level_length = float(length)
        self.skin_name = skin_name

        self.player = Player(start_x=200, start_y=GROUND_Y - 46)
        self.player.set_skin(self.skin_name)

        self.background = ParallaxBackground()
        self.particles = ParticleSystem()
        self.wave_trail = WaveTrail()
        self.ship_trail = ShipFlameTrail()
        self.victory_vfx = VictoryWallEffect(self.level_length)

        self.blocks = []
        self.hazards = []
        self.triggers = []
        self.portals = []
        self.corridors = []

        self.camera_x = 0.0
        self.progress = 0

        self._build_map()
        self.reset()

    @property
    def best_progress(self):
        return self.meta["best_normal"]

    @best_progress.setter
    def best_progress(self, val):
        self.meta["best_normal"] = max(self.meta["best_normal"], int(val))
        if self.meta["best_normal"] >= 100:
            self.meta["coins"] = 3

    # --- CÁC HÀM TIỆN ÍCH DỰNG MAP NHANH CHO LỚP CON ---
    def add_neon_grid(self, start_x, bottom_y, cols, rows, color=BLOCK_PURPLE, dots=None, top_glow=None, bottom_glow=None, has_chain=False):
        dots_set = set(dots) if dots else set()
        for c in range(cols):
            for r in range(rows):
                bx = start_x + c * TILE_SIZE
                by = bottom_y - (r + 1) * TILE_SIZE
                is_top = (r == rows - 1)
                is_bot = (r == 0)
                self.blocks.append(
                    NeonBlock(
                        bx, by, color=color, has_dot=((c, r) in dots_set),
                        top_glow=(top_glow if is_top else None),
                        bottom_glow=(bottom_glow if is_bot else None),
                        has_chain=(has_chain and is_top and c == cols // 2),
                    )
                )

    def add_grid_fortress(self, start_x, bottom_y, cols, rows, color=(140, 25, 215), white_top=True, ring_bottom=False):
        for c in range(cols):
            for r in range(rows):
                bx = start_x + c * TILE_SIZE
                by = bottom_y - (r + 1) * TILE_SIZE
                edges = []
                if white_top:
                    if r == rows - 1:
                        edges.append("TOP")
                    if c == 0:
                        edges.append("LEFT")
                    if c == cols - 1:
                        edges.append("RIGHT")
                else:
                    edges.append("ALL")
                attach = "DOWN" if (ring_bottom and r == 0 and c == cols // 2) else None
                self.blocks.append(GridBlock(bx, by, color=color, white_edges=edges, ring_attach=attach))

    def add_dark_blocks(self, start_x, bottom_y, cols, rows, color=(220, 20, 25)):
        for c in range(cols):
            for r in range(rows):
                bx = start_x + c * TILE_SIZE
                by = bottom_y - (r + 1) * TILE_SIZE
                self.blocks.append(ClassicDarkBlock(bx, by, color=color))

    def add_slab(self, start_x, y, cols=2, color=(150, 35, 225), ring_attach=None):
        for c in range(cols):
            attach = ring_attach if (c == cols // 2) else None
            self.blocks.append(FloatingSlab(start_x + c * TILE_SIZE, y, color=color, ring_attach=attach))

    def _build_map(self):
        raise NotImplementedError

    def _update_theme(self):
        pass

    def reset(self):
        self.player.set_skin(self.skin_name)
        self.player.reset()
        self.particles.clear()
        self.wave_trail.clear()
        self.ship_trail.clear()
        self.victory_vfx.reset(self.level_length)
        self.camera_x = 0.0
        self.progress = 0

        for trig in self.triggers:
            trig.reset()
        for portal in self.portals:
            portal.reset()

        self._update_theme()

    def update(self, dt, is_holding, just_pressed):
        self.background.update(dt, speed=(0 if (self.player.is_dead or self.player.victory) else SCROLL_SPEED))
        self.particles.update(dt)
        self.victory_vfx.update(dt)

        for haz in self.hazards:
            haz.update(dt)
        for trig in self.triggers:
            trig.update(dt)
        for portal in self.portals:
            portal.update(dt)

        if self.player.is_dead or self.player.victory:
            return

        self._update_theme()

        prev_mode = self.player.mode
        self.player.update(
            dt,
            is_holding,
            just_pressed,
            self.blocks,
            self.triggers,
            self.portals,
            self.corridors,
            self.wave_trail,
            self.ship_trail,
            self.particles,
        )

        if self.player.mode != prev_mode:
            if self.player.mode == MODE_WAVE and self.player.y > 420:
                self.player.y = 360
            elif self.player.mode == MODE_CUBE and self.player.gravity_dir > 0:
                max_safe_y = GROUND_Y - TILE_SIZE - self.player.h - 6
                if self.player.y > max_safe_y:
                    self.player.y = max_safe_y
                self.player.vel_y = max(0.0, self.player.vel_y * 0.35)

        # Kiểm tra va chạm với mọi chướng ngại vật kế thừa từ Hazard (Spike, SpikeStrip, Sawblade)
        p_rect = self.player.rect
        for haz in self.hazards:
            if haz.is_visible(self.camera_x) and haz.check_collision(p_rect):
                self.player.is_dead = True
                break

        if self.player.is_dead:
            self.particles.spawn_explosion(
                self.player.x + self.player.w // 2,
                self.player.y + self.player.h // 2,
                self.player.skin.trail_color,
                count=45,
            )
            return

        self.camera_x = self.player.x - 260.0
        raw_pct = int(((self.player.x - 200.0) / (self.level_length - 200.0)) * 100)
        self.progress = max(0, min(100, raw_pct))

        if self.progress > self.best_progress:
            self.best_progress = self.progress

        # Khi chạm vào Bức tường cuối màn -> Phá đảo!
        if self.player.x + self.player.w >= self.level_length:
            self.progress = 100
            self.best_progress = 100
            self.player.victory = True
            self.victory_vfx.trigger(self.player.y + self.player.h // 2)
            self.particles.spawn_explosion(
                self.player.x + self.player.w // 2,
                self.player.y + self.player.h // 2,
                PROGRESS_GREEN,
                count=65,
            )

    def draw(self, surface):
        in_wave_tunnel = (self.player.mode == MODE_WAVE and len(self.corridors) > 0)
        need_ceiling = (self.player.mode == MODE_SHIP) or (self.player.gravity_dir < 0)
        self.background.draw(
            surface,
            self.camera_x,
            mode=self.player.mode,
            draw_ground=(not in_wave_tunnel),
            draw_ceiling=need_ceiling,
        )

        for cor in self.corridors:
            cor.draw(surface, self.camera_x)
        for blk in self.blocks:
            blk.draw(surface, self.camera_x)
        for haz in self.hazards:
            haz.draw(surface, self.camera_x)
        for trig in self.triggers:
            trig.draw(surface, self.camera_x)
        for portal in self.portals:
            portal.draw(surface, self.camera_x)

        self.victory_vfx.draw_wall(surface, self.camera_x)

        if self.player.mode == MODE_WAVE:
            self.wave_trail.draw(surface, self.camera_x)
        elif self.player.mode == MODE_SHIP:
            self.ship_trail.draw(surface, self.camera_x)

        self.particles.draw(surface, self.camera_x)
        if not self.player.victory:
            self.player.draw(surface, self.camera_x)

        if self.player.victory:
            self.victory_vfx.draw_victory_overlay(surface, self.camera_x, self.meta["name"])