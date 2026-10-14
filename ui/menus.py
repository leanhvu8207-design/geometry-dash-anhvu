# ui/menus.py
import math
import pygame
from config import *
from vfx import DrawUtils
from .components import AudioSlider, CircleIconButton


class MainMenuUI:
    """Giao diện Màn hình chính với 3 huy hiệu: Lê Anh Vũ, Gemini Argon 4 và Thái tử."""

    def __init__(self):
        self.font_logo = pygame.font.SysFont("impact", 76)
        self.font_try = pygame.font.SysFont("arialblack", 30, italic=True)
        self.font_robtop = pygame.font.SysFont("arialblack", 38)
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
            return "OPEN_LEVEL_SELECT"
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
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, BLACK, rect, border_radius=10)
        pygame.draw.rect(surface, (215, 225, 245), rect, 2, border_radius=10)

        ic_x = x + 26
        ic_y = y + h // 2

        if badge_style == "AUTHOR":
            pygame.draw.rect(surface, PLAYER_PINK, (ic_x - 11, ic_y - 11, 22, 22), border_radius=4)
            pygame.draw.rect(surface, GOLD_YELLOW, (ic_x - 11, ic_y - 11, 22, 22), 2, border_radius=4)
            pygame.draw.circle(surface, WHITE, (ic_x - 4, ic_y - 2), 2)
            pygame.draw.circle(surface, WHITE, (ic_x + 4, ic_y - 2), 2)
        elif badge_style == "GEMINI":
            pts = [(ic_x, ic_y - 14), (ic_x + 13, ic_y), (ic_x, ic_y + 14), (ic_x - 13, ic_y)]
            pygame.draw.polygon(surface, CYAN_LIGHT, pts)
            pygame.draw.polygon(surface, WHITE, pts, 2)
            pygame.draw.circle(surface, WHITE, (ic_x, ic_y), 4)
        elif badge_style == "PRINCE":
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

        badge_y = SCREEN_HEIGHT - 96
        self._draw_custom_badge(surface, 540, badge_y, 220, 56, "CREATED BY", "Lê Anh Vũ", "AUTHOR")
        self._draw_custom_badge(surface, 780, badge_y, 235, 56, "POWERED BY", "Gemini Argon 4", "GEMINI")
        self._draw_custom_badge(surface, 1035, badge_y, 200, 56, "VIP EDITION", "Thái tử", "PRINCE")

        copy_surf = self.font_copy.render("© 2026 Lê Anh Vũ · Thái tử Edition", True, (110, 150, 215))
        surface.blit(copy_surf, (SCREEN_WIDTH - copy_surf.get_width() - 24, SCREEN_HEIGHT - 26))


