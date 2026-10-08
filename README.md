# 🐍 Power-up Snake (Gelişmiş Yılan Oyunu)

Öğretim ve eğitim amaçlı geliştirilmiş, Python ve **Pygame** kullanılarak yazılmış **Özel Güçlendirici Yemli Yılan Oyunu**.

---

## 🌟 Oyun Özellikleri ve Konsept

Standart yılan oyununa ek olarak oyuna heyecan katan **özel güçlendirici yemler (Power-ups)** ve dinamik görsel/işitsel efektler eklenmiştir:

| Yem / Güçlendirme | Simge | Renk | Etki ve Açıklama |
| :--- | :---: | :---: | :--- |
| **Normal Elma** | 🍏 | Kırmızı | Standard **+10 Puan** verir ve yılanı 1 birim uzatır. |
| **Buz Yemi** | 🧊 | Mavi | Yılanı **6 saniye boyunca %40 yavaşlatır**. Yılan çok hızlandığında veya dar alanlarda mükemmel bir kontrol avantajı sağlar. |
| **Altın Elma** | 🌟 | Altın Sarı | **+50 Puan** verir ve **8 saniye boyunca alınan TÜM puanları 2 katına (2X)** çıkarır! |
| **Hayalet Modu** | 👻 | Mor | **7 saniye boyunca** yılanı saydamlaştırır. Duvarların içinden geçmeyi (**Wrap-Around**) ve kendi kuyruğunun içinden yanmadan geçmeyi sağlar. |
| **Turbo Hız** | ⚡ | Turuncu | **5 saniye boyunca** hızlı depar atılmasını sağlar ve 1.5x puan çarpanı verir. |

---

## 🎮 Kontroller ve Kullanım

- **Yön Tuşları / WASD**: Yılanı yönlendirir.
- **SPACE / P**: Oyunu duraklatır veya devam ettirir.
- **M Tuşu**: Ses efektlerini açar / kapatır (Mute / Unmute).
- **1 - 2 - 3 Tuşları**: Ana menüde zorluk seviyesini seçer (**Kolay**, **Orta**, **Zor**).
- **R Tuşu**: Oyun bittiğinde yeniden başlatır.
- **ESC / M**: Ana menüye döner.

---

## 🚀 Çalıştırma Talimatları

### 1. Hazır Çalıştırma (Tavsiye Edilen)
Terminalde oyun klasöründeyken aşağıdaki komutu çalıştırmanız yeterlidir:

```bash
./run.sh
```

### 2. Manuel Çalıştırma
Sanal ortamınız aktifken doğrudan Python ile başlatabilirsiniz:

```bash
source .venv/bin/activate
python3 main.py
```

---

## 📚 KOD MİMARİSİ VE ÖĞRETİM DOKÜMANI

Proje, yazılım geliştirme prensiplerini ve Nesne Yönelimli Programlama (OOP) kavramlarını öğretmek amacıyla **modüler** ve **temiz kod (clean code)** prensiplerine uygun olarak 5 ana dosyaya ayrılmıştır:

```text
Power-up Snake/
├── config.py           # Oyun sabitleri, renk paletleri ve güçlendirme ayarları
├── models.py           # Yılan, Yem, Parçacık ve Yüzen Metin OOP sınıfları
├── sound_manager.py    # Harici dosyaya ihtiyaç duymayan canlı sinüs ses sentezleyicisi
├── ui_manager.py       # Pygame Surface, ızgara, HUD zamanlayıcıları ve menü çizimleri
├── main.py             # Ana oyun döngüsü (Game Loop), delta time ve çarpışma mantığı
├── highscore.json      # Rekor skorların otomatik saklandığı JSON veri dosyası
└── requirements.txt    # Bağımlılıklar (pygame)
```

### 📋 Modül Detayları:

1. **[config.py](file:///Users/alihan/Documents/Power-up%20Snake/config.py)**:
   - Izgara hücre boyutu, ekran çözünürlüğü ve oyun hızları burada tanımlanır.
   - Renkler RGB formatında tutulur.
   - Öğrenciler oyun hızını, renkleri veya güçlendirme sürelerini tek bir dosyadan kolayca değiştirebilir.

2. **[models.py](file:///Users/alihan/Documents/Power-up%20Snake/models.py)**:
   - `Snake`: Yılanın vücut koordinatlarını `list` olarak tutar. Ani 180 derece dönüşleri engelleyen yön kontrolü, duvar geçişi (Hayalet Modu) ve büyüme mantığı içerir.
   - `FoodItem`: Yemlerin türünü, animasyon fazını ve ekranda kalma sürelerini yönetir.
   - `Particle`: Yem yeme anında patlayan kıvılcım efektlerinin yer çekimi ve saydamlaşma fiziğini hesaplar.
   - `FloatingText`: Skora eklenti yapıldığında ekranda yukarı doğru kayan metin efektidir.

3. **[sound_manager.py](file:///Users/alihan/Documents/Power-up%20Snake/sound_manager.py)**:
   - Harici hiçbir `.wav` veya `.mp3` dosyasına ihtiyaç **duymaz**.
   - Python'un `math.sin` ve `array` modüllerini kullanarak 16-bit dijital sinüs dalgaları üretir ve Pygame Mixer ile sentezler.
   - Öğrencilere ses frekansları (Hz), majör akorlar ve dijital ses işleme kavramlarını öğretir.

4. **[ui_manager.py](file:///Users/alihan/Documents/Power-up%20Snake/ui_manager.py)**:
   - Ekranın üst kısmındaki HUD panelinde aktif güçlendirmelerin kalan sürelerini renkli **dolan/azalan zaman çubukları (ProgressBar)** ile gösterir.
   - Yılanın baş kısmına bakış açısına göre hareket eden dinamik gözler ve güçlendirme haleleri çizer.
   - Menü, duraklatma ve Oyun Bitti ekranlarını hazırlar.

5. **[main.py](file:///Users/alihan/Documents/Power-up%20Snake/main.py)**:
   - Oyun döngüsü (`run`), etkinlik dinleyicisi (`_handle_events`) ve çarpışma testlerini (`_check_collisions`) yürütür.
   - Oyun hızını kitlemeyen esnek `Delta Time (dt)` mantığı kullanır.

---

## 💡 Öğrenciler İçin Geliştirme Fikirleri (Ödev & Alıştırmalar)

Öğrencileriniz veya kendiniz için oyunu genişletebileceğiniz bazı fikirler:

1. **💣 Zehirli / Bomba Yem Ekleme**:
   - Yendiğinde yılanın uzunluğunu 2 birim kısaltan ve puan düşüren kırmızı bomba yemleri ekleyin.
2. **🧱 Engeller ve Duvar Haritaları**:
   - Izgara üzerine sabit veya hareketli engeller (duvarlar) yerleştirin.
3. **👥 2 Kişilik (Multiplayer) Mod**:
   - Aynı klavyede WASD ve Ok Tuşları ile oynayan 2 yılan modu tasarlayın.
