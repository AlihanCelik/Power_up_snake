"""
Gelişmiş Yılan Oyunu - Ses Yöneticisi (Sound Manager)
---------------------------------------------------
Bu modül, harici ses dosyalarına (WAV/MP3) ihtiyaç duymadan
matematiksel sinüs dalgaları kullanarak oyun ses efektlerini canlı üretir.
Öğrencilere dijital ses sentezi ve sinüs dalgaları mantığını öğretmek için mükemmeldir.
"""

import math
import array
import pygame

class SoundManager:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.muted = False
        self.enabled = False
        
        try:
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._generate_sounds()
        except Exception as e:
            print(f"[Uyarı] Ses sistemi başlatılamadı: {e}")
            self.enabled = False

    def _create_sine_wave(self, frequency, duration, volume=0.3, decay=True):
        """Belirtilen frekans ve sürede 16-bit sinüs dalgası ses örneği üretir."""
        if not self.enabled:
            return None
        
        n_samples = int(self.sample_rate * duration)
        buf = array.array('h')
        
        for i in range(n_samples):
            t = float(i) / self.sample_rate
            # Sinüs dalgası formülü: A * sin(2 * pi * f * t)
            value = math.sin(2.0 * math.pi * frequency * t)
            
            # Ses sönümleme (Decay / Envelope)
            env = (1.0 - (t / duration)) if decay else 1.0
            
            sample = int(value * 32767 * volume * env)
            # 16-bit sınırlandırma (clipping engelleme)
            sample = max(-32768, min(32767, sample))
            buf.append(sample)
            
        return pygame.mixer.Sound(buffer=buf)

    def _create_arpeggio(self, frequencies, duration_per_note, volume=0.3):
        """Birden fazla frekansı sırayla çalarak melodik ses efekti üretir."""
        if not self.enabled:
            return None
            
        buf = array.array('h')
        for freq in frequencies:
            n_samples = int(self.sample_rate * duration_per_note)
            for i in range(n_samples):
                t = float(i) / self.sample_rate
                value = math.sin(2.0 * math.pi * freq * t)
                env = 1.0 - (t / duration_per_note)
                sample = int(value * 32767 * volume * env)
                sample = max(-32768, min(32767, sample))
                buf.append(sample)
                
        return pygame.mixer.Sound(buffer=buf)

    def _generate_sounds(self):
        """Tüm oyun ses efektlerini bellekte önceden sentezler."""
        # 1. Normal Yem Yeme Sesi (Kısa yüksek frekanslı bip)
        self.snd_eat = self._create_sine_wave(frequency=587.33, duration=0.08, volume=0.35) # D5
        
        # 2. Buz Güçlendirmesi Sesi (Soğuk, düşen tonlar)
        self.snd_ice = self._create_arpeggio([880, 659, 523], duration_per_note=0.07, volume=0.3)
        
        # 3. Altın Elma Sesi (Neşeli yükselen majör akor: C5 -> E5 -> G5 -> C6)
        self.snd_gold = self._create_arpeggio([523.25, 659.25, 783.99, 1046.50], duration_per_note=0.06, volume=0.35)
        
        # 4. Hayalet Modu Sesi (Gizemli dalgalanan ses)
        self.snd_ghost = self._create_arpeggio([440, 493.88, 554.37, 659.25], duration_per_note=0.08, volume=0.3)
        
        # 5. Turbo Hız Sesi (Zippy yüksek frekans)
        self.snd_turbo = self._create_arpeggio([600, 800, 1200], duration_per_note=0.04, volume=0.3)
        
        # 6. Oyun Bitti (Game Over - Düşük bas sesi)
        self.snd_game_over = self._create_arpeggio([300, 220, 150, 90], duration_per_note=0.15, volume=0.4)

    def play(self, sound_name):
        """İstenen ses efektini çalar."""
        if not self.enabled or self.muted:
            return
            
        sound_map = {
            'eat': getattr(self, 'snd_eat', None),
            'ice': getattr(self, 'snd_ice', None),
            'gold': getattr(self, 'snd_gold', None),
            'ghost': getattr(self, 'snd_ghost', None),
            'turbo': getattr(self, 'snd_turbo', None),
            'game_over': getattr(self, 'snd_game_over', None),
        }
        
        snd = sound_map.get(sound_name)
        if snd:
            snd.play()

    def toggle_mute(self):
        """Sesi açar/kapatır."""
        self.muted = not self.muted
        return self.muted
