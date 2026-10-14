# main.py
import sys
import math
import array
import pygame

from config import *
from level import Level
from ui import MainMenuUI, PauseMenuUI, InGameHUD


class SynthAudioEngine:
    """Bộ tổng hợp âm thanh bằng thuật toán tạo nhạc nền điện tử và SFX."""

    def __init__(self):
        self.enabled = False
        self.music_vol = 0.92
        self.sfx_vol = 0.92
        self.bgm_channel = None
        self.bgm_sound = None
        self.sfx = {}

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._build_sounds()
        except Exception:
            self.enabled = False

    def _make_wave(self, freq_func, duration, volume=0.4, wave_type="square"):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array("h", [0] * n_samples)
        phase = 0.0
        for i in range(n_samples):
            t = i / float(sample_rate)
            freq = freq_func(t)
            phase += (math.tau * freq) / sample_rate
            env = min(1.0, (1.0 - t / duration) * 4.0)
            if wave_type == "square":
                val = 1.0 if math.sin(phase) >= 0 else -1.0
            elif wave_type == "saw":
                val = 2.0 * ((phase / math.tau) - math.floor(0.5 + phase / math.tau))
            else:
                val = math.sin(phase)
            buf[i] = int(val * volume * env * 32767)
        return pygame.mixer.Sound(buffer=buf)

    def _build_sounds(self):
        self.sfx["jump"] = self._make_wave(lambda t: 240 + 520 * t, 0.14, 0.30, "square")
        self.sfx["orb"] = self._make_wave(lambda t: 380 + 780 * t, 0.18, 0.35, "saw")
        self.sfx["portal"] = self._make_wave(lambda t: 520 + math.sin(t * 45) * 180, 0.28, 0.35, "saw")
        self.sfx["death"] = self._make_wave(lambda t: max(60, 320 - 650 * t), 0.35, 0.40, "saw")
        self.sfx["click"] = self._make_wave(lambda t: 660, 0.06, 0.25, "sine")

        notes = [261.6, 329.6, 392.0, 523.3, 392.0, 329.6, 293.7, 349.2, 440.0, 587.3, 440.0, 349.2, 329.6, 392.0, 493.9, 523.3]
        note_dur = 0.18
        sample_rate = 44100
        total_samples = int(sample_rate * note_dur * len(notes))
        bgm_buf = array.array("h", [0] * total_samples)

        idx = 0
        for n_freq in notes:
            n_samp = int(sample_rate * note_dur)
            phase = 0.0
            for i in range(n_samp):
                t = i / float(sample_rate)
                phase += (math.tau * n_freq) / sample_rate
                env = max(0.0, 1.0 - (t / note_dur) * 0.75)
                lead = 0.6 if math.sin(phase) >= 0 else -0.6
                bass = math.sin(phase * 0.5) * 0.4
                bgm_buf[idx] = int((lead + bass) * env * 0.22 * 32767)
                idx += 1

        self.bgm_sound = pygame.mixer.Sound(buffer=bgm_buf)
        self.bgm_channel = self.bgm_sound.play(loops=-1)
        self.set_volumes(self.music_vol, self.sfx_vol)

    def set_volumes(self, music_vol, sfx_vol):
        self.music_vol = music_vol
        self.sfx_vol = sfx_vol
        if not self.enabled:
            return
        if self.bgm_channel:
            self.bgm_channel.set_volume(self.music_vol)
        for s in self.sfx.values():
            s.set_volume(self.sfx_vol)

    def play_sfx(self, name):
        if self.enabled and name in self.sfx:
            self.sfx[name].play()


class GameEngine:
    """Bộ máy điều khiển trung tâm quản lý State Machine, Input và Vòng lặp 60 FPS."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.audio = SynthAudioEngine()
        self.level = Level()
        self.main_menu = MainMenuUI()
        self.pause_menu = PauseMenuUI()
        self.hud = InGameHUD()

        self.state = STATE_MENU
        self.attempt_count = 1
        self.death_respawn_timer = 0.0

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
                            self.state = STATE_PAUSED

                    elif self.state == STATE_PLAYING:
                        if event.key == pygame.K_ESCAPE:
                            self.audio.play_sfx("click")
                            self.state = STATE_PAUSED
                        elif event.key == pygame.K_r:
                            self.level.reset()
                            self.attempt_count += 1
                        elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                            just_pressed = True

                    elif self.state == STATE_PAUSED:
                        if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                            self.audio.play_sfx("click")
                            self.state = STATE_PLAYING

                if self.state == STATE_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        action = self.main_menu.handle_click(event.pos)
                        if action == "PLAY":
                            self.audio.play_sfx("click")
                            self.state = STATE_PAUSED
                        elif action == "FULLSCREEN":
                            self.toggle_fullscreen()

                elif self.state == STATE_PAUSED:
                    action = self.pause_menu.handle_event(event)
                    if action == "VOLUME_CHANGED":
                        self.audio.set_volumes(self.pause_menu.music_slider.value, self.pause_menu.sfx_slider.value)
                    elif action == "RESUME":
                        self.audio.play_sfx("click")
                        if self.level.player.is_dead or self.level.player.victory:
                            self.level.reset()
                        self.state = STATE_PLAYING
                    elif action == "REPLAY":
                        self.audio.play_sfx("click")
                        self.level.reset()
                        self.attempt_count += 1
                        self.state = STATE_PLAYING
                    elif action == "MENU":
                        self.audio.play_sfx("click")
                        self.level.reset()
                        self.level.background.set_theme(STATE_MENU)
                        self.state = STATE_MENU
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
                self.level.background.set_theme(STATE_MENU)
                self.level.background.update(dt, speed=180.0)
                self.main_menu.update(dt)

            elif self.state == STATE_PLAYING:
                was_dead = self.level.player.is_dead
                was_on_ground = self.level.player.on_ground
                prev_mode = self.level.player.mode

                self.level.update(dt, self._is_jump_holding(), just_pressed)

                if was_on_ground and not self.level.player.on_ground and self.level.player.vel_y < 0:
                    self.audio.play_sfx("jump")
                if self.level.player.mode != prev_mode:
                    self.audio.play_sfx("portal")
                if not was_dead and self.level.player.is_dead:
                    self.audio.play_sfx("death")
                    self.death_respawn_timer = 0.95

                if self.level.player.is_dead:
                    self.death_respawn_timer -= dt
                    if self.death_respawn_timer <= 0:
                        self.level.reset()
                        self.attempt_count += 1

            # --- 3. KẾT XUẤT ĐỒ HỌA (RENDER) ---
            if self.state == STATE_MENU:
                self.level.background.draw(self.screen, self.level.background.scroll_x, mode=STATE_MENU, draw_ground=True)
                self.main_menu.draw(self.screen)

            elif self.state == STATE_PLAYING:
                self.level.draw(self.screen)
                self.hud.draw(self.screen, self.level, self.attempt_count)

            elif self.state == STATE_PAUSED:
                self.level.background.draw(self.screen, self.level.camera_x, mode=STATE_MENU, draw_ground=True)
                # Luôn hiển thị phần trăm kỷ lục cao nhất (best_progress) người chơi đạt được trong game
                self.pause_menu.draw(self.screen, self.level.best_progress, self.attempt_count)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()