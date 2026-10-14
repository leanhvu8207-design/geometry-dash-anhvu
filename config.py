# config.py
import pygame

# --- CẤU HÌNH CỬA SỔ & HIỆU NĂNG ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Geometry Dash - Thái tử Edition (Modular OOP)"

# --- THÔNG SỐ VẬT LÝ & MẶT ĐẤT ---
CEILING_Y = 70               # Tọa độ trần khi bay hoặc đảo ngược trọng lực
GROUND_Y = 590               # Tọa độ Y của mặt đất
TILE_SIZE = 50               # Kích thước 1 ô vuông tiêu chuẩn (50x50 px)
SCROLL_SPEED = 470.0         # Tốc độ trôi màn hình (pixels / giây)

# Vật lý chế độ CUBE
CUBE_GRAVITY = 2950.0        # Gia tốc trọng trường
CUBE_JUMP_VEL = -870.0       # Vận tốc nhảy cơ bản
ORB_JUMP_VEL = -930.0        # Vận tốc bật khi kích hoạt Orb trên không
PAD_JUMP_VEL = -1140.0       # Vận tốc bật cao khi chạm Đệm lò xo (Jump Pad)

# Vật lý chế độ WAVE (Bay zíc-zắc 45 độ)
WAVE_SPEED_Y = 470.0

# Vật lý chế độ SHIP (Lái máy bay mượt mà)
SHIP_GRAVITY = 1480.0
SHIP_THRUST = -1680.0
SHIP_MAX_VEL_Y = 510.0

# --- TRẠNG THÁI GAME (STATE MACHINE) ---
STATE_MENU = "MENU"
STATE_LEVEL_SELECT = "LEVEL_SELECT"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"

# --- CHẾ ĐỘ NHÂN VẬT ---
MODE_CUBE = "CUBE"
MODE_SHIP = "SHIP"
MODE_WAVE = "WAVE"

# --- BẢNG MÀU TRÍCH XUẤT TỪ UI & GAMEPLAY ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MENU_BG_BLUE = (4, 48, 130)
MENU_GRID_BLUE = (2, 34, 98)
MENU_GROUND_BLUE = (0, 38, 105)
SELECT_BG_BLUE = (0, 26, 205)
SELECT_CARD_BLUE = (0, 12, 95)

LOGO_GREEN_TOP = (170, 255, 40)
LOGO_GREEN_BOT = (90, 200, 10)
GOLD_YELLOW = (255, 205, 20)
GOLD_ORANGE = (240, 130, 0)
CYAN_LIGHT = (0, 230, 240)
CYAN_DARK = (0, 150, 170)
PROGRESS_GREEN = (0, 255, 20)

# Màu Map 1
CUBE_BG_COLOR = (22, 5, 58)
BLOCK_PURPLE = (165, 15, 255)
BLOCK_ORANGE = (255, 160, 30)
BLOCK_PINK = (245, 100, 180)
PLAYER_PINK = (255, 35, 125)
PLAYER_YELLOW = (255, 235, 20)

WAVE_BG_COLOR = (85, 5, 50)
WAVE_NEON_ORANGE = (255, 140, 0)
WAVE_NEON_RED = (255, 30, 60)
WAVE_TRAIL_PINK = (255, 70, 255)
WAVE_PLAYER_PURPLE = (160, 40, 255)

# Màu Map 2 (Chuyển màu qua 6 phân đoạn dài 18,000px)
MAP2_BLUE_BG = (10, 42, 185)
MAP2_BLUE_GND = (4, 15, 78)

MAP2_PURPLE_BG = (105, 10, 168)
MAP2_PURPLE_GND = (52, 4, 92)

MAP2_INDIGO_BG = (68, 12, 145)
MAP2_INDIGO_GND = (30, 5, 80)

MAP2_MAGENTA_BG = (188, 14, 82)
MAP2_MAGENTA_GND = (28, 6, 22)

MAP2_CRIMSON_BG = (195, 12, 18)
MAP2_CRIMSON_GND = (92, 6, 10)

PLAYER_GREEN_OUTER = (45, 255, 25)
PLAYER_PURPLE_MID = (45, 20, 110)