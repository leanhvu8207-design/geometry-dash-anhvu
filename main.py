# main.py
import sys
import pygame

from config import *
from levels import LevelManager
from ui import MainMenuUI, LevelSelectUI, PauseMenuUI, InGameHUD, SynthAudioEngine


class GameEngine:
    """Bộ máy điều khiển trung tâm kết nối các Package theo kiến trúc Modular OOP."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.audio = SynthAudioEngine()
        self.level_manager = LevelManager()
        self.main_menu = MainMenuUI()
        self.level_select = LevelSelectUI()
        self.pause_menu = PauseMenuUI()
        self.hud = InGameHUD()

        self.state = STATE_MENU
        self.attempt_count = 1
        self.death_respawn_timer = 0.0
        self.victory_overlay_timer = 0.0

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def _is_jump_holding(self):
        keys = pygame.key.get_pressed()
        mouse_btns = pygame.mouse.get_pressed()
        return keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] or mouse_btns[0]

    def run(self):
        running = True
        while running:
            dt = min(0.05, self.clock.tick(FPS) / 1000.0)
            just_pressed = False

            # --- 1. XỬ LÝ SỰ KIỆN (EVENTS) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                    if self.state == STATE_MENU:
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.audio.play_sfx("click")
                            self.state = STATE_LEVEL_SELECT

                    elif self.state == STATE_LEVEL_SELECT:
                        if event.key == pygame.K_ESCAPE:
                            self.audio.play_sfx("click")
                            self.state = STATE_MENU
                        elif event.key == pygame.K_LEFT:
                            self.audio.play_sfx("click")
                            self.level_manager.load_level(self.level_manager.current_level_idx - 1)
                        elif event.key == pygame.K_RIGHT:
                            self.audio.play_sfx("click")
                            self.level_manager.load_level(self.level_manager.current_level_idx + 1)
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.audio.play_sfx("click")
                            self.attempt_count = 1
                            self.level_manager.reset()
                            self.state = STATE_PLAYING

                    elif self.state == STATE_PLAYING:
                        if event.key == pygame.K_ESCAPE:
                            self.audio.play_sfx("click")
                            self.state = STATE_PAUSED
                        elif event.key == pygame.K_r:
                            self.level_manager.reset()
                            self.attempt_count += 1
                        elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                            just_pressed = True

                    elif self.state == STATE_PAUSED:
                        if event.key == pygame.K_ESCAPE:
                            self.audio.play_sfx("click")
                            self.level_manager.reset()
                            self.state = STATE_LEVEL_SELECT
                        elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.audio.play_sfx("click")
                            if self.level_manager.player.is_dead or self.level_manager.player.victory:
                                self.level_manager.reset()
                                self.attempt_count += 1
                            self.state = STATE_PLAYING

                if self.state == STATE_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        action = self.main_menu.handle_click(event.pos)
                        if action == "OPEN_LEVEL_SELECT":
                            self.audio.play_sfx("click")
                            self.state = STATE_LEVEL_SELECT
                        elif action == "FULLSCREEN":
                            self.toggle_fullscreen()

                elif self.state == STATE_LEVEL_SELECT:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        action = self.level_select.handle_click(event.pos)
                        if action == "BACK_TO_MAIN":
                            self.audio.play_sfx("click")
                            self.state = STATE_MENU
                        elif action == "PREV_LEVEL":
                            self.audio.play_sfx("click")
                            self.level_manager.load_level(self.level_manager.current_level_idx - 1)
                        elif action == "NEXT_LEVEL":
                            self.audio.play_sfx("click")
                            self.level_manager.load_level(self.level_manager.current_level_idx + 1)
                        elif action == "START_LEVEL":
                            self.audio.play_sfx("click")
                            self.attempt_count = 1
                            self.level_manager.reset()
                            self.state = STATE_PLAYING

                elif self.state == STATE_PAUSED:
                    action = self.pause_menu.handle_event(event)
                    if action == "VOLUME_CHANGED":
                        self.audio.set_volumes(self.pause_menu.music_slider.value, self.pause_menu.sfx_slider.value)
                    elif action == "RESUME":
                        self.audio.play_sfx("click")
                        if self.level_manager.player.is_dead or self.level_manager.player.victory:
                            self.level_manager.reset()
                            self.attempt_count += 1
                        self.state = STATE_PLAYING
                    elif action == "REPLAY":
                        self.audio.play_sfx("click")
                        self.level_manager.reset()
                        self.attempt_count += 1
                        self.state = STATE_PLAYING
                    elif action == "MENU":
                        self.audio.play_sfx("click")
                        self.level_manager.reset()
                        self.state = STATE_LEVEL_SELECT
                    elif action == "FULLSCREEN":
                        self.toggle_fullscreen()

                elif self.state == STATE_PLAYING:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.hud.handle_click(event.pos) == "PAUSE":
                            self.audio.play_sfx("click")
                            self.state = STATE_PAUSED
                        else:
                            just_pressed = True

            # --- 2. CẬP NHẬT LOGIC (UPDATE) ---
            if self.state == STATE_MENU:
                self.level_manager.background.set_theme(STATE_MENU)
                self.level_manager.background.update(dt, speed=180.0)
                self.main_menu.update(dt)

            elif self.state == STATE_PLAYING:
                p = self.level_manager.player
                was_dead = p.is_dead
                was_victory = p.victory
                was_on_ground = p.on_ground
                prev_mode = p.mode
                prev_grav = p.gravity_dir

                self.level_manager.update(dt, self._is_jump_holding(), just_pressed)

                if was_on_ground and not p.on_ground and (p.vel_y * p.gravity_dir) < 0:
                    self.audio.play_sfx("jump")
                if p.mode != prev_mode or p.gravity_dir != prev_grav:
                    self.audio.play_sfx("portal")
                if not was_dead and p.is_dead:
                    self.audio.play_sfx("death")
                    self.death_respawn_timer = 0.95
                if not was_victory and p.victory:
                    self.audio.play_sfx("win")
                    self.victory_overlay_timer = 2.85

                if p.is_dead:
                    self.death_respawn_timer -= dt
                    if self.death_respawn_timer <= 0:
                        self.level_manager.reset()
                        self.attempt_count += 1

                if p.victory:
                    self.victory_overlay_timer -= dt
                    if self.victory_overlay_timer <= 0:
                        self.state = STATE_PAUSED

            # --- 3. KẾT XUẤT ĐỒ HỌA (RENDER) ---
            if self.state == STATE_MENU:
                self.level_manager.background.draw(
                    self.screen, self.level_manager.background.scroll_x, mode=STATE_MENU, draw_ground=True
                )
                self.main_menu.draw(self.screen)

            elif self.state == STATE_LEVEL_SELECT:
                self.level_select.draw(self.screen, self.level_manager)

            elif self.state == STATE_PLAYING:
                self.level_manager.draw(self.screen)
                if not self.level_manager.player.victory:
                    self.hud.draw(self.screen, self.level_manager, self.attempt_count)

            elif self.state == STATE_PAUSED:
                self.level_manager.background.draw(
                    self.screen, self.level_manager.camera_x, mode=STATE_MENU, draw_ground=True
                )
                self.pause_menu.draw(
                    self.screen,
                    self.level_manager.current_meta["name"],
                    self.level_manager.best_progress,
                    self.attempt_count,
                    is_victory=self.level_manager.player.victory,
                )

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()