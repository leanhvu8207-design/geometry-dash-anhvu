# vfx/draw_utils.py
import pygame
from config import *


class DrawUtils:
    """Bộ công cụ vẽ ánh sáng mịn (Smooth Radial Glow) và chữ viền chất lượng cao."""

    _glow_cache = {}

    @classmethod
    def get_smooth_glow_surface(cls, color, radius):
        """Tạo và lưu đệm (Cache) mặt phẳng phát sáng chuyển sắc mượt theo từng pixel."""
        key = (color, radius)
        if key in cls._glow_cache:
            return cls._glow_cache[key]

        size = radius * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        steps = max(12, radius // 2)
        for i in range(steps, 0, -1):
            ratio = i / float(steps)
            r = int(radius * ratio)
            # Hàm mũ bậc 2 giúp ánh sáng tan dần tự nhiên ở rìa, không bị viền cứng
            alpha = int(16 * ((1.0 - ratio) ** 1.8) + 4)
            pygame.draw.circle(surf, (*color, alpha), (radius, radius), r)

        cls._glow_cache[key] = surf
        return surf

    @classmethod
    def draw_glow_circle(cls, surface, color, center, radius, glow_layers=4):
        if radius <= 2:
            return
        glow_r = int(radius * 1.85)
        glow_surf = cls.get_smooth_glow_surface(color, glow_r)
        surface.blit(
            glow_surf,
            (int(center[0] - glow_r), int(center[1] - glow_r)),
            special_flags=pygame.BLEND_RGBA_ADD,
        )

    @staticmethod
    def draw_outlined_text(surface, text, font, pos, text_color, outline_color=BLACK, outline_width=3, center=True):
        base = font.render(text, True, text_color)
        outline = font.render(text, True, outline_color)
        w, h = base.get_size()
        target_x = pos[0] - w // 2 if center else pos[0]
        target_y = pos[1] - h // 2 if center else pos[1]

        surface.blit(outline, (target_x + outline_width, target_y + outline_width + 2))
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width + 1:
                    surface.blit(outline, (target_x + dx, target_y + dy))
        surface.blit(base, (target_x, target_y))