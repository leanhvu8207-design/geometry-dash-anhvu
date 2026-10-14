# player/modes.py
import math
from config import *


class MovementMode:
    """Lớp cơ sở trừu tượng (Abstract Base Class) cho mọi chế độ di chuyển của Nhân vật."""

    mode_name = MODE_CUBE

    def on_enter(self, player, wave_trail, ship_trail):
        player.angle = 0.0

    def update_physics(self, player, dt, is_holding, just_pressed, blocks, triggers, corridors, wave_trail, ship_trail, particles):
        raise NotImplementedError


class CubeMode(MovementMode):
    """Logic vật lý chế độ Khối vuông (Hỗ trợ cả Trọng lực thuận +1 và Trọng lực ngược -1)."""

    mode_name = MODE_CUBE

    def update_physics(self, player, dt, is_holding, just_pressed, blocks, triggers, corridors, wave_trail, ship_trail, particles):
        g_dir = player.gravity_dir  # +1: rơi xuống đất | -1: hút lên trần
        prev_bottom = player.y + player.h
        prev_top = player.y

        # 1. Kiểm tra tương tác với các Trigger (Đệm lò xo JumpPad tự bật, hoặc Vòng JumpOrb khi bấm)
        for trig in triggers:
            if not trig.activated and player.rect.colliderect(trig.rect):
                if trig.auto_trigger or (is_holding and (just_pressed or not player.on_ground)):
                    trig.apply_effect(player, particles)
                    break

        # 2. Nhảy cơ bản khi đang đứng trên bề mặt
        if player.on_ground and is_holding:
            player.vel_y = CUBE_JUMP_VEL * g_dir
            player.on_ground = False

        # 3. Áp dụng gia tốc trọng trường theo chiều gravity_dir
        player.vel_y += (CUBE_GRAVITY * g_dir) * dt
        player.y += player.vel_y * dt
        player.on_ground = False

        # 4. Va chạm với Mặt đất hoặc Trần (khi đảo ngược trọng lực)
        if g_dir > 0:
            if player.y + player.h >= GROUND_Y:
                player.y = GROUND_Y - player.h
                player.vel_y = 0.0
                player.on_ground = True
            if player.y < -60:
                player.is_dead = True
                return
        else:
            if player.y <= CEILING_Y:
                player.y = CEILING_Y
                player.vel_y = 0.0
                player.on_ground = True
            if player.y + player.h > GROUND_Y:
                player.is_dead = True
                return

        # 5. Va chạm với các khối SolidBlock
        p_rect = player.rect
        for blk in blocks:
            if not blk.is_visible(player.x - 260):
                continue
            if p_rect.colliderect(blk.rect):
                if g_dir > 0 and prev_bottom <= blk.rect.top + 18 and player.vel_y >= 0:
                    player.y = blk.rect.top - player.h
                    player.vel_y = 0.0
                    player.on_ground = True
                    p_rect = player.rect
                elif g_dir < 0 and prev_top >= blk.rect.bottom - 18 and player.vel_y <= 0:
                    player.y = blk.rect.bottom
                    player.vel_y = 0.0
                    player.on_ground = True
                    p_rect = player.rect
                else:
                    player.is_dead = True
                    return

        # 6. Xoay góc Cube và sinh hạt bụi
        if not player.on_ground:
            player.angle = (player.angle - 380.0 * g_dir * dt) % 360.0
        else:
            target_angle = round(player.angle / 90.0) * 90.0
            player.angle += (target_angle - player.angle) * min(1.0, dt * 22.0)
            if int(player.x) % 3 == 0:
                ty = (player.y + player.h - 4) if g_dir > 0 else (player.y + 4)
                particles.spawn_trail(player.x + 6, ty, player.skin.trail_color)


