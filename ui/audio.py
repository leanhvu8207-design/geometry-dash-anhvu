# ui/audio.py
import math
import array
import pygame


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
        self.sfx["win"] = self._make_wave(lambda t: 440 + 480 * t, 0.65, 0.42, "square")

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