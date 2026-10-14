# level.py
import pygame
from config import *
from vfx import ParticleSystem, WaveTrail, ParallaxBackground
from entities import Block, Spike, Orb, Portal, WaveCorridor, Player


class Level:
    """Quản lý toàn bộ dữ liệu bản đồ, Camera, tiến độ (%) và tương tác thực thể của màn chơi."""

    def __init__(self):
        self.player = Player(start_x=200, start_y=GROUND_Y - 46)
        self.background = ParallaxBackground()
        self.particles = ParticleSystem()
        self.wave_trail = WaveTrail()

        self.blocks = []
        self.spikes = []
        self.orbs = []
        self.portals = []
        self.corridors = []

        self.level_length = 8000.0
        self.camera_x = 0.0
        self.progress = 0
        self.best_progress = 0  # Bắt đầu từ 0% và tự động lưu kỷ lục cao nhất của người chơi

        self._build_level()
        self.background.set_theme(MODE_CUBE)

    def _add_block_grid(
        self,
        start_x,
        bottom_y,
        cols,
        rows,
        color=BLOCK_PURPLE,
        dots_coords=None,
        top_glow=None,
        bottom_glow=None,
        has_chain=False,
    ):
        """Hàm tiện ích dựng nhanh một cụm khối vuông (cột hoặc bục) theo hàng và cột."""
        dots_set = set(dots_coords) if dots_coords else set()
        for c in range(cols):
            for r in range(rows):
                bx = start_x + c * TILE_SIZE
                by = bottom_y - (r + 1) * TILE_SIZE
                is_top_row = (r == rows - 1)
                is_bot_row = (r == 0)
                self.blocks.append(
                    Block(
                        x=bx,
                        y=by,
                        color=color,
                        has_dot=((c, r) in dots_set),
                        top_glow=(top_glow if is_top_row else None),
                        bottom_glow=(bottom_glow if is_bot_row else None),
                        has_chain=(has_chain and is_top_row and c == cols // 2),
                    )
                )

    def _build_level(self):
        """Thiết kế màn chơi hoàn chỉnh với quỹ đạo nhảy đã được tính toán chuẩn xác."""
        self.blocks.clear()
        self.spikes.clear()
        self.orbs.clear()
        self.portals.clear()
        self.corridors.clear()

        # =========================================================================
        # GIAI ĐOẠN 1: PHÂN CẢNH CUBE NEON TÍM (X: 600 -> 3850)
        # =========================================================================

        # 1. Cụm khởi động làm quen nhịp nhảy
        self.spikes.append(Spike(750, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self._add_block_grid(1050, GROUND_Y, cols=2, rows=1, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)
        self.spikes.append(Spike(1350, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.spikes.append(Spike(1400, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))

        # 2. CỤM CHƯỚNG NGẠI VẬT MỐC 22% - 45% (ĐÃ MỞ RỘNG LỐI ĐI RỘNG RÃI)
        # - Trụ treo bên trái: treo cao ở y = 220 để không vướng đầu khi nhảy lên bục cam
        self._add_block_grid(
            1680,
            220,
            cols=2,
            rows=3,
            color=BLOCK_PURPLE,
            dots_coords=[(0, 0), (1, 1), (0, 2)],
            bottom_glow=WHITE,
            has_chain=True,
        )
        self.spikes.append(Spike(1680, 220, direction="DOWN", style="WHITE_STAR"))
        self.spikes.append(Spike(1730, 220, direction="DOWN", style="WHITE_STAR"))
        self.spikes.append(Spike(1780, 120, direction="RIGHT", style="BLUE"))
        self.spikes.append(Spike(1780, 70, direction="RIGHT", style="BLUE"))

        # - Bục cam 2x2 dưới mặt đất (đỉnh ở y = 490)
        self._add_block_grid(1800, GROUND_Y, cols=2, rows=2, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)

        # - Cột hồng 1x3 (đỉnh ở y = 440) + Vòng nhảy tím hỗ trợ
        self._add_block_grid(2040, GROUND_Y, cols=1, rows=3, color=BLOCK_PINK, top_glow=BLOCK_ORANGE)
        self.orbs.append(Orb(2065, GROUND_Y - 3 * TILE_SIZE - 35, orb_type="PURPLE_RING"))

        # - Trụ treo ở giữa: nâng đáy lên y = 180 (mũi gai ở y = 230), cách mặt bục tím bên dưới 260px!
        self._add_block_grid(
            2340,
            180,
            cols=2,
            rows=3,
            color=BLOCK_PURPLE,
            dots_coords=[(0, 0), (1, 1), (1, 2)],
            bottom_glow=WHITE,
            has_chain=True,
        )
        self.spikes.append(Spike(2340, 180, direction="DOWN", style="WHITE_STAR"))
        self.spikes.append(Spike(2390, 180, direction="DOWN", style="WHITE_STAR"))
        for r_idx in range(2):
            self.spikes.append(Spike(2340 - TILE_SIZE, 60 + r_idx * TILE_SIZE, direction="LEFT", style="BLUE"))
            self.spikes.append(Spike(2440, 60 + r_idx * TILE_SIZE, direction="RIGHT", style="BLUE"))

        # - Bục lớn màu tím bên dưới: hạ xuống 2 hàng (cols=5, rows=2, đỉnh ở y = 490) giúp đi qua cực thoáng
        self._add_block_grid(2260, GROUND_Y, cols=5, rows=2, color=BLOCK_PURPLE, top_glow=(210, 120, 255))

        # - Quả cầu Cyan phát sáng (Cyan Orb) + Trụ treo bên phải nâng cao lên y = 180
        self.orbs.append(Orb(2730, GROUND_Y - 115, orb_type="CYAN_ORB"))
        self._add_block_grid(2840, 180, cols=3, rows=3, color=BLOCK_PURPLE, bottom_glow=(210, 120, 255))
        for r_idx in range(3):
            self.spikes.append(Spike(2840 - TILE_SIZE, 30 + r_idx * TILE_SIZE, direction="LEFT", style="BLUE"))

        # 3. Nhịp cầu nối dẫn vào cổng Wave Portal (bục cao 2 ô để nhảy từ đất hay từ Orb đều lên được)
        self._add_block_grid(2960, GROUND_Y, cols=4, rows=2, color=BLOCK_PURPLE, top_glow=BLOCK_ORANGE)
        self.orbs.append(Orb(3320, GROUND_Y - 140, orb_type="PURPLE_RING"))
        self._add_block_grid(3480, GROUND_Y, cols=4, rows=2, color=BLOCK_PURPLE, top_glow=CYAN_LIGHT)

        # Cổng chuyển sang chế độ WAVE tại X = 3850 (Đặt 2 cổng nối dọc để không bao giờ bị lọt qua)
        self.portals.append(Portal(3850, GROUND_Y - 360, target_mode=MODE_WAVE))
        self.portals.append(Portal(3850, GROUND_Y - 180, target_mode=MODE_WAVE))

        # =========================================================================
        # GIAI ĐOẠN 2: ĐƯỜNG HẦM ZÍC-ZẮC NEON WAVE (X: 3900 -> 6700)
        # =========================================================================
        wave_top = [
            (3900, 90),
            (4150, 220),
            (4300, 120),
            (4450, 220),
            (4600, 120),
            (4750, 220),
            (4900, 120),
            (5050, 220),
            (5200, 120),
            (5450, 70),
            (5750, 220),
            (6050, 80),
            (6350, 210),
            (6700, 100),
        ]
        wave_bot = [
            (3900, 570),
            (4150, 510),
            (4300, 410),
            (4450, 510),
            (4600, 410),
            (4750, 510),
            (4900, 410),
            (5050, 510),
            (5200, 410),
            (5450, 340),
            (5750, 490),
            (6050, 350),
            (6350, 480),
            (6700, 570),
        ]
        guide_dots = [
            (4225, 315),
            (4375, 315),
            (4525, 315),
            (4675, 315),
            (4825, 315),
            (4975, 315),
            (5125, 315),
            (5450, 205),
            (5750, 355),
            (6050, 215),
            (6350, 345),
        ]
        self.corridors.append(WaveCorridor(3900, 6700, wave_top, wave_bot, guide_dots))

        # Cổng chuyển ngược về chế độ CUBE tại cuối hầm Wave (X = 6720)
        self.portals.append(Portal(6720, 140, target_mode=MODE_CUBE))
        self.portals.append(Portal(6720, 320, target_mode=MODE_CUBE))

        # =========================================================================
        # GIAI ĐOẠN 3: CÚ NHẢY VỀ ĐÍCH (X: 6800 -> 8000)
        # =========================================================================
        self._add_block_grid(6950, GROUND_Y, cols=3, rows=1, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)
        self.orbs.append(Orb(7250, GROUND_Y - 135, orb_type="CYAN_ORB"))
        self.spikes.append(Spike(7200, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.spikes.append(Spike(7250, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))

        # Bục vinh quang trải dài đến vạch đích 100%
        self._add_block_grid(7450, GROUND_Y, cols=12, rows=2, color=BLOCK_PURPLE, top_glow=PROGRESS_GREEN)

    def reset(self):
        """Khởi động lại màn chơi nhưng vẫn giữ nguyên kỷ lục best_progress."""
        self.player.reset()
        self.particles.clear()
        self.wave_trail.clear()
        self.camera_x = 0.0
        self.progress = 0
        self.background.set_theme(MODE_CUBE)

        for orb in self.orbs:
            orb.activated = False
        for portal in self.portals:
            portal.triggered = False

    def update(self, dt, is_holding, just_pressed):
        self.background.update(dt, speed=(0 if self.player.is_dead else SCROLL_SPEED))
        self.particles.update(dt)

        for orb in self.orbs:
            orb.update(dt)
        for portal in self.portals:
            portal.update(dt)

        if self.player.is_dead or self.player.victory:
            return

        prev_mode = self.player.mode
        self.player.update(
            dt,
            is_holding,
            just_pressed,
            self.blocks,
            self.orbs,
            self.portals,
            self.corridors,
            self.wave_trail,
            self.particles,
        )

        # Khi vừa chuyển sang chế độ Wave, căn chỉnh độ cao hợp lý để vào đầu đường hầm an toàn
        if self.player.mode != prev_mode:
            self.background.set_theme(self.player.mode)
            if self.player.mode == MODE_WAVE and self.player.y > 420:
                self.player.y = 360

        # Kiểm tra va chạm với Gai nhọn (Spikes)
        p_rect = self.player.rect
        for spk in self.spikes:
            if spk.is_visible(self.camera_x) and p_rect.colliderect(spk.hitbox):
                self.player.is_dead = True
                break

        # Nếu vừa chết -> Tạo hiệu ứng nổ hạt rực rỡ
        if self.player.is_dead:
            explosion_col = PLAYER_PINK if self.player.mode == MODE_CUBE else WAVE_TRAIL_PINK
            self.particles.spawn_explosion(
                self.player.x + self.player.w // 2,
                self.player.y + self.player.h // 2,
                explosion_col,
                count=45,
            )
            return

        # Cập nhật Camera bám theo nhân vật và tính phần trăm tiến độ (0% -> 100%)
        self.camera_x = self.player.x - 260.0
        raw_pct = int(((self.player.x - 200.0) / (self.level_length - 200.0)) * 100)
        self.progress = max(0, min(100, raw_pct))

        # Cập nhật kỷ lục cao nhất người chơi đạt được trong game
        if self.progress > self.best_progress:
            self.best_progress = self.progress

        if self.progress >= 100:
            self.player.victory = True
            self.best_progress = 100
            self.particles.spawn_explosion(
                self.player.x + self.player.w // 2,
                self.player.y + self.player.h // 2,
                PROGRESS_GREEN,
                count=60,
            )

    def draw(self, surface):
        in_wave_tunnel = (self.player.mode == MODE_WAVE)
        self.background.draw(surface, self.camera_x, mode=self.player.mode, draw_ground=(not in_wave_tunnel))

        for cor in self.corridors:
            cor.draw(surface, self.camera_x)

        for blk in self.blocks:
            blk.draw(surface, self.camera_x)
        for spk in self.spikes:
            spk.draw(surface, self.camera_x)
        for orb in self.orbs:
            orb.draw(surface, self.camera_x)
        for portal in self.portals:
            portal.draw(surface, self.camera_x)

        if self.player.mode == MODE_WAVE:
            self.wave_trail.draw(surface, self.camera_x)

        self.particles.draw(surface, self.camera_x)
        self.player.draw(surface, self.camera_x)