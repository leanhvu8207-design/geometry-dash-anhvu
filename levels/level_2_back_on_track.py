# levels/level_2_back_on_track.py
from config import *
from entities import ClassicDarkBlock, GridBlock, FloatingSlab, Spike, SpikeStrip, Sawblade, JumpOrb, JumpPad, ModePortal, GravityPortal
from .base_level import BaseLevel


class BackOnTrackLevel(BaseLevel):
    """
    MAP 2: BACK ON TRACK - Độ dài 18,000px (Gấp đôi bản cũ), gồm 6 Chương (Acts):
    - Chương 1 (X: 0 -> 3000): Nền Xanh Hiền Hòa - Khởi động gai Nhỏ/Lớn & Đệm lò xo JumpPad [Hình 10]
    - Chương 2 (X: 3000 -> 6400): Nền Tím Thử Thách - Bục treo vòng trắng trên Thảm Gai chuẩn hitbox [Hình 11, 17]
                                  + Pháo đài lưới tím bậc thang chuẩn 1 ô (Đã xóa sạch gai mờ lơ lửng!) [Hình 12, 18]
    - Chương 3 (X: 6400 -> 9600): Nền Chàm Đậm - Cổng Đảo Ngược Trọng Lực (Chạy trên trần) & Nhịp Tên Lửa Wave
    - Chương 4 (X: 9600 -> 13600): Nền Hồng Đỏ Đậm - Đại chiến Không gian Lái Máy Bay (Ship Mode) dài 4000px [Hình 13, 14]
                                   với cột lưới treo vòng trắng, hành lang 7 gai, bánh răng cưa xoay & đảo trọng lực máy bay!
    - Chương 5 (X: 13600 -> 16500): Nền Đỏ Thẫm Gay Cấn - Cổng 3D về Cube, bục lắt léo & Vòng bật xanh cắm cọc [Hình 15]
    - Chương 6 (X: 16500 -> 18000): Cổng Hồng 3D biến hình thành Máy Bay [Hình 15, 19] bay vọt qua khối chữ L
                                    đâm thẳng vào Bức Tường Ánh Sáng Chiến Thắng [Hình 16]!
    """

    def __init__(self):
        meta = {
            "id": 1,
            "name": "BACK ON TRACK",
            "stars": 2,
            "diff_color": (40, 235, 60),
            "best_normal": 0,
            "best_practice": 0,
            "coins": 0,
        }
        super().__init__(meta_info=meta, length=18000.0, skin_name="GREEN_CONCENTRIC")

    def _update_theme(self):
        px = self.player.x
        if px < 3000:
            self.background.set_custom_theme(MAP2_BLUE_BG, MAP2_BLUE_GND, classic_ground=True)
        elif px < 6400:
            self.background.set_custom_theme(MAP2_PURPLE_BG, MAP2_PURPLE_GND, classic_ground=True)
        elif px < 9600:
            self.background.set_custom_theme(MAP2_INDIGO_BG, MAP2_INDIGO_GND, classic_ground=True)
        elif px < 13600:
            self.background.set_custom_theme(MAP2_MAGENTA_BG, MAP2_MAGENTA_GND, classic_ground=True)
        else:
            self.background.set_custom_theme(MAP2_CRIMSON_BG, MAP2_CRIMSON_GND, classic_ground=True)

    def _build_map(self):
        # =========================================================================
        # CHƯƠNG 1 (X: 600 -> 3000): NỀN XANH DƯƠNG HIỀN HÒA (HÌNH MẪU 10)
        # =========================================================================
        # Cặp gai Nhỏ + Lớn sát nhau đặc trưng của Hình mẫu 10
        self.hazards.append(Spike(750, GROUND_Y - int(TILE_SIZE * 0.55), direction="UP", style="CLASSIC_BLACK", scale=0.55))
        self.hazards.append(Spike(780, GROUND_Y - TILE_SIZE, direction="UP", style="CLASSIC_BLACK", scale=1.0))

        # Các bục bước nhẹ nhàng
        self.add_slab(1100, GROUND_Y - 60, cols=3, color=(60, 105, 255))
        self.add_slab(1400, GROUND_Y - 120, cols=3, color=(60, 105, 255))

        # Giới thiệu Đệm lò xo vàng (JumpPad) tự động bật vọt qua 3 gai liên tiếp
        self.triggers.append(JumpPad(1750, GROUND_Y, pad_color=GOLD_YELLOW))
        self.hazards.append(Spike(1850, GROUND_Y - TILE_SIZE, direction="UP"))
        self.hazards.append(Spike(1900, GROUND_Y - TILE_SIZE, direction="UP"))
        self.hazards.append(Spike(1950, GROUND_Y - TILE_SIZE, direction="UP"))
        self.add_slab(2050, GROUND_Y - 110, cols=4, color=(60, 105, 255))

        # Nhịp cầu có vòng Cyan Orb dẫn sang Chương 2
        self.triggers.append(JumpOrb(2450, GROUND_Y - 140, orb_type="CYAN_ORB"))
        self.hazards.append(Spike(2400, GROUND_Y - TILE_SIZE, direction="UP"))
        self.hazards.append(Spike(2450, GROUND_Y - TILE_SIZE, direction="UP"))
        self.hazards.append(Spike(2750, GROUND_Y - int(TILE_SIZE * 0.55), direction="UP", scale=0.55))
        self.hazards.append(Spike(2780, GROUND_Y - TILE_SIZE, direction="UP", scale=1.0))

        # =========================================================================
        # CHƯƠNG 2 (X: 3000 -> 6400): NỀN TÍM - BỤC TREO VÒNG TRẮNG & PHÁO ĐÀI LƯỚI
        # (ĐÃ SỬA TRIỆT ĐỂ HITBOX THẢM GAI MỐC 24% & XÓA GAI MỜ MỐC 35%)
        # =========================================================================
        # 2A. Thảm gai dài 1150px có Hitbox phủ kín 100% (Hình mẫu 11 & 17)
        self.hazards.append(SpikeStrip(3120, width=1150, y_bottom=GROUND_Y))

        # Nhánh trên (An toàn): 4 thanh Slab đen viền trắng có vòng tròn trắng treo bên dưới
        self.add_slab(3060, 515, cols=2, color=(150, 35, 225), ring_attach="DOWN")
        self.add_slab(3320, 440, cols=2, color=(150, 35, 225), ring_attach="DOWN")
        self.add_slab(3580, 365, cols=2, color=(150, 35, 225), ring_attach="DOWN")
        self.add_slab(3850, 290, cols=3, color=(150, 35, 225), ring_attach="DOWN")

        # [BẪY LỪA NGƯỜI CHƠI #1]: Ở dưới thấp sau Slab 2 (X=3500) có một bục phụ lắp Đệm lò xo đỏ;
        # ai không nhảy lên Slab 3 mà rơi xuống bục thấp này sẽ bị lò xo hất thẳng vào gai!
        self.add_slab(3520, 505, cols=3, color=(150, 35, 225))
        self.triggers.append(JumpPad(3570, 505, pad_color=WAVE_NEON_RED, boost_scale=0.65))
        self.hazards.append(Spike(3720, 415, direction="UP"))

        # 2B. Pháo đài lưới tím (GridBlock) bậc thang chuẩn (Hình mẫu 12 & 18)
        # Bậc 1 cao đúng 1 ô (50px, mặt trên ở y = 540) để nhảy từ mặt đất lên cực kỳ mượt
        self.add_grid_fortress(4380, GROUND_Y, cols=5, rows=1, color=(140, 25, 215), white_top=True)
        # Bậc 2 cao 2 ô (100px, mặt trên ở y = 490)
        self.add_grid_fortress(4630, GROUND_Y, cols=5, rows=2, color=(140, 25, 215), white_top=True)
        # Bậc 3 cao 3 ô (150px, mặt trên ở y = 440) kèm Gai thật ở mép phải (X=5230)
        self.add_grid_fortress(4880, GROUND_Y, cols=8, rows=3, color=(140, 25, 215), white_top=True)
        self.hazards.append(Spike(5230, 440 - TILE_SIZE, direction="UP"))

        # Bậc 4 hạ xuống 1 ô (X: 5280 -> 5780, mặt trên ở y = 540) có gai sát chân vách (X=5280)
        self.add_grid_fortress(5280, GROUND_Y, cols=10, rows=1, color=(140, 25, 215), white_top=True)
        self.hazards.append(Spike(5280, 540 - TILE_SIZE, direction="UP"))
        self.hazards.append(Spike(5630, 540 - TILE_SIZE, direction="UP"))

        # [BẪY LỪA NGƯỜI CHƠI #2 - NHÁNH ĐƯỜNG ĐÔI]:
        # Từ X=5850, người chơi thấy 1 Orb Vàng dưới thấp và 1 Đệm lò xo lên bục cao:
        # - Nhánh trên (Bục cao y=420): Đường chuẩn an toàn vượt qua hố gai.
        # - Nhánh dưới (Orb Vàng X=5980): Nhử người chơi nhảy vào hố cưa máy Sawblade!
        self.hazards.append(SpikeStrip(5850, width=500, y_bottom=GROUND_Y))
        self.triggers.append(JumpPad(5730, 540, pad_color=GOLD_YELLOW))
        self.add_slab(5920, 390, cols=4, color=(150, 35, 225), ring_attach="DOWN")
        self.add_slab(6180, 440, cols=3, color=(150, 35, 225))
        self.triggers.append(JumpOrb(5980, 510, orb_type="YELLOW_ORB", boost_scale=0.5))
        self.hazards.append(Sawblade(6160, 535, radius=38))

        # =========================================================================
        # CHƯƠNG 3 (X: 6400 -> 9600): NỀN CHÀM ĐẬM - ĐẢO NGƯỢC TRỌNG LỰC & TÊN LỬA WAVE
        # =========================================================================
        # 3A. Cổng Đảo Ngược Trọng Lực Xanh Lam tại X = 6480 (Hút nhân vật chạy lộn ngược trên trần CEILING_Y = 70!)
        self.portals.append(GravityPortal(6480, GROUND_Y - 220, target_gravity=-1))
        self.portals.append(GravityPortal(6480, GROUND_Y - 380, target_gravity=-1))

        # Chạy trên trần nhà (CEILING_Y = 70) và nhảy qua các mũi gai treo ngược chúc xuống!
        self.hazards.append(Spike(6900, CEILING_Y, direction="DOWN"))
        self.hazards.append(Spike(7250, CEILING_Y, direction="DOWN"))
        self.hazards.append(Spike(7300, CEILING_Y, direction="DOWN"))

        # Bục lưới gắn trên trần nhà giúp người chơi bước xuống thấp dần
        self.add_grid_fortress(7580, CEILING_Y + TILE_SIZE * 2, cols=5, rows=2, color=(95, 40, 235), white_top=False)
        self.hazards.append(Spike(7980, CEILING_Y, direction="DOWN"))

        # Cổng Trọng Lực Vàng tại X = 8150: Trả nhân vật rơi về mặt đất chuẩn!
        self.portals.append(GravityPortal(8150, CEILING_Y + 20, target_gravity=1))
        self.portals.append(GravityPortal(8150, CEILING_Y + 180, target_gravity=1))
        self.add_slab(8200, GROUND_Y - 70, cols=5, color=(95, 40, 235))

        # 3B. Phân đoạn Tên lửa Wave (X: 8500 -> 9450) luồn qua các trạm Cưa máy (Sawblades)
        self.portals.append(ModePortal(8480, GROUND_Y - 340, target_mode=MODE_WAVE))
        self.portals.append(ModePortal(8480, GROUND_Y - 180, target_mode=MODE_WAVE))

        self.hazards.append(Sawblade(8800, 180, radius=48, color=CYAN_LIGHT))
        self.hazards.append(Sawblade(8800, 500, radius=48, color=CYAN_LIGHT))
        self.hazards.append(Sawblade(9120, 340, radius=54, color=WAVE_TRAIL_PINK))
        self.hazards.append(Sawblade(9400, 160, radius=46, color=CYAN_LIGHT))
        self.hazards.append(Sawblade(9400, 510, radius=46, color=CYAN_LIGHT))

        # =========================================================================
        # CHƯƠNG 4 (X: 9600 -> 13600): NỀN HỒNG ĐỎ ĐẬM - ĐẠI CHIẾN LÁI MÁY BAY (SHIP MODE)
        # (TÁI HIỆN HÌNH MẪU 13 & 14 + MỞ RỘNG GẤP ĐÔI QUÃNG ĐƯỜNG BAY)
        # =========================================================================
        # Cổng biến hình sang chế độ Lái Máy Bay (MODE_SHIP) tại X = 9600
        for py in range(80, GROUND_Y - 120, 140):
            self.portals.append(ModePortal(9600, py, target_mode=MODE_SHIP))

        # 4A. Bay qua các cột lưới treo trần có vòng tròn trắng (Hình mẫu 13)
        self.add_grid_fortress(10050, 280, cols=1, rows=4, color=(205, 30, 85), white_top=False, ring_bottom=True)
        self.add_grid_fortress(10380, GROUND_Y, cols=2, rows=3, color=(205, 30, 85), white_top=True)
        self.add_grid_fortress(10720, 260, cols=1, rows=4, color=(205, 30, 85), white_top=False, ring_bottom=True)

        # 4B. Hành lang 7 gai trần & 7 gai sàn + Khối lưới gắn vòng trắng (Hình mẫu 14)
        for i in range(7):
            sx = 11050 + i * TILE_SIZE
            self.hazards.append(Spike(sx, CEILING_Y, direction="DOWN"))
            self.hazards.append(Spike(sx, GROUND_Y - TILE_SIZE, direction="UP"))

        self.blocks.append(GridBlock(11400, CEILING_Y, color=(205, 30, 85), white_edges=["ALL"], ring_attach="DOWN"))
        self.blocks.append(GridBlock(11400, GROUND_Y - TILE_SIZE, color=(205, 30, 85), white_edges=["ALL"], ring_attach="UP"))

        # 4C. Thử thách Máy bay nâng cao: Luồn qua Cưa máy xoay & Hầm hẹp zíc-zắc
        self.hazards.append(Sawblade(11780, 210, radius=46))
        self.hazards.append(Sawblade(12080, 460, radius=46))
        self.add_slab(12350, 250, cols=4, color=(205, 30, 85), ring_attach="DOWN")
        self.add_slab(12350, 450, cols=4, color=(205, 30, 85), ring_attach="UP")

        self.add_grid_fortress(12800, 240, cols=2, rows=3, color=(205, 30, 85), white_top=False, ring_bottom=True)
        self.add_grid_fortress(13150, GROUND_Y, cols=2, rows=3, color=(205, 30, 85), white_top=True)

        # =========================================================================
        # CHƯƠNG 5 (X: 13600 -> 16650): NỀN ĐỎ THẪM - CỔNG 3D VỀ CUBE & ĐƯỜNG LẮT LÉO
        # (TÁI HIỆN HÌNH MẪU 15 MỞ RỘNG)
        # =========================================================================
        # Cổng ống trụ 3D tại X = 13600 chuyển từ Máy bay về Khối vuông (MODE_CUBE)
        for py in range(90, GROUND_Y - 120, 140):
            self.portals.append(ModePortal(13600, py, target_mode=MODE_CUBE, style_3d=True))

        # Đường băng đáp rộng rãi sau cổng (X: 13620 -> 14120)
        self.add_slab(13620, GROUND_Y - 50, cols=10, color=(220, 20, 25))

        # Thảm gai nhọn dưới đáy hố dài 2400px (X: 14120 -> 16520)
        self.hazards.append(SpikeStrip(14120, width=2400, y_bottom=GROUND_Y))

        # Tổ hợp 1 (Hình mẫu 15): Bục có Vòng bật Xanh lá cắm cọc ở đầu & Gai chặn ở cuối
        self.add_slab(14180, 430, cols=3, color=(220, 20, 25))
        self.triggers.append(JumpOrb(14205, 365, orb_type="GREEN_POST_RING", post_height=65))
        self.hazards.append(Spike(14280, 430 - TILE_SIZE, direction="UP"))

        # Đáp xuống bục thấp hơn (X: 14460 -> 14660, y = 485)
        self.add_slab(14460, 485, cols=4, color=(220, 20, 25))

        # Tổ hợp 2: Bật liên hoàn qua 2 Vòng Xanh lá + Đệm lò xo trên không
        self.triggers.append(JumpOrb(14820, 390, orb_type="GREEN_POST_RING"))
        self.add_slab(14980, 350, cols=3, color=(220, 20, 25), ring_attach="DOWN")
        self.triggers.append(JumpPad(15080, 350, pad_color=GOLD_YELLOW, boost_scale=0.88))

        self.add_slab(15350, 290, cols=3, color=(220, 20, 25))
        self.hazards.append(Spike(15450, 290 - TILE_SIZE, direction="UP"))
        self.add_slab(15620, 410, cols=4, color=(220, 20, 25))

        # Tổ hợp 3: Bục có Vòng bật Xanh lá thứ hai dẫn thẳng tới Khe Cổng 3D (Hình mẫu 15)
        self.add_slab(15920, 420, cols=3, color=(220, 20, 25))
        self.triggers.append(JumpOrb(15945, 355, orb_type="GREEN_POST_RING", post_height=65))
        self.hazards.append(Spike(16020, 420 - TILE_SIZE, direction="UP"))

        self.add_slab(16200, 475, cols=4, color=(220, 20, 25))

        # =========================================================================
        # CHƯƠNG 6 (X: 16650 -> 18000): CỔNG HỒNG 3D BIẾN HÌNH THÀNH MÁY BAY & PHÁ ĐẢO
        # (SỬA LỖI MỐC 92%: CỔNG CHUYỂN SANG MÁY BAY ĐỂ BAY QUA KHỐI CHỮ L VÀO ĐÍCH!)
        # =========================================================================
        # Cột dưới 3 tầng & Cột trên 2 tầng có gắn vòng tròn bên sườn phải (Hình mẫu 15 & 19)
        for r in range(3):
            attach = "RIGHT" if r in (1, 2) else None
            self.blocks.append(ClassicDarkBlock(16650, GROUND_Y - (r + 1) * TILE_SIZE, color=(220, 20, 25), ring_attach=attach))
        for r in range(2):
            self.blocks.append(ClassicDarkBlock(16650, CEILING_Y + r * TILE_SIZE, color=(220, 20, 25), ring_attach="RIGHT"))

        # Chiếc Cổng Hồng 3D nằm giữa khe cột nay là ModePortal(target_mode=MODE_SHIP)!
        # Khi người chơi nhảy qua khe cột chạm vào cổng sẽ lập tức biến thành Máy bay phản lực!
        self.portals.append(ModePortal(16635, 235, target_mode=MODE_SHIP, style_3d=True))
        self.portals.append(ModePortal(16635, 350, target_mode=MODE_SHIP, style_3d=True))

        # Các bục trang trí và cụm khối chữ L trước vạch đích (Hình mẫu 16 & 19)
        # Nhờ đã biến thành Máy bay ở cổng 16635, Thái tử có thể lượn mượt mà qua đỉnh khối chữ L!
        self.add_slab(16850, 470, cols=3, color=(220, 20, 25))
        self.add_dark_blocks(17250, GROUND_Y, cols=2, rows=1, color=(220, 20, 25))
        self.add_dark_blocks(17350, GROUND_Y, cols=1, rows=4, color=(220, 20, 25))

        # Cổng năng lượng trang trí dẫn thẳng vào Bức tường Ánh sáng Chiến thắng ở X = 18000
        self.add_slab(17620, 220, cols=2, color=(220, 20, 25), ring_attach="DOWN")
        self.add_slab(17620, 480, cols=2, color=(220, 20, 25), ring_attach="UP")