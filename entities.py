# entities.py
import math
import pygame
from config import *
from vfx import DrawUtils


class GameObject:
    """Lớp cơ sở (Base Class) cho mọi vật thể trong màn chơi."""

    def __init__(self, x, y, w, h):
        self.x = float(x)
        self.y = float(y)
        self.w = int(w)
        self.h = int(h)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def is_visible(self, camera_x):
        """Kiểm tra vật thể có nằm trong vùng nhìn của Camera không (Culling)."""
        return (self.x + self.w >= camera_x - 100) and (self.x <= camera_x + SCREEN_WIDTH + 100)

    def update(self, dt):
        pass

    def draw(self, surface, camera_x):
        pass


class Block(GameObject):
    """
    Khối vuông cấu trúc màn chơi:
    - Hỗ trợ màu sắc tùy chỉnh (Cam, Hồng, Tím)
    - Hỗ trợ chấm tròn trắng ở tâm (has_dot)
    - Hỗ trợ dải sọc đen trắng + đèn Neon phát sáng ở đỉnh/đáy (top_glow, bottom_glow)
    - Hỗ trợ dây xích xanh treo lên trần (has_chain)
    """

    def __init__(
        self,
        x,
        y,
        color=BLOCK_PURPLE,
        has_dot=False,
        top_glow=None,
        bottom_glow=None,
        has_chain=False,
    ):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.has_dot = has_dot
        self.top_glow = top_glow        # Màu đèn phát sáng phía trên (nếu có)
        self.bottom_glow = bottom_glow  # Màu đèn phát sáng phía dưới (nếu có)
        self.has_chain = has_chain      # Vẽ dây xích treo từ đỉnh khối lên trần

        # Tạo bề mặt (Surface) được dựng sẵn (Pre-rendered) cho từng ô để tối ưu FPS
        self.block_surf = self._bake_block_surface()

    def _bake_block_surface(self):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        # Viền đen/tối bên ngoài
        pygame.draw.rect(surf, (15, 5, 30), (0, 0, self.w, self.h), border_radius=4)

        # Lớp màu nền chính bên trong
        inner_margin = 4
        pygame.draw.rect(
            surf,
            self.color,
            (inner_margin, inner_margin, self.w - inner_margin * 2, self.h - inner_margin * 2),
            border_radius=4,
        )

        # Lớp sáng nhẹ ở tâm khối tạo độ nổi 3D
        bright_color = tuple(min(255, c + 45) for c in self.color)
        core_margin = 10
        pygame.draw.rect(
            surf,
            bright_color,
            (core_margin, core_margin, self.w - core_margin * 2, self.h - core_margin * 2),
            border_radius=3,
        )

        # Viền mảnh sáng bên trong
        pygame.draw.rect(
            surf,
            tuple(min(255, c + 70) for c in self.color),
            (inner_margin, inner_margin, self.w - inner_margin * 2, self.h - inner_margin * 2),
            2,
            border_radius=4,
        )

        # Chấm tròn trắng (đinh tán) ở giữa khối giống hình mẫu 3
        if self.has_dot:
            center = (self.w // 2, self.h // 2)
            pygame.draw.circle(surf, (25, 10, 45), center, 9)
            pygame.draw.circle(surf, WHITE, center, 6)

        return surf

    def _draw_hazard_and_glow(self, surface, sx, sy, glow_color, is_top=True):
        """Vẽ thanh sọc đen-trắng và hào quang phát sáng trên đỉnh hoặc dưới đáy khối."""
        stripe_h = 6
        bar_y = sy - stripe_h if is_top else sy + self.h

        # Vẽ nền trắng và các vạch đen cho thanh cảnh báo
        pygame.draw.rect(surface, WHITE, (sx, bar_y, self.w, stripe_h))
        for offset in range(0, self.w, 12):
            pygame.draw.rect(surface, BLACK, (sx + offset, bar_y, 6, stripe_h))

        # Vẽ quầng sáng Neon tỏa ra bằng Alpha Surface cục bộ
        glow_h = 28
        glow_surf = pygame.Surface((self.w, glow_h), pygame.SRCALPHA)
        for i in range(glow_h):
            ratio = (glow_h - i) / glow_h if not is_top else (i / glow_h)
            alpha = int(135 * (ratio ** 1.6))
            pygame.draw.line(glow_surf, (*glow_color, alpha), (0, i), (self.w, i))

        dest_y = bar_y - glow_h if is_top else bar_y + stripe_h
        surface.blit(glow_surf, (sx, dest_y), special_flags=pygame.BLEND_RGBA_ADD)

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx = int(self.x - camera_x)
        sy = int(self.y)

        # Vẽ dây xích treo màu xanh dương nếu là trụ lơ lửng
        if self.has_chain:
            chain_x = sx + self.w // 2
            # Đế gắn dây xích
            pygame.draw.rect(surface, (10, 90, 240), (chain_x - 14, sy - 8, 28, 8), border_radius=3)
            # Các mắt xích nối lên phía trên
            curr_y = sy - 16
            link_idx = 0
            while curr_y > -20:
                if link_idx % 2 == 0:
                    pygame.draw.rect(surface, (15, 115, 255), (chain_x - 6, curr_y - 12, 12, 18), 3, border_radius=4)
                else:
                    pygame.draw.line(surface, (60, 160, 255), (chain_x, curr_y - 10), (chain_x, curr_y + 4), 4)
                curr_y -= 14
                link_idx += 1

        # Vẽ thân khối vuông
        surface.blit(self.block_surf, (sx, sy))

        # Vẽ hiệu ứng phát sáng đỉnh / đáy (nếu có)
        if self.top_glow:
            self._draw_hazard_and_glow(surface, sx, sy, self.top_glow, is_top=True)
        if self.bottom_glow:
            self._draw_hazard_and_glow(surface, sx, sy, self.bottom_glow, is_top=False)


class Spike(GameObject):
    """
    Chướng ngại vật Gai nhọn (Spike):
    - Hỗ trợ 4 hướng: 'UP', 'DOWN', 'LEFT', 'RIGHT'
    - Hỗ trợ kiểu gai trắng treo trần có sao lấp lánh hoặc gai xanh dương bên sườn trụ
    """

    def __init__(self, x, y, direction="UP", style="BLUE", scale=1.0):
        size = int(TILE_SIZE * scale)
        super().__init__(x, y, size, size)
        self.direction = direction
        self.style = style  # 'BLUE', 'WHITE_STAR', 'DARK'

    @property
    def hitbox(self):
        """Hitbox thu nhỏ ở phần lõi gai giúp trải nghiệm nhảy chuẩn xác, không bị ức chế."""
        pad_x = int(self.w * 0.32)
        pad_y = int(self.h * 0.30)
        return pygame.Rect(
            int(self.x + pad_x),
            int(self.y + pad_y),
            max(6, self.w - pad_x * 2),
            max(6, self.h - pad_y * 2),
        )

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx = int(self.x - camera_x)
        sy = int(self.y)
        w, h = self.w, self.h

        # Xác định 3 đỉnh tam giác theo hướng của gai
        if self.direction == "UP":
            pts = [(sx, sy + h), (sx + w // 2, sy + 4), (sx + w, sy + h)]
            tip = (sx + w // 2, sy + 2)
        elif self.direction == "DOWN":
            pts = [(sx, sy), (sx + w // 2, sy + h - 4), (sx + w, sy)]
            tip = (sx + w // 2, sy + h - 2)
        elif self.direction == "LEFT":
            pts = [(sx + w, sy + 6), (sx + 6, sy + h // 2), (sx + w, sy + h - 6)]
            tip = (sx + 4, sy + h // 2)
        else:  # RIGHT
            pts = [(sx, sy + 6), (sx + w - 6, sy + h // 2), (sx, sy + h - 6)]
            tip = (sx + w - 4, sy + h // 2)

        # Chọn bảng màu theo style
        if self.style == "WHITE_STAR":
            fill_col = (235, 240, 255)
            border_col = (160, 175, 210)
        elif self.style == "BLUE":
            fill_col = (10, 165, 255)
            border_col = (80, 220, 255)
        else:
            fill_col = (20, 10, 35)
            border_col = (200, 70, 255)

        pygame.draw.polygon(surface, fill_col, pts)
        pygame.draw.polygon(surface, border_col, pts, 2)

        # Nếu là gai trắng treo dưới đáy trụ (như hình mẫu 3), vẽ thêm ngôi sao 4 cánh ở đỉnh nhọn
        if self.style == "WHITE_STAR":
            tx, ty = tip
            pygame.draw.line(surface, WHITE, (tx - 5, ty), (tx + 5, ty), 2)
            pygame.draw.line(surface, WHITE, (tx, ty - 5), (tx, ty + 5), 2)


class Orb(GameObject):
    """
    Vòng tròn tương tác trên không:
    - 'PURPLE_RING': Vòng nhẫn tím giúp bật nhảy khi người chơi bấm phím lúc chạm vòng
    - 'CYAN_ORB': Quả cầu xanh cyan phát sáng có các chấm tím xoay xung quanh
    """

    def __init__(self, x, y, orb_type="PURPLE_RING"):
        super().__init__(x - 24, y - 24, 48, 48)
        self.orb_type = orb_type
        self.activated = False
        self.anim_timer = 0.0

    def update(self, dt):
        self.anim_timer += dt

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        cx = int(self.x - camera_x + self.w // 2)
        cy = int(self.y + self.h // 2)
        pulse = math.sin(self.anim_timer * 7.0) * 2.5

        if self.orb_type == "PURPLE_RING":
            # Vòng tròn tím dưới chân nhân vật (Hình mẫu 3)
            DrawUtils.draw_glow_circle(surface, (180, 30, 255), (cx, cy), int(20 + pulse), glow_layers=3)
            pygame.draw.circle(surface, (165, 20, 245), (cx, cy), int(16 + pulse * 0.5), 5)
            pygame.draw.circle(surface, (230, 140, 255), (cx, cy), int(16 + pulse * 0.5), 2)
        elif self.orb_type == "CYAN_ORB":
            # Quả cầu Cyan phát sáng kèm 4 hạt vệ tinh màu tím xoay quanh (Hình mẫu 3)
            DrawUtils.draw_glow_circle(surface, CYAN_LIGHT, (cx, cy), int(30 + pulse), glow_layers=4)
            # Vòng tròn tím phía ngoài
            pygame.draw.circle(surface, (140, 40, 235), (cx, cy), 24, 3)
            for i in range(4):
                angle = self.anim_timer * 3.2 + i * (math.pi / 2)
                ox = cx + int(math.cos(angle) * 25)
                oy = cy + int(math.sin(angle) * 25)
                pygame.draw.circle(surface, (165, 50, 255), (ox, oy), 6)

            # Lõi xanh Cyan phát sáng
            pygame.draw.circle(surface, WHITE, (cx, cy), 19)
            pygame.draw.circle(surface, CYAN_LIGHT, (cx, cy), 15)
            pygame.draw.circle(surface, (180, 255, 255), (cx, cy), 9)


class Portal(GameObject):
    """Cổng chuyển đổi trạng thái nhân vật giữa CUBE và WAVE."""

    def __init__(self, x, y, target_mode=MODE_WAVE):
        super().__init__(x, y, 56, 150)
        self.target_mode = target_mode
        self.timer = 0.0
        self.triggered = False

    def update(self, dt):
        self.timer += dt

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return
        sx = int(self.x - camera_x)
        sy = int(self.y)
        cx = sx + self.w // 2
        cy = sy + self.h // 2

        color = CYAN_LIGHT if self.target_mode == MODE_WAVE else BLOCK_ORANGE
        DrawUtils.draw_glow_circle(surface, color, (cx, cy), 65, glow_layers=4)

        # Vẽ khung cổng elip đôi
        rect_outer = pygame.Rect(sx, sy, self.w, self.h)
        rect_inner = pygame.Rect(sx + 10, sy + 16, self.w - 20, self.h - 32)
        pygame.draw.ellipse(surface, color, rect_outer, 6)
        pygame.draw.ellipse(surface, WHITE, rect_inner, 4)


class WaveCorridor(GameObject):
    """
    Hành lang zíc-zắc chế độ Wave (Tái hiện chính xác Hình mẫu 4):
    - Tường gạch tím/đỏ phía trên và phía dưới
    - Đường viền laser màu cam-đỏ phát sáng rực rỡ dọc theo mép zíc-zắc
    - Các chấm tròn màu hồng dẫn đường ở chính giữa hành lang
    """

    def __init__(self, start_x, end_x, top_vertices, bottom_vertices, guide_dots):
        super().__init__(start_x, 0, end_x - start_x, SCREEN_HEIGHT)
        self.start_x = start_x
        self.end_x = end_x
        self.top_vertices = top_vertices        # Danh sách điểm (x, y) của trần zíc-zắc
        self.bottom_vertices = bottom_vertices  # Danh sách điểm (x, y) của sàn zíc-zắc
        self.guide_dots = guide_dots            # Danh sách điểm (x, y) của các chấm tròn hồng

        # Tạo mẫu gạch (Brick Pattern Tile) để lát lên trần và sàn Wave
        self.brick_tile = self._create_brick_tile()

    def _create_brick_tile(self):
        w, h = 64, 32
        tile = pygame.Surface((w, h))
        tile.fill((52, 6, 75))
        # Vẽ 2 hàng gạch so le
        pygame.draw.rect(tile, (82, 12, 110), (2, 2, 28, 12), border_radius=2)
        pygame.draw.rect(tile, (72, 10, 98), (34, 2, 28, 12), border_radius=2)
        pygame.draw.rect(tile, (75, 10, 102), (18, 18, 28, 12), border_radius=2)
        pygame.draw.rect(tile, (85, 14, 115), (50, 18, 14, 12), border_radius=2)
        pygame.draw.rect(tile, (85, 14, 115), (0, 18, 14, 12), border_radius=2)
        # Viền mạch gạch tối màu
        pygame.draw.line(tile, (25, 2, 40), (0, 0), (w, 0), 2)
        pygame.draw.line(tile, (25, 2, 40), (0, 16), (w, 16), 2)
        return tile

    def check_collision(self, player_rect):
        """Kiểm tra mũi tên Wave có chạm vào trần hoặc sàn zíc-zắc không."""
        px = player_rect.centerx
        if px < self.start_x or px > self.end_x:
            return False

        # Nội suy tuyến tính chiều cao trần (top_y) tại vị trí px
        top_y = 0
        for i in range(len(self.top_vertices) - 1):
            x1, y1 = self.top_vertices[i]
            x2, y2 = self.top_vertices[i + 1]
            if x1 <= px <= x2:
                t = (px - x1) / max(1.0, (x2 - x1))
                top_y = y1 + t * (y2 - y1)
                break

        # Nội suy tuyến tính chiều cao sàn (bot_y) tại vị trí px
        bot_y = SCREEN_HEIGHT
        for i in range(len(self.bottom_vertices) - 1):
            x1, y1 = self.bottom_vertices[i]
            x2, y2 = self.bottom_vertices[i + 1]
            if x1 <= px <= x2:
                t = (px - x1) / max(1.0, (x2 - x1))
                bot_y = y1 + t * (y2 - y1)
                break

        # Khoảng đệm an toàn 8px quanh tâm mũi tên
        if player_rect.top + 6 <= top_y or player_rect.bottom - 6 >= bot_y:
            return True
        return False

    def draw(self, surface, camera_x):
        if not self.is_visible(camera_x):
            return

        # Lọc các đoạn nằm gần vùng nhìn của Camera để vẽ nhanh
        vis_top = [(int(x - camera_x), int(y)) for x, y in self.top_vertices if -250 <= x - camera_x <= SCREEN_WIDTH + 250]
        vis_bot = [(int(x - camera_x), int(y)) for x, y in self.bottom_vertices if -250 <= x - camera_x <= SCREEN_WIDTH + 250]

        if len(vis_top) < 2 or len(vis_bot) < 2:
            return

        # 1. Vẽ khối đa giác tường gạch phía trên và phía dưới
        top_poly = [(vis_top[0][0], 0)] + vis_top + [(vis_top[-1][0], 0)]
        bot_poly = [(vis_bot[0][0], SCREEN_HEIGHT)] + vis_bot + [(vis_bot[-1][0], SCREEN_HEIGHT)]

        # Tạo mặt nạ cắt gạch (Polygon Masking) giúp tường gạch hiển thị đúng hình răng cưa
        wall_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(wall_surf, (68, 10, 95, 255), top_poly)
        pygame.draw.polygon(wall_surf, (68, 10, 95, 255), bot_poly)

        # Vẽ vân gạch ngang lên tường
        brick_off_x = int(camera_x) % 64
        for y in range(0, SCREEN_HEIGHT, 32):
            pygame.draw.line(wall_surf, (30, 3, 45, 255), (0, y), (SCREEN_WIDTH, y), 3)
            row_shift = 32 if (y // 32) % 2 == 1 else 0
            for x in range(-brick_off_x + row_shift, SCREEN_WIDTH, 64):
                pygame.draw.line(wall_surf, (30, 3, 45, 255), (x, y), (x, y + 32), 3)

        # Cắt bỏ phần lòng đường hầm ở giữa để lộ nền đỏ tím phía sau
        corridor_poly = vis_top + list(reversed(vis_bot))
        pygame.draw.polygon(wall_surf, (0, 0, 0, 0), corridor_poly)
        surface.blit(wall_surf, (0, 0))

        # 2. Vẽ các chấm tròn màu hồng dẫn đường ở giữa hành lang (Hình mẫu 4)
        for gx, gy in self.guide_dots:
            sx = int(gx - camera_x)
            if -30 <= sx <= SCREEN_WIDTH + 30:
                DrawUtils.draw_glow_circle(surface, (255, 20, 140), (sx, int(gy)), 13, glow_layers=2)
                pygame.draw.circle(surface, (255, 45, 160), (sx, int(gy)), 9)

        # 3. Vẽ đường viền laser Cam-Đỏ Neon phát sáng dọc theo mép zíc-zắc
        glow_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_RED, 85), False, vis_top, 22)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_ORANGE, 160), False, vis_top, 12)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_RED, 85), False, vis_bot, 22)
        pygame.draw.lines(glow_overlay, (*WAVE_NEON_ORANGE, 160), False, vis_bot, 12)
        surface.blit(glow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Lõi vàng-trắng rực sáng ở tâm đường kẻ
        pygame.draw.lines(surface, WAVE_NEON_ORANGE, False, vis_top, 6)
        pygame.draw.lines(surface, (255, 240, 150), False, vis_top, 3)
        pygame.draw.lines(surface, WAVE_NEON_ORANGE, False, vis_bot, 6)
        pygame.draw.lines(surface, (255, 240, 150), False, vis_bot, 3)


class Player:
    """
    Lớp Nhân vật chính (Player):
    - Chế độ CUBE: Khối vuông hồng viền vàng có biểu cảm đáng yêu (Hình mẫu 3)
    - Chế độ WAVE: Mũi tên tím bay zíc-zắc 45 độ kèm vòng xung nhịp hồng (Hình mẫu 4)
    """

    def __init__(self, start_x, start_y):
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.w = 46
        self.h = 46
        self.cube_surf = self._bake_cute_cube()
        self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel_y = 0.0
        self.angle = 0.0
        self.mode = MODE_CUBE
        self.on_ground = False
        self.is_dead = False
        self.victory = False
        self.pulse_timer = 0.0

    def _bake_cute_cube(self):
        """Vẽ sẵn nhân vật khối vuông hồng viền vàng có khuôn mặt Kawaii giống Hình mẫu 3."""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        # Viền đen ngoài cùng
        pygame.draw.rect(surf, BLACK, (0, 0, self.w, self.h), border_radius=6)
        # Viền vàng rực rỡ
        pygame.draw.rect(surf, PLAYER_YELLOW, (2, 2, self.w - 4, self.h - 4), border_radius=5)
        # Thân màu hồng đậm
        pygame.draw.rect(surf, PLAYER_PINK, (6, 6, self.w - 12, self.h - 12), border_radius=4)
        # Điểm nhấn полу-tròn màu cam hồng ở cạnh dưới
        pygame.draw.ellipse(surf, (255, 130, 90), (11, self.h - 16, self.w - 22, 12))

        # Đôi mắt đen to tròn + đốm sáng trắng
        pygame.draw.circle(surf, BLACK, (14, 19), 4)
        pygame.draw.circle(surf, WHITE, (13, 18), 1)
        pygame.draw.circle(surf, BLACK, (self.w - 14, 19), 4)
        pygame.draw.circle(surf, WHITE, (self.w - 15, 18), 1)

        # Miệng cười nhỏ nhắn nằm giữa 2 mắt
        pygame.draw.arc(surf, BLACK, (19, 17, 8, 7), math.pi, math.tau, 2)
        return surf

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, is_holding, just_pressed, blocks, orbs, portals, corridors, wave_trail, particles):
        if self.is_dead or self.victory:
            return

        self.pulse_timer += dt
        prev_bottom = self.y + self.h

        # Dịch chuyển ngang theo tốc độ màn chơi
        self.x += SCROLL_SPEED * dt

        # --- XỬ LÝ VẬT LÝ THEO CHẾ ĐỘ ---
        if self.mode == MODE_CUBE:
            # Kiểm tra bấm kích hoạt Orb trên không
            if is_holding:
                for orb in orbs:
                    if not orb.activated and self.rect.colliderect(orb.rect):
                        if just_pressed or not self.on_ground:
                            orb.activated = True
                            self.vel_y = ORB_JUMP_VEL
                            self.on_ground = False
                            particles.spawn_explosion(orb.x + 24, orb.y + 24, CYAN_LIGHT, count=15)
                            break

            # Nhảy tự động khi đang chạm đất và giữ phím
            if self.on_ground and is_holding:
                self.vel_y = CUBE_JUMP_VEL
                self.on_ground = False

            # Áp dụng trọng lực
            self.vel_y += CUBE_GRAVITY * dt
            self.y += self.vel_y * dt

            # Va chạm với mặt đất chuẩn
            self.on_ground = False
            if self.y + self.h >= GROUND_Y:
                self.y = GROUND_Y - self.h
                self.vel_y = 0.0
                self.on_ground = True

            # Va chạm với các khối Block
            player_r = self.rect
            for blk in blocks:
                if not blk.is_visible(self.x - 260):
                    continue
                if player_r.colliderect(blk.rect):
                    # Nếu rơi từ trên xuống chạm mặt trên của Block -> Đứng lên Block
                    if prev_bottom <= blk.rect.top + 16 and self.vel_y >= 0:
                        self.y = blk.rect.top - self.h
                        self.vel_y = 0.0
                        self.on_ground = True
                        player_r = self.rect
                    else:
                        # Đâm ngang hông hoặc cụng đầu vào đáy Block -> Nổ tung!
                        self.is_dead = True
                        return

            # Xoay góc Cube: đang bay thì xoay tròn, chạm đất thì tự làm tròn về bội số của 90 độ
            if not self.on_ground:
                self.angle = (self.angle - 380.0 * dt) % 360.0
            else:
                target_angle = round(self.angle / 90.0) * 90.0
                self.angle += (target_angle - self.angle) * min(1.0, dt * 22.0)
                if int(self.x) % 3 == 0:
                    particles.spawn_trail(self.x + 6, self.y + self.h - 4, PLAYER_PINK)

        elif self.mode == MODE_WAVE:
            # Chế độ Wave: giữ phím bay chéo lên (-45°), nhả phím lao chéo xuống (+45°)
            self.vel_y = -WAVE_SPEED_Y if is_holding else WAVE_SPEED_Y
            self.y += self.vel_y * dt
            self.angle = 35.0 if is_holding else -35.0

            # Lưu tọa độ tâm mũi tên vào WaveTrail để vẽ đường laser hồng zíc-zắc
            wave_trail.add_point(self.x + self.w // 2, self.y + self.h // 2)

            # Kiểm tra va chạm với trần và sàn đường hầm Wave
            for cor in corridors:
                if cor.check_collision(self.rect):
                    self.is_dead = True
                    return

        # --- KIỂM TRA CHẠM CỔNG CHUYỂN CHẾ ĐỘ (PORTAL) ---
        for portal in portals:
            if not portal.triggered and self.rect.colliderect(portal.rect):
                portal.triggered = True
                self.mode = portal.target_mode
                self.vel_y = 0.0
                if self.mode == MODE_WAVE:
                    wave_trail.clear()
                    wave_trail.add_point(self.x + self.w // 2, self.y + self.h // 2)
                particles.spawn_explosion(self.x + self.w // 2, self.y + self.h // 2, CYAN_LIGHT, count=25)

    def draw(self, surface, camera_x):
        if self.is_dead:
            return

        sx = int(self.x - camera_x)
        sy = int(self.y)
        cx = sx + self.w // 2
        cy = sy + self.h // 2

        if self.mode == MODE_CUBE:
            rotated = pygame.transform.rotate(self.cube_surf, self.angle)
            rot_rect = rotated.get_rect(center=(cx, cy))
            surface.blit(rotated, rot_rect.topleft)

        elif self.mode == MODE_WAVE:
            # Vẽ vòng tròn xung nhịp màu hồng tím phía sau mũi tên (giống Hình mẫu 4)
            ring_r = int(28 + math.sin(self.pulse_timer * 10.0) * 6)
            pygame.draw.circle(surface, WAVE_TRAIL_PINK, (cx - 18, cy + 12), ring_r, 2)

            # Tạo hình mũi tên Wave (Phi tiêu tím viền trắng sắc nét)
            dart_surf = pygame.Surface((52, 52), pygame.SRCALPHA)
            pts = [(48, 26), (8, 8), (18, 26), (8, 44)]
            pygame.draw.polygon(dart_surf, WAVE_PLAYER_PURPLE, pts)
            pygame.draw.polygon(dart_surf, WHITE, pts, 3)

            rotated_dart = pygame.transform.rotate(dart_surf, self.angle)
            rot_rect = rotated_dart.get_rect(center=(cx, cy))
            surface.blit(rotated_dart, rot_rect.topleft)