"""
Gelişmiş Yılan Oyunu - Görsel Arayüz Yöneticisi (UI Manager)
------------------------------------------------------------
Bu modül tüm çizim (rendering), ızgara görünümü, yılan görselleri,
güçlendirme efektleri, HUD paneli ve menü ekranlarını yönetir.
Pygame Surface, Alpha Blending ve Matris Çizim teknolojilerini öğretir.
"""

import math
import pygame
from config import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT,
    HUD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, COLOR_GRID, COLOR_HUD_BG,
    COLOR_BORDER, COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_SNAKE_EYE, COLOR_SNAKE_PUPIL,
    COLOR_FOOD_NORMAL, COLOR_POWERUP_GOLD, COLOR_POWERUP_ICE, COLOR_POWERUP_GHOST, COLOR_POWERUP_TURBO,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_ACCENT, POWERUP_TYPES
)

class UIManager:
    """Çizim işlemlerini ve kullanıcı arayüzünü yöneten sınıf."""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Sistem Yazı Tipleri (Fonts)
        self.font_title = pygame.font.SysFont('arial', 36, bold=True)
        self.font_header = pygame.font.SysFont('arial', 24, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 18, bold=True)
        self.font_small = pygame.font.SysFont('arial', 14)

    def draw_grid(self):
        """Oyun alanının arka planını ve neon ızgara çizgilerini çizer."""
        # 1. Arka Plan
        play_rect = pygame.Rect(0, HUD_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_BG, play_rect)
        
        # 2. Izgara Çizgileri
        for x in range(0, PLAY_AREA_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, HUD_HEIGHT), (x, SCREEN_HEIGHT))
        for y in range(HUD_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (PLAY_AREA_WIDTH, y))

        # 3. Oyun Alanı Kenarlığı (Border)
        pygame.draw.rect(self.screen, COLOR_BORDER, play_rect, 2)

    def grid_to_screen(self, gx, gy):
        """Izgara koordinatlarını (x, y) piksel ekran koordinatlarına dönüştürür."""
        px = gx * GRID_SIZE
        py = HUD_HEIGHT + (gy * GRID_SIZE)
        return px, py

    def draw_snake(self, snake):
        """
        Yılanı, başını, gözlerini ve aktif güçlendirme haresini çizer.
        Öğrencilerin geometri ve açı matematiklerini anlamasına yardımcı olur.
        """
        is_ghost = snake.is_ghost()
        is_ice = snake.is_ice()
        is_gold = snake.is_gold()
        is_turbo = snake.is_turbo()

        # Saydamlık Matrisi (Hayalet Modunda yılan %50 saydam olur)
        alpha = 130 if is_ghost else 255
        
        # Güçlendirme Halesi Rengi
        aura_color = None
        if is_ghost:
            aura_color = (155, 89, 182, 100) # Mor
        elif is_gold:
            aura_color = (241, 196, 15, 120)  # Altın Sarı
        elif is_ice:
            aura_color = (52, 152, 219, 120)  # Buz Mavi
        elif is_turbo:
            aura_color = (230, 126, 34, 120) # Turbo Turuncu

        # 1. Gövde Çizimi (Sondan başa doğru tapering - daralma)
        body_len = len(snake.body)
        for index, (gx, gy) in enumerate(reversed(snake.body)):
            real_index = body_len - 1 - index
            px, py = self.grid_to_screen(gx, gy)
            
            # Baş kısım dışındakiler gövdedir
            if real_index > 0:
                # Segment boyutu hafifçe daralır
                shrink = max(0, int(3 * (real_index / body_len)))
                rect = pygame.Rect(
                    px + shrink + 2,
                    py + shrink + 2,
                    GRID_SIZE - (shrink * 2) - 4,
                    GRID_SIZE - (shrink * 2) - 4
                )
                
                # Gövde Rengi
                base_color = COLOR_SNAKE_BODY
                if is_gold:
                    base_color = (243, 156, 18)
                elif is_ice:
                    base_color = (41, 128, 185)
                elif is_ghost:
                    base_color = (142, 68, 173)

                # Şeffaf Çizim Yüzeyi (Surface)
                segment_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(
                    segment_surface,
                    (*base_color, alpha),
                    (shrink + 2, shrink + 2, GRID_SIZE - (shrink * 2) - 4, GRID_SIZE - (shrink * 2) - 4),
                    border_radius=8
                )
                
                # Eğer güçlendirme varsa etrafına halka çiz
                if aura_color:
                    pygame.draw.rect(
                        segment_surface,
                        aura_color,
                        (0, 0, GRID_SIZE, GRID_SIZE),
                        width=2,
                        border_radius=10
                    )

                self.screen.blit(segment_surface, (px, py))

        # 2. Baş Çizimi (Head)
        hx, hy = snake.head
        px, py = self.grid_to_screen(hx, hy)
        
        head_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        
        # Baş Taban Rengi
        head_color = COLOR_SNAKE_HEAD
        if is_gold:
            head_color = (241, 196, 15)
        elif is_ice:
            head_color = (52, 152, 219)
        elif is_ghost:
            head_color = (155, 89, 182)

        # Baş Oval Daire/Dikdörtgen Çizimi
        pygame.draw.rect(
            head_surface,
            (*head_color, alpha),
            (2, 2, GRID_SIZE - 4, GRID_SIZE - 4),
            border_radius=12
        )
        
        # Halka / Aura efekti
        if aura_color:
            pygame.draw.rect(
                head_surface,
                aura_color,
                (0, 0, GRID_SIZE, GRID_SIZE),
                width=3,
                border_radius=14
            )

        # 3. Yılan Gözleri (Hareket yönüne bakar)
        dx, dy = snake.direction
        eye_radius = 4
        pupil_radius = 2
        
        # Göz pozisyonları (Bakış açısına göre ötelenir)
        if dx == 1:   # Sağa
            e1 = (GRID_SIZE - 8, 8)
            e2 = (GRID_SIZE - 8, GRID_SIZE - 8)
        elif dx == -1: # Sola
            e1 = (8, 8)
            e2 = (8, GRID_SIZE - 8)
        elif dy == -1: # Yukarı
            e1 = (8, 8)
            e2 = (GRID_SIZE - 8, 8)
        else:          # Aşağı
            e1 = (8, GRID_SIZE - 8)
            e2 = (GRID_SIZE - 8, GRID_SIZE - 8)

        # Göz Akı & Bebeği Çiz
        for ex, ey in [e1, e2]:
            pygame.draw.circle(head_surface, (*COLOR_SNAKE_EYE, alpha), (ex, ey), eye_radius)
            pygame.draw.circle(head_surface, (*COLOR_SNAKE_PUPIL, alpha), (ex + dx, ey + dy), pupil_radius)

        self.screen.blit(head_surface, (px, py))

    def draw_foods(self, foods):
        """Ekranda aktif olan normal yem ve güçlendirme nesnelerini çizer."""
        for food in foods:
            px, py = self.grid_to_screen(food.x, food.y)
            p_config = POWERUP_TYPES.get(food.type, POWERUP_TYPES['NORMAL'])
            color = p_config['color']

            # Canlı Dalgalanma / Yanıp Sönme Animasyonu (Pulse)
            pulse = math.sin(food.anim_phase) * 3.0
            radius = int((GRID_SIZE // 2) - 3 + pulse)
            center_x = px + (GRID_SIZE // 2)
            center_y = py + (GRID_SIZE // 2)

            if food.type == 'NORMAL':
                # 🍏 Elma Şekli
                pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
                # Küçük Yaprak
                pygame.draw.ellipse(self.screen, (46, 204, 113), (center_x, center_y - radius - 2, 6, 4))
                
            elif food.type == 'ICE':
                # 🧊 Buz Kristali (Baklava / Elmas Şekli)
                pts = [
                    (center_x, center_y - radius - 2),
                    (center_x + radius + 2, center_y),
                    (center_x, center_y + radius + 2),
                    (center_x - radius - 2, center_y)
                ]
                pygame.draw.polygon(self.screen, color, pts)
                pygame.draw.polygon(self.screen, (255, 255, 255), pts, width=2)
                
            elif food.type == 'GOLD':
                # 🌟 Altın Yıldız / Parlak Elma
                pygame.draw.circle(self.screen, color, (center_x, center_y), radius + 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), radius - 3, width=2)
                
            elif food.type == 'GHOST':
                # 👻 Hayalet Sembolü (Yarım Daire + Etek)
                ghost_rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
                pygame.draw.ellipse(self.screen, color, ghost_rect)
                # Küçük Gözler
                pygame.draw.circle(self.screen, (255, 255, 255), (center_x - 4, center_y - 2), 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (center_x + 4, center_y - 2), 2)
                
            elif food.type == 'TURBO':
                # ⚡ Turbo Yıldırım Şekli
                pygame.draw.circle(self.screen, color, (center_x, center_y), radius + 1)
                bolt_pts = [
                    (center_x + 2, center_y - radius),
                    (center_x - radius, center_y + 1),
                    (center_x, center_y + 1),
                    (center_x - 2, center_y + radius),
                    (center_x + radius, center_y - 1),
                    (center_x, center_y - 1)
                ]
                pygame.draw.polygon(self.screen, (255, 255, 255), bolt_pts)

            # Eğer güçlendirmenin kalan kalma süresi varsa etrafında dairesel geri sayım barı çiz
            if food.lifetime > 0:
                ratio = max(0.0, food.lifetime / food.max_lifetime)
                arc_rect = pygame.Rect(px - 2, py - 2, GRID_SIZE + 4, GRID_SIZE + 4)
                pygame.draw.arc(self.screen, color, arc_rect, 0, math.pi * 2 * ratio, width=2)

    def draw_particles(self, particles):
        """Parçacık efektlerini şeffaflıkla çizer."""
        for p in particles:
            alpha = int(255 * p.alpha_ratio)
            if alpha > 0:
                p_surf = pygame.Surface((int(p.size * 2), int(p.size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(p_surf, (*p.color, alpha), (int(p.size), int(p.size)), int(p.size))
                self.screen.blit(p_surf, (p.x - p.size, p.y - p.size))

    def draw_floating_texts(self, texts):
        """Drifting float metinlerini çizer."""
        for ft in texts:
            alpha = ft.alpha
            if alpha > 0:
                txt_surf = self.font_medium.render(ft.text, True, ft.color)
                txt_surf.set_alpha(alpha)
                self.screen.blit(txt_surf, (ft.x, ft.y))

    def draw_hud(self, score, high_score, snake, is_muted):
        """Üst bilgi panelini (HUD), skorları ve aktif güçlendirme geri sayım barlarını çizer."""
        # HUD Paneli Arka Planı
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_HUD_BG, hud_rect)
        pygame.draw.line(self.screen, COLOR_BORDER, (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 2)

        # 1. Skor Bilgileri
        score_txt = self.font_header.render(f"SKOR: {score}", True, COLOR_TEXT_MAIN)
        high_txt = self.font_medium.render(f"REKOR: {high_score}", True, COLOR_ACCENT)
        self.screen.blit(score_txt, (20, 15))
        self.screen.blit(high_txt, (20, 48))

        # 2. Ses Durumu Simgesi
        sound_str = "🔊 [M] SES: AÇIK" if not is_muted else "🔇 [M] SES: KAPALI"
        sound_txt = self.font_small.render(sound_str, True, COLOR_TEXT_MUTED)
        self.screen.blit(sound_txt, (SCREEN_WIDTH - 150, 15))

        # 3. Aktif Güçlendirme Göstergeleri (Countdown Gauge Bars)
        start_x = 220
        bar_width = 120
        bar_height = 16
        gap = 130
        
        col_idx = 0
        for p_type, time_left in snake.active_powerups.items():
            p_config = POWERUP_TYPES.get(p_type)
            if not p_config or p_config['duration'] <= 0:
                continue
                
            bx = start_x + (col_idx * gap)
            by = 40
            col_idx += 1
            
            # Kalan Süre Oranı
            ratio = max(0.0, time_left / p_config['duration'])
            
            # Etiket
            label = self.font_small.render(f"{p_config['icon']} {p_config['name'][:8]}: {time_left:.1f}s", True, p_config['color'])
            self.screen.blit(label, (bx, by - 22))
            
            # Bar Çerçevesi
            bg_bar = pygame.Rect(bx, by, bar_width, bar_height)
            pygame.draw.rect(self.screen, (30, 40, 60), bg_bar, border_radius=4)
            
            # İç Doygunluk Barı
            if ratio > 0:
                fill_width = int(bar_width * ratio)
                fill_bar = pygame.Rect(bx, by, fill_width, bar_height)
                pygame.draw.rect(self.screen, p_config['color'], fill_bar, border_radius=4)
            pygame.draw.rect(self.screen, COLOR_BORDER, bg_bar, width=1, border_radius=4)

    def draw_menu(self, high_score, selected_difficulty):
        """Başlangıç ve Zorluk Seçim Menüsü."""
        # Yarı saydam koyu overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 12, 22, 245))
        self.screen.blit(overlay, (0, 0))

        # Başlıklar
        title = self.font_title.render("🐍 POWER-UP SNAKE", True, COLOR_ACCENT)
        subtitle = self.font_medium.render("Gelişmiş Özel Yemli Yılan Oyunu", True, COLOR_TEXT_MUTED)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 130))

        # Rekor Skor Gösterimi
        hs_txt = self.font_header.render(f"En Yüksek Rekor: {high_score}", True, COLOR_POWERUP_GOLD)
        self.screen.blit(hs_txt, (SCREEN_WIDTH // 2 - hs_txt.get_width() // 2, 180))

        # Güçlendirmeler Rehberi Kutusunu Çiz
        guide_box = pygame.Rect(SCREEN_WIDTH // 2 - 260, 230, 520, 210)
        pygame.draw.rect(self.screen, (20, 28, 45), guide_box, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_BORDER, guide_box, width=2, border_radius=12)

        guide_title = self.font_header.render("✨ ÖZEL YEMLER VE GÜÇLER", True, COLOR_TEXT_MAIN)
        self.screen.blit(guide_title, (SCREEN_WIDTH // 2 - guide_title.get_width() // 2, 242))

        items = [
            ("🍏 Elma", "+10 Puan & Uzama"),
            ("🧊 Buz Yemi", "Yılanı %40 Yavaşlatır (Kontrol Kolaylığı)"),
            ("🌟 Altın Elma", "+50 Puan & 8 Saniye 2X SKOR Çarpanı"),
            ("👻 Hayalet", "Duvarlardan ve Kendi İçinden Geçiş"),
            ("⚡ Turbo Hız", "Hızlı Depar & Extra Puan"),
        ]

        for i, (icon_name, desc) in enumerate(items):
            iy = 280 + (i * 28)
            p_type_key = ['NORMAL', 'ICE', 'GOLD', 'GHOST', 'TURBO'][i]
            col = POWERUP_TYPES[p_type_key]['color']
            
            lbl = self.font_medium.render(icon_name, True, col)
            dsc = self.font_small.render(desc, True, COLOR_TEXT_MAIN)
            self.screen.blit(lbl, (SCREEN_WIDTH // 2 - 240, iy))
            self.screen.blit(dsc, (SCREEN_WIDTH // 2 - 80, iy + 3))

        # Zorluk Seçenekleri
        diff_txt = self.font_header.render("ZORLUK SEÇİNİ (1-2-3 Tuşları veya Tıklayın):", True, COLOR_TEXT_MAIN)
        self.screen.blit(diff_txt, (SCREEN_WIDTH // 2 - diff_txt.get_width() // 2, 465))

        difficulties = [("1. KOLAY", "EASY"), ("2. ORTA", "MEDIUM"), ("3. ZOR", "HARD")]
        for idx, (label, key) in enumerate(difficulties):
            bx = SCREEN_WIDTH // 2 - 210 + (idx * 145)
            by = 505
            is_sel = (selected_difficulty == key)
            
            btn_rect = pygame.Rect(bx, by, 130, 45)
            bg_col = COLOR_ACCENT if is_sel else (30, 40, 65)
            txt_col = (10, 10, 10) if is_sel else COLOR_TEXT_MAIN
            
            pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_ACCENT, btn_rect, width=2, border_radius=8)
            
            t = self.font_medium.render(label, True, txt_col)
            self.screen.blit(t, (bx + (65 - t.get_width() // 2), by + 12))

        # Başlat İpucu
        start_txt = self.font_header.render("[ ENTER / SPACE ] TUŞUNA BASARAK BAŞLAYIN", True, COLOR_ACCENT)
        self.screen.blit(start_txt, (SCREEN_WIDTH // 2 - start_txt.get_width() // 2, 580))

    def draw_pause(self):
        """Duraklatma Ekranı."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        p_txt = self.font_title.render("⏸ OYUN DURAKLATILDI", True, COLOR_POWERUP_GOLD)
        c_txt = self.font_header.render("Devam etmek için [ SPACE / P ] tuşuna basın", True, COLOR_TEXT_MAIN)
        
        self.screen.blit(p_txt, (SCREEN_WIDTH // 2 - p_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(c_txt, (SCREEN_WIDTH // 2 - c_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    def draw_game_over(self, final_score, high_score, is_new_record):
        """Oyun Bitti (Game Over) Ekranı."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 5, 10, 220))
        self.screen.blit(overlay, (0, 0))

        card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 160, 400, 320)
        pygame.draw.rect(self.screen, (25, 15, 25), card_rect, border_radius=16)
        pygame.draw.rect(self.screen, COLOR_FOOD_NORMAL, card_rect, width=3, border_radius=16)

        go_txt = self.font_title.render("💥 OYUN BİTTİ", True, COLOR_FOOD_NORMAL)
        self.screen.blit(go_txt, (SCREEN_WIDTH // 2 - go_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 130))

        if is_new_record:
            rec_txt = self.font_header.render("🎉 YENİ REKOR!", True, COLOR_POWERUP_GOLD)
            self.screen.blit(rec_txt, (SCREEN_WIDTH // 2 - rec_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        score_lbl = self.font_header.render(f"Toplanan Skor: {final_score}", True, COLOR_TEXT_MAIN)
        high_lbl = self.font_medium.render(f"En Yüksek Skor: {high_score}", True, COLOR_TEXT_MUTED)
        
        self.screen.blit(score_lbl, (SCREEN_WIDTH // 2 - score_lbl.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(high_lbl, (SCREEN_WIDTH // 2 - high_lbl.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        restart_btn = self.font_header.render("[ R ] TEKRAR OYNA", True, COLOR_ACCENT)
        menu_btn = self.font_medium.render("[ M / ESC ] ANA MENÜYE DÖN", True, COLOR_TEXT_MUTED)
        
        self.screen.blit(restart_btn, (SCREEN_WIDTH // 2 - restart_btn.get_width() // 2, SCREEN_HEIGHT // 2 + 65))
        self.screen.blit(menu_btn, (SCREEN_WIDTH // 2 - menu_btn.get_width() // 2, SCREEN_HEIGHT // 2 + 110))