class ShipMode(MovementMode):
    """Logic vật lý chế độ Lái Máy Bay (Phản lực mượt, trượt được trên trần & sàn)."""

    mode_name = MODE_SHIP

    def on_enter(self, player, wave_trail, ship_trail):
        player.angle = 0.0
        ship_trail.clear()

    def update_physics(self, player, dt, is_holding, just_pressed, blocks, triggers, corridors, wave_trail, ship_trail, particles):
        g_dir = player.gravity_dir
        prev_bottom = player.y + player.h
        prev_top = player.y

        # Cho phép máy bay ăn Orb hoặc chạm JumpPad
        for trig in triggers:
            if not trig.activated and player.rect.colliderect(trig.rect):
                if trig.auto_trigger or (is_holding and just_pressed):
                    trig.apply_effect(player, particles)
                    break

        accel = (SHIP_THRUST if is_holding else SHIP_GRAVITY) * g_dir
        player.vel_y += accel * dt
        player.vel_y = max(-SHIP_MAX_VEL_Y, min(SHIP_MAX_VEL_Y, player.vel_y))
        player.y += player.vel_y * dt

        player.on_ground = False
        if player.y <= CEILING_Y:
            player.y = CEILING_Y
            player.vel_y = max(0.0, player.vel_y)
            if g_dir < 0:
                player.on_ground = True
        if player.y + player.h >= GROUND_Y:
            player.y = GROUND_Y - player.h
            player.vel_y = min(0.0, player.vel_y)
            if g_dir > 0:
                player.on_ground = True

        p_rect = player.rect
        for blk in blocks:
            if not blk.is_visible(player.x - 260):
                continue
            if p_rect.colliderect(blk.rect):
                if prev_bottom <= blk.rect.top + 16 and player.vel_y >= 0:
                    player.y = blk.rect.top - player.h
                    player.vel_y = 0.0
                    player.on_ground = True
                    p_rect = player.rect
                elif prev_top >= blk.rect.bottom - 16 and player.vel_y <= 0:
                    player.y = blk.rect.bottom
                    player.vel_y = 0.0
                    p_rect = player.rect
                else:
                    player.is_dead = True
                    return

        target_angle = max(-28.0, min(28.0, -player.vel_y * 0.055))
        if player.on_ground:
            target_angle = 0.0
        player.angle += (target_angle - player.angle) * min(1.0, dt * 14.0)

        rad = math.radians(player.angle)
        nozzle_x = player.x + 6 - math.cos(rad) * 10
        nozzle_y = player.y + player.h // 2 + 4 + math.sin(rad) * 10
        ship_trail.add_point(nozzle_x, nozzle_y)
        if int(player.x) % 2 == 0:
            particles.spawn_ship_sparks(nozzle_x, nozzle_y)


class WaveMode(MovementMode):
    """Logic vật lý chế độ Tên lửa / Mũi tên zíc-zắc 45 độ."""

    mode_name = MODE_WAVE

    def on_enter(self, player, wave_trail, ship_trail):
        player.angle = 0.0
        wave_trail.clear()
        wave_trail.add_point(player.x + player.w // 2, player.y + player.h // 2)

    def update_physics(self, player, dt, is_holding, just_pressed, blocks, triggers, corridors, wave_trail, ship_trail, particles):
        g_dir = player.gravity_dir
        player.vel_y = (-WAVE_SPEED_Y if is_holding else WAVE_SPEED_Y) * g_dir
        player.y += player.vel_y * dt
        player.angle = (35.0 if is_holding else -35.0) * g_dir

        wave_trail.add_point(player.x + player.w // 2, player.y + player.h // 2)

        # Kiểm tra chạm trần/sàn hoặc hành lang Wave
        if player.y <= 10 or player.y + player.h >= SCREEN_HEIGHT - 10:
            player.is_dead = True
            return

        for cor in corridors:
            if cor.check_collision(player.rect):
                player.is_dead = True
                return

        p_rect = player.rect
        for blk in blocks:
            if blk.is_visible(player.x - 260) and p_rect.colliderect(blk.rect):
                player.is_dead = True
                return