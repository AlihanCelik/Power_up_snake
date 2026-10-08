"""
Gelişmiş Yılan Oyunu (Power-up Snake) - Yapılandırma ve Sabitler
---------------------------------------------------------------
Bu dosya oyundaki tüm görsel, matematiksel ve mantıksal ayarları içerir.
Öğrencilerin oyunu kolayca özelleştirebilmesi için modüler olarak tasarlanmıştır.
"""

import pygame

# 1. Ekran ve Izgara (Grid) Ayarları
GRID_SIZE = 30           # Her bir kare (hücre) boyutu (piksel)
GRID_WIDTH = 26          # Yatay kare sayısı
GRID_HEIGHT = 20         # Dikey kare sayısı

# Ekran Boyutları
PLAY_AREA_WIDTH = GRID_WIDTH * GRID_SIZE   # 780 px
PLAY_AREA_HEIGHT = GRID_HEIGHT * GRID_SIZE # 600 px
HUD_HEIGHT = 90                            # Üst bilgi çubuğu yüksekliği
SCREEN_WIDTH = PLAY_AREA_WIDTH
SCREEN_HEIGHT = PLAY_AREA_HEIGHT + HUD_HEIGHT

FPS = 60 # Hedef Kare Hızı (Frame Rate)

# 2. Renk Paleti (Neon Arcade Teması)
COLOR_BG = (15, 18, 28)            # Koyu Lacivert / Siyah Arka Plan
COLOR_GRID = (25, 32, 48)          # 💡 Izgara Çizgileri
COLOR_HUD_BG = (10, 12, 20)        # Üst Panel Arka Planı
COLOR_BORDER = (40, 50, 75)        # Kenarlık Rengi

# Yılan Renkleri
COLOR_SNAKE_HEAD = (46, 204, 113)  # Canlı Yeşil Baş
COLOR_SNAKE_BODY = (39, 174, 96)   # Yeşil Gövde
COLOR_SNAKE_EYE = (255, 255, 255)  # Göz Akı
COLOR_SNAKE_PUPIL = (20, 20, 20)   # Göz Bebeği

# Güçlendirme ve Yem Renkleri
COLOR_FOOD_NORMAL = (231, 76, 60)  # 🍏 Kırmızı Elma
COLOR_POWERUP_ICE = (52, 152, 219)  # 🧊 Mavi Buz Yemi
COLOR_POWERUP_GOLD = (241, 196, 15) # 🌟 Altın Elma
COLOR_POWERUP_GHOST = (155, 89, 182)# 👻 Mor Hayalet Yemi
COLOR_POWERUP_TURBO = (230, 126, 34)# ⚡ Turuncu Turbo Yemi
COLOR_POWERUP_BOMB = (231, 76, 60) # 💣 Kırmızı Bomba/Zehir

# Yazı Renkleri
COLOR_TEXT_MAIN = (236, 240, 241)
COLOR_TEXT_MUTED = (149, 165, 166)
COLOR_ACCENT = (46, 204, 113)

# 3. Yılan Hız Seviyeleri (Saniye başına adım sayısı)
SPEED_EASY = 7
SPEED_MEDIUM = 10
SPEED_HARD = 14

# 4. Güçlendirme (Power-up) Türleri ve Ayarları
POWERUP_TYPES = {
    'NORMAL': {
        'name': 'Elma',
        'color': COLOR_FOOD_NORMAL,
        'icon': '🍏',
        'score': 10,
        'duration': 0,      # Anlık etki (Süresiz)
        'description': '+10 Puan & Büyüme'
    },
    'ICE': {
        'name': 'Buz Yavaşlatıcı',
        'color': COLOR_POWERUP_ICE,
        'icon': '🧊',
        'score': 15,
        'duration': 6.0,    # 6 saniye yavaşlatma
        'speed_modifier': 0.6, # Hızı %40 yavaşlatır (Kontrol kolaylığı sağlar)
        'description': 'Hızı Yavaşlatır (6s)'
    },
    'GOLD': {
        'name': 'Altın Elma',
        'color': COLOR_POWERUP_GOLD,
        'icon': '🌟',
        'score': 50,
        'duration': 8.0,    # 8 saniye boyunca puanları 2 katına çıkarır
        'score_multiplier': 2.0,
        'description': '2x Puan Çarpanı (8s)'
    },
    'GHOST': {
        'name': 'Hayalet Modu',
        'color': COLOR_POWERUP_GHOST,
        'icon': '👻',
        'score': 20,
        'duration': 7.0,    # 7 saniye boyunca duvarlardan ve kendi içinden geçebilir
        'description': 'Duvarlardan Geçiş (7s)'
    },
    'TURBO': {
        'name': 'Turbo Hız',
        'color': COLOR_POWERUP_TURBO,
        'icon': '⚡',
        'score': 25,
        'duration': 5.0,
        'speed_modifier': 1.5, # %50 daha hızlı
        'score_multiplier': 1.5,
        'description': 'Hızlı Depar + 1.5x Puan'
    }
}

# Güçlendirmelerin Ekranda Kalma Süresi (Saniye)
POWERUP_SPAWN_LIFETIME = 10.0

# 5. Yön Vektörleri
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
