"""
===================================================================
 Gelişmiş Yılan Oyunu (Power-up Snake)
-------------------------------------------------------------------
 Bu proje, standart Yılan Oyunu mantığını modern görsel efektler,
 özel güçlendirici yemler (Buz, Altın Elma, Hayalet Modu, Turbo)
 ve ses sentezleme teknolojisi ile harmanlayan öğretim amaçlı bir oyundur.

 Kullanılan Teknolojiler: Python 3, Pygame
===================================================================
"""

import os
import sys
import json
import math
import random
import pygame

from config import (
    GRID_WIDTH, GRID_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SPEED_EASY, SPEED_MEDIUM, SPEED_HARD, POWERUP_TYPES, POWERUP_SPAWN_LIFETIME,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT
)
from models import Snake, FoodItem, Particle, FloatingText
from sound_manager import SoundManager
from ui_manager import UIManager


class PowerUpSnakeGame:
    """Ana Oyun Yöneticisi Sınıfı."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("🐍 Power-up Snake - Gelişmiş Yılan Oyunu")

        # Ekran Oluşturma
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Alt Sistemler
        self.sound = SoundManager()
        self.ui = UIManager(self.screen)

        # Rekor Skor Dosyası
        self.highscore_file = os.path.join(os.path.dirname(__file__), "highscore.json")
        self.high_score = self._load_high_score()

        # Oyun Durumu (MENU, PLAYING, PAUSED, GAME_OVER)
        self.state = "MENU"
        self.difficulty = "MEDIUM" # Varsayılan Zorluk: Orta

        # Oyun Mantığı Değişkenleri
        self.snake = None
        self.foods = []
        self.particles = []
        self.floating_texts = []
        
        self.score = 0
        self.is_new_record = False
        
        # Hareket Zamanlayıcısı (Delta Time Accumulator)
        self.move_timer = 0.0
        self.special_spawn_timer = 0.0

        # Oyunu Başlat
        self._reset_game()

    def _load_high_score(self):
        """Kaydedilmiş en yüksek skoru yükler."""
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except Exception:
                return 0
        return 0

    def _save_high_score(self):
        """En yüksek skoru yerel JSON dosyasına kaydeder."""
        try:
            with open(self.highscore_file, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception as e:
            print(f"[Hata] Rekor kaydedilemedi: {e}")

    def _reset_game(self):
        """Yeni bir oyun turu için tüm nesneleri sıfırlar."""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = Snake(start_x, start_y)
        
        self.foods = []
        self.particles = []
        self.floating_texts = []
        self.score = 0
        self.is_new_record = False
        self.move_timer = 0.0
        self.special_spawn_timer = 0.0

        # 1 Adet Normal Kırmızı Elma Oluştur
        self._spawn_food(p_type='NORMAL')

    def _get_random_free_cell(self):
        """Yılanın üzerinde bulunmadığı boş bir ızgara hücresi seçer."""
        occupied = set(self.snake.body)
        for food in self.foods:
            occupied.add(food.pos)
            
        free_cells = [
            (x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        
        if free_cells:
            return random.choice(free_cells)
        return (0, 0)

    def _spawn_food(self, p_type='NORMAL'):
        """Belirtilen tipte yeni bir yem üretir."""
        x, y = self._get_random_free_cell()
        lifetime = 0 if p_type == 'NORMAL' else POWERUP_SPAWN_LIFETIME
        food = FoodItem(x, y, p_type=p_type, lifetime=lifetime)
        self.foods.append(food)

    def _spawn_particles(self, gx, gy, color, count=15):
        """Yem yendiğinde patlayan renkli kıvılcımlar üretir."""
        px = gx * 30 + 15
        py = 90 + (gy * 30) + 15 # HUD Offset + Y-center
        
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(40, 160)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.uniform(3, 7)
            lifetime = random.uniform(0.3, 0.7)
            
            p = Particle(px, py, color, vx, vy, size, lifetime)
            self.particles.append(p)

    def _add_floating_text(self, text, gx, gy, color):
        """Ekranda yukarı kayan puan yazısı oluşturur."""
        px = gx * 30
        py = 90 + (gy * 30) - 10
        ft = FloatingText(text, px, py, color)
        self.floating_texts.append(ft)

    def run(self):
        """Ana Oyun Döngüsü (Main Game Loop)."""
        running = True
        while running:
            # Delta Time (Geçen süre - saniye)
            dt = self.clock.tick(FPS) / 1000.0

            # 1. Olayları Dinle (Event Handling)
            running = self._handle_events()

            # 2. Mantık Güncelleme (Game Logic Update)
            if self.state == "PLAYING":
                self._update_game(dt)

            # 3. Ekranı Çiz (Rendering)
            self._render()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Kullanıcı tuş ve fare girdilerini işler."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Ses Aç / Kapat
                if event.key == pygame.K_m and self.state != "GAME_OVER":
                    self.sound.toggle_mute()

                # MENÜ EKRANI TUŞLARI
                if self.state == "MENU":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._reset_game()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_1:
                        self.difficulty = "EASY"
                    elif event.key == pygame.K_2:
                        self.difficulty = "MEDIUM"
                    elif event.key == pygame.K_3:
                        self.difficulty = "HARD"

                # OYUN EKRANI TUŞLARI
                elif self.state == "PLAYING":
                    # Yön Kontrolleri (Ok Tuşları veya WASD)
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(DIR_UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DIR_DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(DIR_LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(DIR_RIGHT)
                    elif event.key in (pygame.K_SPACE, pygame.K_p):
                        self.state = "PAUSED"

                # DURAKLATMA EKRANI TUŞLARI
                elif self.state == "PAUSED":
                    if event.key in (pygame.K_SPACE, pygame.K_p):
                        self.state = "PLAYING"

                # OYUN BİTTİ EKRANI TUŞLARI
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self._reset_game()
                        self.state = "PLAYING"
                    elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                        self.state = "MENU"

            # Fare Tıklama Kontrolü (Menü seçenekleri için)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.state == "MENU":
                    # Zorluk Butonları Tıklama Alanları
                    diff_y = 505
                    if diff_y <= my <= diff_y + 45:
                        if SCREEN_WIDTH // 2 - 210 <= mx <= SCREEN_WIDTH // 2 - 80:
                            self.difficulty = "EASY"
                        elif SCREEN_WIDTH // 2 - 65 <= mx <= SCREEN_WIDTH // 2 + 65:
                            self.difficulty = "MEDIUM"
                        elif SCREEN_WIDTH // 2 + 80 <= mx <= SCREEN_WIDTH // 2 + 210:
                            self.difficulty = "HARD"
                            
                    # Başlat Butonu Tıklama
                    if 570 <= my <= 620:
                        self._reset_game()
                        self.state = "PLAYING"

        return True

    def _get_current_speed(self):
        """Seçilen zorluğa ve aktif güçlendirmeye göre yılanın adım hızını verir."""
        base_speed = SPEED_MEDIUM
        if self.difficulty == "EASY":
            base_speed = SPEED_EASY
        elif self.difficulty == "HARD":
            base_speed = SPEED_HARD
            
        # Yılanın güçlendirme hız çarpanı (Örn: Buz yavaşlatır, Turbo hızlandırır)
        return base_speed * self.snake.get_speed_multiplier()

    def _update_game(self, dt):
        """Oyun durumunu ve nesneleri kare kare günceller."""
        # 1. Yılanın Güçlendirme Sürelerini Azalt
        self.snake.update_powerups(dt)

        # 2. Yemlerin ve Güçlendirmelerin Ekranda Kalma Sürelerini Güncelle
        active_foods = []
        for food in self.foods:
            if food.update(dt):
                active_foods.append(food)
        self.foods = active_foods

        # Eğer ekranda hiç normal elma kalmadıysa yenisini ekle
        if not any(f.type == 'NORMAL' for f in self.foods):
            self._spawn_food('NORMAL')

        # 3. Rastgele Özel Güçlendirme Yemi Çıkarma Zamanlayıcısı
        self.special_spawn_timer += dt
        if self.special_spawn_timer >= 8.0: # Her 8 saniyede bir şans kontrolü
            self.special_spawn_timer = 0.0
            # Ekranda 2'den fazla yem yoksa ve %70 şansla özel yem üret
            if len(self.foods) < 3 and random.random() < 0.70:
                p_type = random.choice(['ICE', 'GOLD', 'GHOST', 'TURBO'])
                self._spawn_food(p_type)

        # 4. Parçacık ve Metin Efektlerini Güncelle
        self.particles = [p for p in self.particles if p.update(dt)]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

        # 5. Yılan Hareketi Zamanlaması
        step_interval = 1.0 / self._get_current_speed()
        self.move_timer += dt

        if self.move_timer >= step_interval:
            self.move_timer -= step_interval
            
            # Yılanı 1 Kare Hareket Ettir
            self.snake.move(GRID_WIDTH, GRID_HEIGHT)

            # Çarpmaları Kontrol Et
            self._check_collisions()

    def _check_collisions(self):
        """Yılanın yemlerle, duvarlarla ve kendisiyle çarpışmalarını yönetir."""
        head_pos = self.snake.head

        # A) Duvar Çarpışması Kontrolü (Hayalet modunda serbesttir)
        if self.snake.check_wall_collision(GRID_WIDTH, GRID_HEIGHT):
            self._trigger_game_over()
            return

        # B) Kendi Kuyruğuna Çarpma Kontrolü (Hayalet modunda serbesttir)
        if self.snake.check_self_collision():
            self._trigger_game_over()
            return

        # C) Yem Yeme Kontrolü
        eaten_food = None
        for food in self.foods:
            if food.pos == head_pos:
                eaten_food = food
                break

        if eaten_food:
            self.foods.remove(eaten_food)
            p_config = POWERUP_TYPES.get(eaten_food.type, POWERUP_TYPES['NORMAL'])

            # Puan Hesaplama
            base_score = p_config['score']
            
            # Altın 2X çarpanı aktif mi?
            score_mult = 1.0
            if self.snake.is_gold():
                score_mult *= 2.0
            if p_config.get('score_multiplier'):
                score_mult *= p_config['score_multiplier']

            final_points = int(base_score * score_mult)
            self.score += final_points

            # Yılanı Büyüt ve Güçlendirmeyi Ekle
            self.snake.grow(1)
            if p_config['duration'] > 0:
                self.snake.add_powerup(eaten_food.type, p_config['duration'])

            # Ses Çal
            sound_key = eaten_food.type.lower()
            self.sound.play(sound_key)

            # Görsel Parçacık ve Yüzen Skor Yazısı
            self._spawn_particles(eaten_food.x, eaten_food.y, p_config['color'], count=20)
            txt_str = f"+{final_points}"
            if score_mult > 1.0:
                txt_str += " (2X!)"
            self._add_floating_text(txt_str, eaten_food.x, eaten_food.y, p_config['color'])

            # Eğer yenen normal elma ise hemen yenisini üret
            if eaten_food.type == 'NORMAL':
                self._spawn_food('NORMAL')

    def _trigger_game_over(self):
        """Oyun bitti durumunu tetikler."""
        self.state = "GAME_OVER"
        self.sound.play('game_over')

        # Rekor Kontrolü
        if self.score > self.high_score:
            self.high_score = self.score
            self.is_new_record = True
            self._save_high_score()

    def _render(self):
        """Ekranı ve tüm bileşenleri çizer."""
        # 1. Izgara ve Arka Plan
        self.ui.draw_grid()

        # 2. Yemler ve Güçlendirmeler
        self.ui.draw_foods(self.foods)

        # 3. Yılan
        if self.snake:
            self.ui.draw_snake(self.snake)

        # 4. Efektler (Parçacıklar ve Yüzen Metinler)
        self.ui.draw_particles(self.particles)
        self.ui.draw_floating_texts(self.floating_texts)

        # 5. Üst Bilgi Paneli (HUD)
        self.ui.draw_hud(self.score, self.high_score, self.snake, self.sound.muted)

        # 6. Duruma Özel Ekran Kaplamaları (Overlays)
        if self.state == "MENU":
            self.ui.draw_menu(self.high_score, self.difficulty)
        elif self.state == "PAUSED":
            self.ui.draw_pause()
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.score, self.high_score, self.is_new_record)

        # Ekranı Güncelle
        pygame.display.flip()


if __name__ == "__main__":
    game = PowerUpSnakeGame()
    game.run()
