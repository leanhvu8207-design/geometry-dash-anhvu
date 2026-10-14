# levels/__init__.py
from .base_level import BaseLevel
from .level_1_stereo import StereoMadnessLevel
from .level_2_back_on_track import BackOnTrackLevel


class LevelManager:
    """Quản lý danh sách tất cả các Màn chơi (Maps) và lưu trữ kỷ lục của từng Map."""

    def __init__(self):
        self.levels = [
            StereoMadnessLevel(),
            BackOnTrackLevel(),
        ]
        self.current_level_idx = 0

    @property
    def current_level(self):
        return self.levels[self.current_level_idx]

    @property
    def current_meta(self):
        return self.current_level.meta

    @property
    def player(self):
        return self.current_level.player

    @property
    def background(self):
        return self.current_level.background

    @property
    def camera_x(self):
        return self.current_level.camera_x

    @property
    def progress(self):
        return self.current_level.progress

    @property
    def best_progress(self):
        return self.current_level.best_progress

    def load_level(self, idx):
        self.current_level_idx = idx % len(self.levels)
        self.current_level.reset()

    def reset(self):
        self.current_level.reset()

    def update(self, dt, is_holding, just_pressed):
        self.current_level.update(dt, is_holding, just_pressed)

    def draw(self, surface):
        self.current_level.draw(surface)