"""
Gelişmiş Yılan Oyunu - Oyun Modelleri (OOP Nesneleri)
---------------------------------------------------
Bu dosya yılan, yemler, güçlendirmeler ve görsel parçacıkların
mantıksal sınıflarını (Classes) barındırır.
"""

import random

class Snake:
    """Yılan nesnesi: Pozisyon, hareket, büyüme ve güçlendirme durumlarını yönetir."""
    
    def __init__(self, start_x, start_y, initial_length=3):
        self.reset(start_x, start_y, initial_length)

    def reset(self, start_x, start_y, initial_length=3):
        """Yılanı başlangıç durumuna sıfırlar."""
        self.body = [(start_x - i, start_y) for i in range(initial_length)]
        self.direction = (1, 0)       # Sağa doğru hareket
        self.next_direction = (1, 0)  # Bir sonraki hamle
        self.grow_pending = 0
        
        # Aktif Güçlendirmeler Dict: {'POWERUP_TYPE': kalan_saniye}
        self.active_powerups = {}

    @property
    def head(self):
        """Yılanın başının koordinatı."""
        return self.body[0]

    def change_direction(self, new_dir):
        """
        Kullanıcı tuş girdisini işler.
        Ters yöne ani 180 derece dönüşleri (kendi içine girmeyi) engeller.
        """
        cur_dx, cur_dy = self.direction
        new_dx, new_dy = new_dir
        
        # Eğer mevcut yönün tam zıttı değilse kabul et
        if (cur_dx + new_dx != 0) or (cur_dy + new_dy != 0):
            self.next_direction = new_dir

    def update_powerups(self, dt):
        """Aktif güçlendirmelerin kalan sürelerini günceller."""
        expired = []
        for p_type, time_left in self.active_powerups.items():
            new_time = time_left - dt
            if new_time <= 0:
                expired.append(p_type)
            else:
                self.active_powerups[p_type] = new_time
                
        for p_type in expired:
            del self.active_powerups[p_type]

    def add_powerup(self, p_type, duration):
        """Yılana yeni bir güçlendirme ekler veya süresini yeniler."""
        if duration > 0:
            self.active_powerups[p_type] = duration

    def is_ghost(self):
        """Hayalet modu aktif mi?"""
        return 'GHOST' in self.active_powerups

    def is_ice(self):
        """Buz modu aktif mi?"""
        return 'ICE' in self.active_powerups

    def is_gold(self):
        """Altın 2x çarpan aktif mi?"""
        return 'GOLD' in self.active_powerups

    def is_turbo(self):
        """Turbo mod aktif mi?"""
        return 'TURBO' in self.active_powerups

    def get_speed_multiplier(self):
        """Aktif güçlendirmelere göre hız çarpanını hesaplar."""
        mult = 1.0
        if self.is_ice():
            mult *= 0.6  # Yavaşlatma
        if self.is_turbo():
            mult *= 1.4  # Hızlandırma
        return mult

    def move(self, grid_width, grid_height):
        """
        Yılanı 1 kare ileri taşır.
        Hayalet modunda duvarlardan geçer (Wrap around).
        """
        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.head
        
        new_x = head_x + dx
        new_y = head_y + dy

        # Hayalet modu veya sınır geçişi kontrolü
        is_ghost = self.is_ghost()
        
        if is_ghost:
            # Duvarların içinden geçiş (Ekrandan çıkınca karşıdan girer)
            new_x = new_x % grid_width
            new_y = new_y % grid_height
        
        new_head = (new_x, new_y)
        self.body.insert(0, new_head)

        # Eğer büyümeyecekse kuyruğun sonunu sil
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        """Yılanın büyüme miktarını artırır."""
        self.grow_pending += amount

    def check_wall_collision(self, grid_width, grid_height):
        """Hayalet modu haricinde duvara çarpma kontrolü."""
        if self.is_ghost():
            return False
            
        hx, hy = self.head
        return hx < 0 or hx >= grid_width or hy < 0 or hy >= grid_height

    def check_self_collision(self):
        """
        Kendi kuyruğuna çarpma kontrolü.
        Hayalet modunda kendi içinden geçebildiği için çarpışma olmaz!
        """
        if self.is_ghost():
            return False
            
        # Baş kısmının gövdenin geri kalanıyla kesişip kesişmediğine bakılır
        return self.head in self.body[1:]


class FoodItem:
    """Yem ve Özel Güçlendirme Nesnesi."""
    
    def __init__(self, x, y, p_type='NORMAL', lifetime=0):
        self.x = x
        self.y = y
        self.type = p_type
        self.lifetime = lifetime       # 0 ise sonsuz (ekranda kalır), >0 ise kaybolur
        self.max_lifetime = lifetime
        self.anim_phase = random.uniform(0, 6.28) # Görsel salınım için radyan fazı

    @property
    def pos(self):
        return (self.x, self.y)

    def update(self, dt):
        """Görsel animasyon ve kalan kalma süresini günceller."""
        self.anim_phase += dt * 4.0
        if self.lifetime > 0:
            self.lifetime -= dt
            return self.lifetime > 0
        return True


class Particle:
    """Yem yeme veya güçlendirme anında oluşan görsel parçacık efekti."""
    
    def __init__(self, x, y, color, vx=0, vy=0, size=4, lifetime=0.5):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self, dt):
        """Parçacığı hareket ettirir ve yaşlandırır."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        return self.lifetime > 0

    @property
    def alpha_ratio(self):
        """0.0 ile 1.0 arasında kalan ömür oranı."""
        return max(0.0, self.lifetime / self.max_lifetime)


class FloatingText:
    """Ekranda yukarı doğru süzülen ve saydamlaşan skor/bilgi metinleri."""
    
    def __init__(self, text, x, y, color, duration=1.0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.max_duration = duration

    def update(self, dt):
        """Yazıyı yukarı süzdürür."""
        self.y -= 25.0 * dt # Saniyede 25px yukarı kayar
        self.duration -= dt
        return self.duration > 0

    @property
    def alpha(self):
        """Saydamlık oranı (0-255)."""
        return int(255 * max(0.0, self.duration / self.max_duration))
