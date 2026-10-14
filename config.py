# config.py
import pygame

# --- CẤU HÌNH CỬA SỔ & HIỆU NĂNG ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Geometry Dash - Stereo Madness (OOP Edition)"

# --- THÔNG SỐ VẬT LÝ & MẶT ĐẤT ---
GROUND_Y = 590               # Tọa độ Y của mặt đất
TILE_SIZE = 50               # Kích thước 1 ô vuông tiêu chuẩn (1 Block = 50x50 px)
SCROLL_SPEED = 460.0         # Tốc độ trôi màn hình (pixels / giây)

# Vật lý chế độ CUBE
CUBE_GRAVITY = 2900.0        # Gia tốc trọng trường
CUBE_JUMP_VEL = -860.0       # Vận tốc nhảy cơ bản
ORB_JUMP_VEL = -940.0        # Vận tốc bật khi kích hoạt Orb trên không
PAD_JUMP_VEL = -1150.0       # Vận tốc bật khi chạm Pad lò xo

# Vật lý chế độ WAVE (Bay zíc-zắc 45 độ)
WAVE_SPEED_Y = 460.0         # Vận tốc lên/xuống bằng tốc độ ngang -> tạo góc 45 độ chuẩn

# --- TRẠNG THÁI GAME (STATE MACHINE) ---
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"

# --- CHẾ ĐỘ NHÂN VẬT ---
MODE_CUBE = "CUBE"
MODE_WAVE = "WAVE"

# --- BẢNG MÀU TRÍCH XUẤT TỪ UI & GAMEPLAY ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Màu Main Menu & Pause UI
MENU_BG_BLUE = (4, 48, 130)
MENU_GRID_BLUE = (2, 34, 98)
MENU_GROUND_BLUE = (0, 38, 105)
LOGO_GREEN_TOP = (170, 255, 40)
LOGO_GREEN_BOT = (90, 200, 10)
GOLD_YELLOW = (255, 205, 20)
GOLD_ORANGE = (240, 130, 0)
CYAN_LIGHT = (0, 230, 240)
CYAN_DARK = (0, 150, 170)
PROGRESS_GREEN = (0, 255, 20)

# Màu Stage 1: Cube Mode (Tông Tím Neon)
CUBE_BG_COLOR = (22, 5, 58)
CUBE_GRID_COLOR = (35, 10, 82)
BLOCK_PURPLE = (165, 15, 255)
BLOCK_PURPLE_DARK = (90, 5, 160)
BLOCK_ORANGE = (255, 160, 30)
BLOCK_PINK = (245, 100, 180)
PLAYER_PINK = (255, 35, 125)
PLAYER_YELLOW = (255, 235, 20)

# Màu Stage 2: Wave Mode (Tông Đỏ Tím & Đường hầm Cam Neon)
WAVE_BG_COLOR = (85, 5, 50)
WAVE_BRICK_COLOR = (70, 10, 95)
WAVE_NEON_ORANGE = (255, 140, 0)
WAVE_NEON_RED = (255, 30, 60)
WAVE_TRAIL_PINK = (255, 70, 255)
WAVE_PLAYER_PURPLE = (160, 40, 255)