class LevelSelectUI:
    """Giao diện Chọn Màn Chơi (Level Select Menu)."""

    def __init__(self):
        self.font_level_title = pygame.font.SysFont("arialblack", 44)
        self.font_star = pygame.font.SysFont("arialblack", 26)
        self.font_mode = pygame.font.SysFont("arialblack", 23)
        self.font_pct = pygame.font.SysFont("arialblack", 22)
        self.font_soundtrack = pygame.font.SysFont("arialblack", 22)
        self.font_info = pygame.font.SysFont("arial", 22, bold=True)

        self.back_btn_rect = pygame.Rect(22, 16, 62, 68)
        self.left_arrow_rect = pygame.Rect(22, 260, 68, 130)
        self.right_arrow_rect = pygame.Rect(SCREEN_WIDTH - 90, 260, 68, 130)
        self.card_rect = pygame.Rect(255, 110, 770, 210)

    def handle_click(self, pos):
        if self.back_btn_rect.collidepoint(pos):
            return "BACK_TO_MAIN"
        if self.left_arrow_rect.collidepoint(pos):
            return "PREV_LEVEL"
        if self.right_arrow_rect.collidepoint(pos):
            return "NEXT_LEVEL"
        if self.card_rect.collidepoint(pos):
            return "START_LEVEL"
        return None

    def _draw_top_frame(self, surface):
        cx = SCREEN_WIDTH // 2
        for x_pos in (cx - 320, cx + 250):
            r = pygame.Rect(x_pos, -6, 70, 32)
            pygame.draw.rect(surface, WHITE, r.inflate(8, 8), border_radius=6)
            pygame.draw.rect(surface, BLACK, r.inflate(4, 4), border_radius=5)
            pygame.draw.rect(surface, CYAN_LIGHT, r, border_radius=4)

        for x_pos in (cx - 260, cx + 50):
            r = pygame.Rect(x_pos, -4, 210, 56)
            pygame.draw.rect(surface, WHITE, r.inflate(8, 8), border_radius=6)
            pygame.draw.rect(surface, BLACK, r.inflate(4, 4), border_radius=5)
            pygame.draw.rect(surface, LOGO_GREEN_BOT, r, border_radius=4)
            pygame.draw.rect(surface, LOGO_GREEN_TOP, (r.x + 4, 0, r.w - 8, 26), border_radius=3)

        center_r = pygame.Rect(cx - 52, -4, 104, 64)
        pygame.draw.rect(surface, WHITE, center_r.inflate(8, 8), border_radius=6)
        pygame.draw.rect(surface, BLACK, center_r.inflate(4, 4), border_radius=5)
        pygame.draw.rect(surface, CYAN_DARK, center_r, border_radius=4)
        pygame.draw.rect(surface, CYAN_LIGHT, (center_r.x + 4, 0, center_r.w - 8, 36), border_radius=3)

    def _draw_bottom_corners(self, surface):
        steps = [
            (0, SCREEN_HEIGHT - 160, 26, 160),
            (26, SCREEN_HEIGHT - 122, 34, 122),
            (60, SCREEN_HEIGHT - 84, 38, 84),
            (98, SCREEN_HEIGHT - 46, 52, 46),
        ]
        for bx, by, bw, bh in steps:
            rl = pygame.Rect(bx, by, bw, bh)
            pygame.draw.rect(surface, WHITE, rl.inflate(8, 8), border_radius=5)
            pygame.draw.rect(surface, BLACK, rl.inflate(4, 4), border_radius=4)
            pygame.draw.rect(surface, CYAN_LIGHT if bw < 35 else LOGO_GREEN_TOP, rl)

            rr = pygame.Rect(SCREEN_WIDTH - bx - bw, by, bw, bh)
            pygame.draw.rect(surface, WHITE, rr.inflate(8, 8), border_radius=5)
            pygame.draw.rect(surface, BLACK, rr.inflate(4, 4), border_radius=4)
            pygame.draw.rect(surface, CYAN_LIGHT if bw < 35 else LOGO_GREEN_TOP, rr)

    def _draw_difficulty_face(self, surface, center, color):
        cx, cy = center
        r = 38
        pygame.draw.circle(surface, BLACK, (cx, cy), r + 3)
        pygame.draw.circle(surface, color, (cx, cy), r)
        pygame.draw.ellipse(surface, tuple(min(255, c + 55) for c in color), (cx - 24, cy - 30, 48, 22))

        for ex in (cx - 14, cx + 14):
            pygame.draw.circle(surface, BLACK, (ex, cy - 8), 9)
            pygame.draw.circle(surface, WHITE, (ex + 2, cy - 10), 4)
        pygame.draw.arc(surface, BLACK, (cx - 26, cy - 26, 22, 14), 0.3, 2.8, 3)
        pygame.draw.arc(surface, BLACK, (cx + 4, cy - 26, 22, 14), 0.3, 2.8, 3)

        mouth_rect = pygame.Rect(cx - 24, cy + 2, 48, 24)
        pygame.draw.arc(surface, BLACK, mouth_rect, math.pi, math.tau, 12)
        pygame.draw.polygon(surface, (35, 5, 15), [(cx - 22, cy + 10), (cx + 22, cy + 10), (cx + 14, cy + 24), (cx - 14, cy + 24)])
        pygame.draw.ellipse(surface, (240, 60, 120), (cx - 12, cy + 16, 24, 10))

    def _draw_star(self, surface, center, radius, fill_color, border_color=BLACK):
        cx, cy = center
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * (math.pi / 5)
            r = radius if i % 2 == 0 else radius * 0.44
            pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
        pygame.draw.polygon(surface, fill_color, pts)
        pygame.draw.polygon(surface, border_color, pts, 2)

    def draw(self, surface, level_manager):
        meta = level_manager.current_meta
        mouse_pos = pygame.mouse.get_pos()

        surface.fill(SELECT_BG_BLUE)
        ground_y_select = 588
        pygame.draw.rect(surface, (0, 18, 150), (0, ground_y_select, SCREEN_WIDTH, SCREEN_HEIGHT - ground_y_select))
        pygame.draw.line(surface, (80, 140, 255), (0, ground_y_select), (SCREEN_WIDTH, ground_y_select), 3)

        self._draw_top_frame(surface)
        self._draw_bottom_corners(surface)

        bx, by, bw, bh = self.back_btn_rect
        back_pts = [(bx + bw, by), (bx, by + bh // 2), (bx + bw, by + bh)]
        pygame.draw.polygon(surface, WHITE, [(bx + bw + 4, by - 4), (bx - 5, by + bh // 2), (bx + bw + 4, by + bh + 4)])
        pygame.draw.polygon(surface, BLACK, [(bx + bw + 2, by - 2), (bx - 2, by + bh // 2), (bx + bw + 2, by + bh + 2)])
        pygame.draw.polygon(surface, LOGO_GREEN_BOT, back_pts)
        pygame.draw.polygon(surface, LOGO_GREEN_TOP, [(bx + bw - 3, by + 6), (bx + 6, by + bh // 2), (bx + bw - 3, by + bh // 2)])

        info_c = (SCREEN_WIDTH - 42, 46)
        pygame.draw.circle(surface, BLACK, info_c, 26)
        pygame.draw.circle(surface, WHITE, info_c, 24)
        pygame.draw.circle(surface, CYAN_LIGHT, info_c, 21)
        DrawUtils.draw_outlined_text(surface, "i", self.font_info, info_c, WHITE, BLACK, 2)

        l_hover = self.left_arrow_rect.collidepoint(mouse_pos)
        lx, ly, lw, lh = self.left_arrow_rect.inflate(6 if l_hover else 0, 8 if l_hover else 0)
        l_pts = [(lx + lw, ly), (lx, ly + lh // 2), (lx + lw, ly + lh)]
        pygame.draw.polygon(surface, BLACK, [(lx + lw + 4, ly - 5), (lx - 5, ly + lh // 2), (lx + lw + 4, ly + lh + 5)])
        pygame.draw.polygon(surface, WHITE, l_pts)

        r_hover = self.right_arrow_rect.collidepoint(mouse_pos)
        rx, ry, rw, rh = self.right_arrow_rect.inflate(6 if r_hover else 0, 8 if r_hover else 0)
        r_pts = [(rx, ry), (rx + rw, ry + rh // 2), (rx, ry + rh)]
        pygame.draw.polygon(surface, BLACK, [(rx - 4, ry - 5), (rx + rw + 5, ry + rh // 2), (rx - 4, ry + rh + 5)])
        pygame.draw.polygon(surface, WHITE, r_pts)

        card_hover = self.card_rect.collidepoint(mouse_pos)
        c_rect = self.card_rect.inflate(6 if card_hover else 0, 4 if card_hover else 0)
        pygame.draw.rect(surface, SELECT_CARD_BLUE, c_rect, border_radius=26)
        pygame.draw.rect(surface, (0, 8, 65), c_rect, 3, border_radius=26)

        self._draw_difficulty_face(surface, (c_rect.x + 105, c_rect.centery - 6), meta["diff_color"])
        DrawUtils.draw_outlined_text(
            surface, meta["name"], self.font_level_title, (c_rect.centerx + 48, c_rect.centery - 6), WHITE, BLACK, 4
        )
        DrawUtils.draw_outlined_text(
            surface, str(meta["stars"]), self.font_star, (c_rect.right - 68, c_rect.top + 30), WHITE, BLACK, 3
        )
        self._draw_star(surface, (c_rect.right - 34, c_rect.top + 30), 17, GOLD_YELLOW)

        for i in range(3):
            coin_cx = c_rect.right - 145 + i * 54
            coin_cy = c_rect.bottom - 32
            earned = i < meta["coins"]
            outer_col = GOLD_YELLOW if earned else (140, 145, 150)
            inner_col = GOLD_ORANGE if earned else (95, 100, 105)
            pygame.draw.circle(surface, BLACK, (coin_cx, coin_cy), 23)
            pygame.draw.circle(surface, outer_col, (coin_cx, coin_cy), 21)
            pygame.draw.circle(surface, inner_col, (coin_cx, coin_cy), 16)
            self._draw_star(surface, (coin_cx, coin_cy), 11, GOLD_YELLOW if earned else (130, 135, 140), border_color=inner_col)

        bar_w, bar_h = 768, 46
        bar_x = (SCREEN_WIDTH - bar_w) // 2

        DrawUtils.draw_outlined_text(surface, "NORMAL  MODE", self.font_mode, (SCREEN_WIDTH // 2, 368), WHITE, BLACK, 3)
        norm_rect = pygame.Rect(bar_x, 392, bar_w, bar_h)
        pygame.draw.rect(surface, (0, 8, 65), norm_rect, border_radius=23)
        norm_pct = meta["best_normal"]
        if norm_pct > 0:
            fill_w = max(36, int(bar_w * (norm_pct / 100.0)))
            pygame.draw.rect(surface, PROGRESS_GREEN, (bar_x, 392, fill_w, bar_h), border_radius=23)
        DrawUtils.draw_outlined_text(surface, f"{norm_pct}%", self.font_pct, norm_rect.center, WHITE, BLACK, 3)

        DrawUtils.draw_outlined_text(surface, "PRACTICE  MODE", self.font_mode, (SCREEN_WIDTH // 2, 482), WHITE, BLACK, 3)
        prac_rect = pygame.Rect(bar_x, 506, bar_w, bar_h)
        pygame.draw.rect(surface, (0, 8, 65), prac_rect, border_radius=23)
        prac_pct = meta["best_practice"]
        if prac_pct > 0:
            fill_w = max(36, int(bar_w * (prac_pct / 100.0)))
            pygame.draw.rect(surface, CYAN_LIGHT, (bar_x, 506, fill_w, bar_h), border_radius=23)
        DrawUtils.draw_outlined_text(surface, f"{prac_pct}%", self.font_pct, prac_rect.center, WHITE, BLACK, 3)

        DrawUtils.draw_outlined_text(
            surface, "DOWNLOAD  THE  SOUNDTRACKS", self.font_soundtrack, (SCREEN_WIDTH // 2, 636), WHITE, BLACK, 3
        )

        total_dots = len(level_manager.levels)
        dot_spacing = 36
        start_dot_x = SCREEN_WIDTH // 2 - ((total_dots - 1) * dot_spacing) // 2
        for i in range(total_dots):
            dx = start_dot_x + i * dot_spacing
            dy = 678
            is_active = (i == level_manager.current_level_idx)
            pygame.draw.circle(surface, WHITE if is_active else (125, 135, 165), (dx, dy), 10 if is_active else 8)


class PauseMenuUI:
    """Giao diện Tạm dừng & Tổng kết Phá đảo."""

    def __init__(self):
        self.font_title = pygame.font.SysFont("arialblack", 42)
        self.font_mode = pygame.font.SysFont("arialblack", 24)
        self.font_pct = pygame.font.SysFont("arialblack", 22)
        self.font_attempt = pygame.font.SysFont("arialblack", 52)

        cy = 368
        self.btn_replay = CircleIconButton((452, cy), 58, "REPLAY")
        self.btn_play = CircleIconButton((648, cy), 78, "PLAY")
        self.btn_menu = CircleIconButton((844, cy), 58, "MENU")

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
            pos = event.pos
            if self.btn_play.is_hovered(pos):
                return "RESUME"
            if self.btn_replay.is_hovered(pos):
                return "REPLAY"
            if self.btn_menu.is_hovered(pos):
                return "MENU"
            if self.fullscreen_rect.collidepoint(pos):
                return "FULLSCREEN"
        return None

    def draw(self, surface, level_name, best_pct, attempt_count, is_victory=False):
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

        header_text = f"{level_name} - COMPLETE!" if is_victory else level_name
        header_col = LOGO_GREEN_TOP if is_victory else WHITE
        DrawUtils.draw_outlined_text(surface, header_text, self.font_title, (SCREEN_WIDTH // 2, 72), header_col, BLACK, 4)

        sub_text = "PHÁ ĐẢO THÀNH CÔNG! CHỌN REPLAY HOẶC MENU BÊN DƯỚI" if is_victory else "NORMAL  MODE"
        sub_col = GOLD_YELLOW if is_victory else WHITE
        DrawUtils.draw_outlined_text(surface, sub_text, self.font_mode, (SCREEN_WIDTH // 2, 142), sub_col, BLACK, 3)

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

        self.btn_replay.draw(surface, mouse_pos)
        self.btn_play.draw(surface, mouse_pos)
        self.btn_menu.draw(surface, mouse_pos)

        self.music_slider.draw(surface)
        self.sfx_slider.draw(surface)


class InGameHUD:
    """Giao diện HUD hiển thị thanh tiến độ và nút Pause trong lúc chơi."""

    def __init__(self):
        self.font_hud = pygame.font.SysFont("arialblack", 20)
        self.font_attempt = pygame.font.SysFont("arialblack", 40)
        self.pause_btn_rect = pygame.Rect(SCREEN_WIDTH - 64, 16, 46, 46)

    def handle_click(self, pos):
        if self.pause_btn_rect.collidepoint(pos):
            return "PAUSE"
        return None

    def draw(self, surface, level_manager, attempt_count):
        att_screen_x = int(380 - level_manager.camera_x)
        if -300 <= att_screen_x <= SCREEN_WIDTH + 200:
            DrawUtils.draw_outlined_text(surface, f"ATTEMPT  {attempt_count}", self.font_attempt, (att_screen_x, 220), WHITE, BLACK, 4)

        bar_w, bar_h = 420, 18
        bar_x = (SCREEN_WIDTH - bar_w) // 2
        bar_y = 18
        pygame.draw.rect(surface, (10, 15, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=9)
        fill_w = int(bar_w * (level_manager.progress / 100.0))
        if fill_w > 0:
            pygame.draw.rect(surface, PROGRESS_GREEN, (bar_x, bar_y, max(14, fill_w), bar_h), border_radius=9)
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=9)
        DrawUtils.draw_outlined_text(surface, f"{level_manager.progress}%", self.font_hud, (bar_x + bar_w + 42, bar_y + 9), WHITE, BLACK, 2)

        pygame.draw.rect(surface, (20, 35, 70), self.pause_btn_rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.pause_btn_rect, 2, border_radius=10)
        cx, cy = self.pause_btn_rect.center
        pygame.draw.rect(surface, GOLD_YELLOW, (cx - 9, cy - 11, 6, 22), border_radius=2)
        pygame.draw.rect(surface, GOLD_YELLOW, (cx + 3, cy - 11, 6, 22), border_radius=2)