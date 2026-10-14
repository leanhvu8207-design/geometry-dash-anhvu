# levels/level_1_stereo.py
from config import *
from entities import Spike, JumpOrb, ModePortal, WaveCorridor
from .base_level import BaseLevel


class StereoMadnessLevel(BaseLevel):
    """Map 1: Stereo Madness (Cube Neon Tím & Đường hầm Zíc-zắc Wave)."""

    def __init__(self):
        meta = {
            "id": 0,
            "name": "STEREO MADNESS",
            "stars": 1,
            "diff_color": (0, 185, 255),
            "best_normal": 0,
            "best_practice": 0,
            "coins": 0,
        }
        super().__init__(meta_info=meta, length=8150.0, skin_name="PINK")

    def _update_theme(self):
        self.background.set_theme(self.player.mode)

    def _build_map(self):
        # Giai đoạn 1: Cube Neon
        self.hazards.append(Spike(750, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.add_neon_grid(1050, GROUND_Y, cols=2, rows=1, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)
        self.hazards.append(Spike(1350, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.hazards.append(Spike(1400, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))

        self.add_neon_grid(1680, 220, cols=2, rows=3, color=BLOCK_PURPLE, dots=[(0, 0), (1, 1), (0, 2)], bottom_glow=WHITE, has_chain=True)
        self.hazards.append(Spike(1680, 220, direction="DOWN", style="WHITE_STAR"))
        self.hazards.append(Spike(1730, 220, direction="DOWN", style="WHITE_STAR"))
        self.hazards.append(Spike(1780, 120, direction="RIGHT", style="BLUE"))
        self.hazards.append(Spike(1780, 70, direction="RIGHT", style="BLUE"))

        self.add_neon_grid(1800, GROUND_Y, cols=2, rows=2, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)
        self.add_neon_grid(2040, GROUND_Y, cols=1, rows=3, color=BLOCK_PINK, top_glow=BLOCK_ORANGE)
        self.triggers.append(JumpOrb(2065, GROUND_Y - 3 * TILE_SIZE - 35, orb_type="PURPLE_RING"))

        self.add_neon_grid(2340, 180, cols=2, rows=3, color=BLOCK_PURPLE, dots=[(0, 0), (1, 1), (1, 2)], bottom_glow=WHITE, has_chain=True)
        self.hazards.append(Spike(2340, 180, direction="DOWN", style="WHITE_STAR"))
        self.hazards.append(Spike(2390, 180, direction="DOWN", style="WHITE_STAR"))
        for r_idx in range(2):
            self.hazards.append(Spike(2340 - TILE_SIZE, 60 + r_idx * TILE_SIZE, direction="LEFT", style="BLUE"))
            self.hazards.append(Spike(2440, 60 + r_idx * TILE_SIZE, direction="RIGHT", style="BLUE"))

        self.add_neon_grid(2260, GROUND_Y, cols=5, rows=2, color=BLOCK_PURPLE, top_glow=(210, 120, 255))
        self.triggers.append(JumpOrb(2730, GROUND_Y - 115, orb_type="CYAN_ORB"))
        self.add_neon_grid(2840, 180, cols=3, rows=3, color=BLOCK_PURPLE, bottom_glow=(210, 120, 255))
        for r_idx in range(3):
            self.hazards.append(Spike(2840 - TILE_SIZE, 30 + r_idx * TILE_SIZE, direction="LEFT", style="BLUE"))

        self.add_neon_grid(2960, GROUND_Y, cols=4, rows=2, color=BLOCK_PURPLE, top_glow=BLOCK_ORANGE)
        self.triggers.append(JumpOrb(3320, GROUND_Y - 140, orb_type="PURPLE_RING"))
        self.add_neon_grid(3480, GROUND_Y, cols=4, rows=2, color=BLOCK_PURPLE, top_glow=CYAN_LIGHT)

        self.portals.append(ModePortal(3850, GROUND_Y - 360, target_mode=MODE_WAVE))
        self.portals.append(ModePortal(3850, GROUND_Y - 180, target_mode=MODE_WAVE))

        # Giai đoạn 2: Đường hầm Wave
        wave_top = [
            (3900, 90), (4150, 220), (4300, 120), (4450, 220), (4600, 120), (4750, 220), (4900, 120),
            (5050, 220), (5200, 120), (5450, 70), (5750, 220), (6050, 80), (6350, 210), (6700, 100),
        ]
        wave_bot = [
            (3900, 570), (4150, 510), (4300, 410), (4450, 510), (4600, 410), (4750, 510), (4900, 410),
            (5050, 510), (5200, 410), (5450, 340), (5750, 490), (6050, 350), (6350, 480), (6700, 570),
        ]
        guide_dots = [
            (4225, 315), (4375, 315), (4525, 315), (4675, 315), (4825, 315), (4975, 315),
            (5125, 315), (5450, 205), (5750, 355), (6050, 215), (6350, 345),
        ]
        self.corridors.append(WaveCorridor(3900, 6700, wave_top, wave_bot, guide_dots))

        self.portals.append(ModePortal(6720, 140, target_mode=MODE_CUBE))
        self.portals.append(ModePortal(6720, 320, target_mode=MODE_CUBE))

        # Giai đoạn 3: Bãi đáp cam dài 11 ô & Về đích
        self.add_neon_grid(6730, GROUND_Y, cols=11, rows=1, color=BLOCK_ORANGE, top_glow=BLOCK_ORANGE)
        self.hazards.append(Spike(7350, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.hazards.append(Spike(7400, GROUND_Y - TILE_SIZE, direction="UP", style="BLUE"))
        self.triggers.append(JumpOrb(7375, GROUND_Y - 140, orb_type="CYAN_ORB"))
        self.add_neon_grid(7560, GROUND_Y, cols=14, rows=2, color=BLOCK_PURPLE, top_glow=PROGRESS_GREEN)