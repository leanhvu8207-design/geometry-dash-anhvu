# ui.py
import math
import pygame
from config import *
from vfx import DrawUtils


class AudioSlider:
    """Thanh trượt âm lượng tương tác cho Nhạc nền (♪) và Hiệu ứng (Loa)."""

    def __init__(self, x, y, width, height, icon_type="music", initial_val=1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.icon_type = icon_type
        self.value = max(0.0, min(1.0, float(initial_val)))
        self.dragging = False
        self.knob_radius = 19

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            knob_x = self.rect.x + int(self.value * self.rect.w)
            knob_y = self.rect.centery
            if math.hypot(mx - knob_x, my - knob_y) <= self.knob_radius + 6 or self.rect.inflate(10, 16).collidepoint(mx, my):
                self.dragging = True
                self._update_val(mx)
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val(event.pos[0])
            return True
        return False

    def _update_val(self, mouse_x):
        rel = (mouse_x - self.rect.x) / float(self.rect.w)
        self.value = max(0.0, min(1.0, rel))

    def draw(self, surface):
        ix = self.rect.x - 42
        iy = self.rect.centery
        if self.icon_type == "music":
            pygame.draw.circle(surface, WHITE, (ix - 6, iy + 8), 6)
            pygame.draw.circle(surface, WHITE, (ix + 10, iy + 6), 6)
            pygame.draw.line(surface, WHITE, (ix - 2, iy + 8), (ix - 2, iy - 12), 4)
            pygame.draw.line(surface, WHITE, (ix + 14, iy + 6), (ix + 14, iy - 14), 4)
            pygame.draw.line(surface, WHITE, (ix - 2, iy - 11), (ix + 14, iy - 13), 5)
        else:
            pts = [(ix - 12, iy - 5), (ix - 4, iy - 5), (ix + 5, iy - 13), (ix + 5, iy + 13), (ix - 4, iy + 5), (ix - 12, iy + 5)]
            pygame.draw.polygon(surface, WHITE, pts)
            pygame.draw.arc(surface, WHITE, (ix + 2, iy - 9, 12, 18), -math.pi / 3, math.pi / 3, 2)
            pygame.draw.arc(surface, WHITE, (ix + 5, iy - 14, 16, 28), -math.pi / 3, math.pi / 3, 2)

        pygame.draw.rect(surface, (15, 25, 45), self.rect, border_radius=8)

        fill_w = int(self.rect.w * self.value)
        if fill_w > 6:
            fill_surf = pygame.Surface((fill_w, self.rect.h), pygame.SRCALPHA)
            pygame.draw.rect(fill_surf, (0, 175, 240), (0, 0, fill_w, self.rect.h), border_radius=7)
            for sx in range(-20, fill_w + 20, 18):
                pygame.draw.line(fill_surf, (60, 225, 255), (sx, self.rect.h), (sx + 12, 0), 5)
            surface.blit(fill_surf, self.rect.topleft)

        pygame.draw.rect(surface, (215, 175, 35), self.rect, 3, border_radius=8)

        knob_x = self.rect.x + fill_w
        knob_y = self.rect.centery
        pygame.draw.circle(surface, BLACK, (knob_x, knob_y), self.knob_radius + 2)
        pygame.draw.circle(surface, (230, 190, 45), (knob_x, knob_y), self.knob_radius)
        pygame.draw.circle(surface, (165, 130, 20), (knob_x, knob_y), self.knob_radius - 4)
        pygame.draw.circle(surface, (245, 215, 90), (knob_x - 3, knob_y - 3), 4)


class MainMenuUI:
    """Giao diện Màn hình chính với 3 huy hiệu: Lê Anh Vũ, Gemini Argon 4 và Thái tử."""

    def __init__(self):
        self.font_logo = pygame.font.SysFont("impact", 76)
        self.font_try = pygame.font.SysFont("arialblack", 30, italic=True)
        self.font_robtop = pygame.font.SysFont("arialblack", 38)
        # Sử dụng Segoe UI / Arial hỗ trợ hiển thị tiếng Việt có dấu sắc nét
        self.font_badge_small = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_badge_big = pygame.font.SysFont("segoeui", 19, bold=True)
        self.font_copy = pygame.font.SysFont("segoeui", 14)

        self.play_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT // 2 - 70, 190, 190)
        self.fullscreen_rect = pygame.Rect(20, 18, 36, 36)
        self.anim_timer = 0.0

    def update(self, dt):
        self.anim_timer += dt

    def handle_click(self, pos):
        if self.play_btn_rect.collidepoint(pos):
            return "PLAY"
        if self.fullscreen_rect.collidepoint(pos):
            return "FULLSCREEN"
        return None

    def _draw_fullscreen_icon(self, surface, rect):
        x, y, w, h = rect
        c = (120, 180, 255)
        l = 9
        pygame.draw.lines(surface, c, False, [(x, y + l), (x, y), (x + l, y)], 3)
        pygame.draw.lines(surface, c, False, [(x + w - l, y), (x + w, y), (x + w, y + l)], 3)
        pygame.draw.lines(surface, c, False, [(x, y + h - l), (x, y + h), (x + l, y + h)], 3)
        pygame.draw.lines(surface, c, False, [(x + w - l, y + h), (x + w, y + h), (x + w, y + h - l)], 3)

    def _draw_center_play_button(self, surface, mouse_pos):
        is_hover = self.play_btn_rect.collidepoint(mouse_pos)
        scale = 1.06 if is_hover else 1.0 + math.sin(self.anim_timer * 3.5) * 0.02

        cx, cy = self.play_btn_rect.center
        size = int(176 * scale)
        half = size // 2
        arm = int(size * 0.36)

        for i in range(6):
            ang = self.anim_timer * 1.2 + i * 1.05
            px = cx + int(math.cos(ang) * (half + 18))
            py = cy + int(math.sin(ang * 1.5) * (half - 10))
            pygame.draw.rect(surface, (40, 160, 255), (px - 4, py - 4, 8, 8))

        sq_size = int(size * 0.80)
        sq_rect = pygame.Rect(cx - sq_size // 2, cy - sq_size // 2, sq_size, sq_size)
        pygame.draw.rect(surface, WHITE, sq_rect.inflate(12, 12), border_radius=8)
        pygame.draw.rect(surface, BLACK, sq_rect.inflate(6, 6), border_radius=6)
        pygame.draw.rect(surface, CYAN_DARK, sq_rect, border_radius=4)
        pygame.draw.rect(surface, CYAN_LIGHT, sq_rect.inflate(-12, -12), border_radius=4)

        v_rect = pygame.Rect(cx - arm, cy - half, arm * 2, size)
        h_rect = pygame.Rect(cx - half, cy - arm, size, arm * 2)

        for r in (v_rect, h_rect):
            pygame.draw.rect(surface, WHITE, r.inflate(12, 12), border_radius=10)
            pygame.draw.rect(surface, BLACK, r.inflate(6, 6), border_radius=8)

        for r in (v_rect, h_rect):
            pygame.draw.rect(surface, LOGO_GREEN_BOT, r, border_radius=6)
            top_half = pygame.Rect(r.x + 4, r.y + 4, r.w - 8, r.h // 2)
            pygame.draw.rect(surface, LOGO_GREEN_TOP, top_half, border_radius=4)

        pygame.draw.rect(surface, BLACK, v_rect, 4, border_radius=6)
        pygame.draw.rect(surface, BLACK, h_rect, 4, border_radius=6)

        tri_r = int(size * 0.27)
        tri_pts = [
            (cx - int(tri_r * 0.65), cy - int(tri_r * 0.85)),
            (cx - int(tri_r * 0.65), cy + int(tri_r * 0.85)),
            (cx + int(tri_r * 0.95), cy),
        ]
        pygame.draw.polygon(surface, GOLD_YELLOW, tri_pts)
        pygame.draw.polygon(surface, (45, 75, 10), tri_pts, 5)

    def _draw_custom_badge(self, surface, x, y, w, h, top_text, main_text, badge_style):
        """Vẽ 3 huy hiệu danh tính: Lê Anh Vũ, Gemini Argon 4 và Thái tử."""
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, BLACK, rect, border_radius=10)
        pygame.draw.rect(surface, (215, 225, 245), rect, 2, border_radius=10)

        ic_x = x + 26
        ic_y = y + h // 2

        if badge_style == "AUTHOR":
            # Biểu tượng Ngôi sao vàng 4 cánh & Khối Cube Neon cho Lê Anh Vũ
            pygame.draw.rect(surface, PLAYER_PINK, (ic_x - 11, ic_y - 11, 22, 22), border_radius=4)
            pygame.draw.rect(surface, GOLD_YELLOW, (ic_x - 11, ic_y - 11, 22, 22), 2, border_radius=4)
            pygame.draw.circle(surface, WHITE, (ic_x - 4, ic_y - 2), 2)
            pygame.draw.circle(surface, WHITE, (ic_x + 4, ic_y - 2), 2)
        elif badge_style == "GEMINI":
            # Biểu tượng Kim cương lấp lánh AI Cyan cho Gemini Argon 4
            pts = [(ic_x, ic_y - 14), (ic_x + 13, ic_y), (ic_x, ic_y + 14), (ic_x - 13, ic_y)]
            pygame.draw.polygon(surface, CYAN_LIGHT, pts)
            pygame.draw.polygon(surface, WHITE, pts, 2)
            pygame.draw.circle(surface, WHITE, (ic_x, ic_y), 4)
        elif badge_style == "PRINCE":
            # Biểu tượng Vương miện Hoàng gia Vàng cho Thái tử
            crown_pts = [
                (ic_x - 13, ic_y + 9),
                (ic_x - 13, ic_y - 7),
                (ic_x - 6, ic_y + 1),
                (ic_x, ic_y - 11),
                (ic_x + 6, ic_y + 1),
                (ic_x + 13, ic_y - 7),
                (ic_x + 13, ic_y + 9),
            ]
            pygame.draw.polygon(surface, GOLD_YELLOW, crown_pts)
            pygame.draw.polygon(surface, WHITE, crown_pts, 2)

        t1 = self.font_badge_small.render(top_text, True, (180, 210, 255))
        t2 = self.font_badge_big.render(main_text, True, WHITE)
        surface.blit(t1, (x + 48, y + 7))
        surface.blit(t2, (x + 48, y + 22))

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        self._draw_fullscreen_icon(surface, self.fullscreen_rect)
        info_center = (SCREEN_WIDTH - 34, 34)
        pygame.draw.circle(surface, BLACK, info_center, 18)
        pygame.draw.circle(surface, (20, 140, 255), info_center, 16)
        DrawUtils.draw_outlined_text(surface, "i", self.font_badge_big, info_center, WHITE, BLACK, 2)

        title_y = 115
        DrawUtils.draw_outlined_text(surface, "GEOMETRY  DASH", self.font_logo, (SCREEN_WIDTH // 2, title_y), WHITE, WHITE, 7)
        DrawUtils.draw_outlined_text(surface, "GEOMETRY  DASH", self.font_logo, (SCREEN_WIDTH // 2, title_y), LOGO_GREEN_TOP, BLACK, 4)
        DrawUtils.draw_outlined_text(surface, "TRY ME!", self.font_try, (SCREEN_WIDTH // 2 + 195, title_y + 72), GOLD_YELLOW, BLACK, 3)

        self._draw_center_play_button(surface, mouse_pos)

        rob_rect = pygame.Rect(48, SCREEN_HEIGHT - 102, 265, 64)
        pygame.draw.rect(surface, GOLD_ORANGE, rob_rect.inflate(10, 10), border_radius=20)
        pygame.draw.rect(surface, GOLD_YELLOW, rob_rect, border_radius=16)
        DrawUtils.draw_outlined_text(surface, "ROBTOP", self.font_robtop, rob_rect.center, GOLD_YELLOW, BLACK, 5)

        # Bộ 3 huy hiệu mới thay thế hoàn toàn App Store, Google Play và Steam
        badge_y = SCREEN_HEIGHT - 96
        self._draw_custom_badge(surface, 540, badge_y, 220, 56, "CREATED BY", "Lê Anh Vũ", "AUTHOR")
        self._draw_custom_badge(surface, 780, badge_y, 235, 56, "POWERED BY", "Gemini Argon 4", "GEMINI")
        self._draw_custom_badge(surface, 1035, badge_y, 200, 56, "VIP EDITION", "Thái tử", "PRINCE")

        copy_surf = self.font_copy.render("© 2026 Lê Anh Vũ · Thái tử Edition", True, (110, 150, 215))
        surface.blit(copy_surf, (SCREEN_WIDTH - copy_surf.get_width() - 24, SCREEN_HEIGHT - 26))


class PauseMenuUI:
    """Giao diện Tạm dừng hiển thị chính xác phần trăm tiến độ cao nhất (Best Progress) của người chơi."""

    def __init__(self):
        self.font_title = pygame.font.SysFont("arialblack", 42)
        self.font_mode = pygame.font.SysFont("arialblack", 24)
        self.font_pct = pygame.font.SysFont("arialblack", 22)
        self.font_attempt = pygame.font.SysFont("arialblack", 52)

        cy = 368
        self.replay_center = (452, cy)
        self.replay_radius = 58

        self.play_center = (648, cy)
        self.play_radius = 78

        self.menu_center = (844, cy)
        self.menu_radius = 58

        self.fullscreen_rect = pygame.Rect(65, 52, 34, 34)

        slider_y = 555
        self.music_slider = AudioSlider(265, slider_y - 8, 325, 16, icon_type="music", initial_val=0.92)
        self.sfx_slider = AudioSlider(710, slider_y - 8, 325, 16, icon_type="sfx", initial_val=0.92)

    def handle_event(self, event):
        if self.music_slider.handle_event(event):
            return "VOLUME_CHANGED"
        if self.sfx_slider.handle_event(event):
            return "VOLUME_CHANGED"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if math.hypot(mx - self.play_center[0], my - self.play_center[1]) <= self.play_radius:
                return "RESUME"
            if math.hypot(mx - self.replay_center[0], my - self.replay_center[1]) <= self.replay_radius:
                return "REPLAY"
            if math.hypot(mx - self.menu_center[0], my - self.menu_center[1]) <= self.menu_radius:
                return "MENU"
            if self.fullscreen_rect.collidepoint(mx, my):
                return "FULLSCREEN"
        return None

    def _draw_green_circle_btn(self, surface, center, radius, hover=False):
        r = int(radius * (1.06 if hover else 1.0))
        cx, cy = center
        pygame.draw.circle(surface, BLACK, (cx, cy + 3), r + 6)
        pygame.draw.circle(surface, WHITE, (cx, cy), r + 4)
        pygame.draw.circle(surface, BLACK, (cx, cy), r)
        pygame.draw.circle(surface, LOGO_GREEN_BOT, (cx, cy), r - 4)

        hi_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(hi_surf, (*LOGO_GREEN_TOP, 210), (10, 6, (r - 5) * 2, int(r * 1.15)))
        surface.blit(hi_surf, (cx - r, cy - r))

    def draw(self, surface, best_pct, attempt_count):
        mouse_pos = pygame.mouse.get_pos()

        DrawUtils.draw_outlined_text(surface, f"T  {attempt_count}", self.font_attempt, (55, 175), (185, 195, 205), BLACK, 4)

        cube_rect = pygame.Rect(450, 448, 62, 62)
        pygame.draw.rect(surface, BLACK, cube_rect, border_radius=4)
        pygame.draw.rect(surface, (15, 110, 20), cube_rect.inflate(-6, -6), border_radius=3)
        pygame.draw.rect(surface, (10, 140, 155), (460, 460, 12, 10))
        pygame.draw.rect(surface, (10, 140, 155), (488, 460, 12, 10))
        pygame.draw.rect(surface, (10, 140, 155), (460, 482, 40, 10))

        spk_pts = [(795, 512), (828, 448), (861, 512)]
        pygame.draw.polygon(surface, (35, 45, 65), spk_pts)
        pygame.draw.polygon(surface, BLACK, [(802, 510), (828, 456), (854, 510)])

        panel_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel_rect = pygame.Rect(36, 22, SCREEN_WIDTH - 72, SCREEN_HEIGHT - 44)
        pygame.draw.rect(panel_surf, (2, 8, 22, 185), panel_rect, border_radius=42)
        surface.blit(panel_surf, (0, 0))

        x, y, w, h = self.fullscreen_rect
        l = 8
        for pts in [
            [(x, y + l), (x, y), (x + l, y)],
            [(x + w - l, y), (x + w, y), (x + w, y + l)],
            [(x, y + h - l), (x, y + h), (x + l, y + h)],
            [(x + w - l, y + h), (x + w, y + h), (x + w, y + h - l)],
        ]:
            pygame.draw.lines(surface, (220, 230, 245), False, pts, 3)

        DrawUtils.draw_outlined_text(surface, "STEREO  MADNESS", self.font_title, (SCREEN_WIDTH // 2, 72), WHITE, BLACK, 4)
        DrawUtils.draw_outlined_text(surface, "NORMAL  MODE", self.font_mode, (SCREEN_WIDTH // 2, 145), WHITE, BLACK, 3)

        # Thanh tiến độ hiển thị đúng kỷ lục cao nhất (best_pct) người chơi đạt được
        bar_w, bar_h = 756, 42
        bar_x = (SCREEN_WIDTH - bar_w) // 2
        bar_y = 168
        bar_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
        pygame.draw.rect(surface, (4, 10, 22), bar_rect, border_radius=21)

        clamped_pct = max(0, min(100, best_pct))
        if clamped_pct > 0:
            fill_w = max(28, int(bar_w * (clamped_pct / 100.0)))
            fill_rect = pygame.Rect(bar_x, bar_y, fill_w, bar_h)
            pygame.draw.rect(surface, PROGRESS_GREEN, fill_rect, border_radius=21)

        DrawUtils.draw_outlined_text(surface, f"{clamped_pct}%", self.font_pct, bar_rect.center, WHITE, BLACK, 3)

        rep_hover = math.hypot(mouse_pos[0] - self.replay_center[0], mouse_pos[1] - self.replay_center[1]) <= self.replay_radius
        self._draw_green_circle_btn(surface, self.replay_center, self.replay_radius, rep_hover)
        rcx, rcy = self.replay_center
        arc_rect = pygame.Rect(rcx - 28, rcy - 28, 56, 56)
        pygame.draw.arc(surface, BLACK, arc_rect.inflate(6, 6), 0.4, math.tau - 0.5, 15)
        pygame.draw.arc(surface, CYAN_LIGHT, arc_rect, 0.4, math.tau - 0.5, 11)
        arrow_pts = [(rcx + 12, rcy - 2), (rcx + 34, rcy - 8), (rcx + 26, rcy + 16)]
        pygame.draw.polygon(surface, BLACK, [(p[0] + 2, p[1] + 2) for p in arrow_pts])
        pygame.draw.polygon(surface, CYAN_LIGHT, arrow_pts)

        play_hover = math.hypot(mouse_pos[0] - self.play_center[0], mouse_pos[1] - self.play_center[1]) <= self.play_radius
        self._draw_green_circle_btn(surface, self.play_center, self.play_radius, play_hover)
        pcx, pcy = self.play_center
        tri_pts = [(pcx - 24, pcy - 38), (pcx - 24, pcy + 38), (pcx + 42, pcy)]
        pygame.draw.polygon(surface, BLACK, [(p[0] + 3, p[1] + 3) for p in tri_pts])
        pygame.draw.polygon(surface, GOLD_YELLOW, tri_pts)
        pygame.draw.polygon(surface, BLACK, tri_pts, 4)

        menu_hover = math.hypot(mouse_pos[0] - self.menu_center[0], mouse_pos[1] - self.menu_center[1]) <= self.menu_radius
        self._draw_green_circle_btn(surface, self.menu_center, self.menu_radius, menu_hover)
        mcx, mcy = self.menu_center
        for offset_y in [-18, 0, 18]:
            y_pos = mcy + offset_y
            pygame.draw.circle(surface, BLACK, (mcx - 24, y_pos), 8)
            pygame.draw.circle(surface, CYAN_LIGHT, (mcx - 24, y_pos), 6)
            bar_r = pygame.Rect(mcx - 10, y_pos - 6, 40, 12)
            pygame.draw.rect(surface, BLACK, bar_r.inflate(4, 4), border_radius=4)
            pygame.draw.rect(surface, CYAN_LIGHT, bar_r, border_radius=3)

        self.music_slider.draw(surface)
        self.sfx_slider.draw(surface)


class InGameHUD:
    """Giao diện HUD hiển thị trong lúc đang chơi."""

    def __init__(self):
        self.font_hud = pygame.font.SysFont("arialblack", 20)
        self.font_attempt = pygame.font.SysFont("arialblack", 40)
        self.font_win = pygame.font.SysFont("arialblack", 54)
        self.pause_btn_rect = pygame.Rect(SCREEN_WIDTH - 64, 16, 46, 46)

    def handle_click(self, pos):
        if self.pause_btn_rect.collidepoint(pos):
            return "PAUSE"
        return None

    def draw(self, surface, level, attempt_count):
        att_screen_x = int(380 - level.camera_x)
        if -300 <= att_screen_x <= SCREEN_WIDTH + 200:
            DrawUtils.draw_outlined_text(surface, f"ATTEMPT  {attempt_count}", self.font_attempt, (att_screen_x, 220), WHITE, BLACK, 4)

        bar_w, bar_h = 420, 18
        bar_x = (SCREEN_WIDTH - bar_w) // 2
        bar_y = 18
        pygame.draw.rect(surface, (10, 15, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=9)
        fill_w = int(bar_w * (level.progress / 100.0))
        if fill_w > 0:
            pygame.draw.rect(surface, PROGRESS_GREEN, (bar_x, bar_y, max(14, fill_w), bar_h), border_radius=9)
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=9)
        DrawUtils.draw_outlined_text(surface, f"{level.progress}%", self.font_hud, (bar_x + bar_w + 42, bar_y + 9), WHITE, BLACK, 2)

        pygame.draw.rect(surface, (20, 35, 70), self.pause_btn_rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.pause_btn_rect, 2, border_radius=10)
        cx, cy = self.pause_btn_rect.center
        pygame.draw.rect(surface, GOLD_YELLOW, (cx - 9, cy - 11, 6, 22), border_radius=2)
        pygame.draw.rect(surface, GOLD_YELLOW, (cx + 3, cy - 11, 6, 22), border_radius=2)

        if level.player.victory:
            DrawUtils.draw_outlined_text(
                surface,
                "LEVEL COMPLETE!",
                self.font_win,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40),
                LOGO_GREEN_TOP,
                BLACK,
                5,
            )
            DrawUtils.draw_outlined_text(
                surface,
                "Press [R] to Replay or [ESC] for Pause Menu",
                self.font_hud,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25),
                GOLD_YELLOW,
                BLACK,
                3,
            )