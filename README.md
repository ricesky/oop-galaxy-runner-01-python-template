# oop-galaxy-runner-01-python

## Capaian Pembelajaran

Setelah menyelesaikan seluruh tahapan, mahasiswa diharapkan mampu:

1. Memodelkan permainan 2D sederhana menggunakan **pemrograman berorientasi objek** (class, object, composition, encapsulation, inheritance, polymorphism) di Python.
2. Menggunakan **PyGame** untuk membangun game 2D dengan beberapa komponen: player, musuh (enemy), background, skor, dan UI dasar.
3. Menerapkan **multimedia** (gambar, sprite animation, suara) di dalam game.
4. Mengelola **beberapa screen** (main menu, game screen, high score) menggunakan Screen Manager berbasis OOP.
5. Menerapkan **perilaku AI sederhana** pada musuh (enemy) dan mengatur tingkat kesulitan permainan.

---

## Lingkungan Pengembangan

1. Platform: Python **3.12+** (boleh 3.13 selama PyGame berjalan)
2. Bahasa: Python
3. Editor/IDE yang disarankan:

   * VS Code + Python Extension
   * Terminal
4. Library:

   * `pygame 2.6.1`
   * `pytest`

---

## Cara Menjalankan Project

```bash
python -m src.main
```

---

# Tahap 1 — Class, Object, dan Composition Dasar

**Tujuan Tahap 1**

1. Mahasiswa dapat membuat class `Player` dan `Starfield` menggunakan Python.
2. Mahasiswa memahami **komposisi**: class `Game` memiliki objek `Player` dan `Starfield`.
3. Mahasiswa dapat menjalankan game loop PyGame sederhana dengan background bintang bergerak dan player yang bisa digerakkan dengan keyboard.

Di tahap ini:

* Belum ada enemy
* Belum ada skor
* Belum ada menu
* Fokus ke: **fondasi OOP + game loop**

---

## 0. Menyiapkan Struktur Direktori

Buat struktur berikut:

```text
oop-galaxy-runner-python/
├─ README.md
├─ requirements.txt
└─ src/
   ├─ __init__.py
   ├─ main.py
   └─ core/
      ├─ __init__.py
      ├─ player.py
      ├─ starfield.py
      └─ game.py
```

---

## 1. Membuat Class Player

Kita mulai dari objek yang dikendalikan pemain: **Player**.
Untuk sementara bentuknya **pesawat sederhana** (persegi panjang) yang bergerak horizontal di bagian bawah layar.

Tugas `Player` di Tahap 1:

* Menyimpan posisi dan kecepatan
* Meng-update posisi berdasarkan input keyboard
* Menggambar dirinya ke layar

---

### 1.1 Buat file `src/core/player.py`

Isi dengan kode berikut:

```python
import pygame


class Player:
    def __init__(self, x: float, y: float, speed: float, screen_width: int):
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width

        # Ukuran kapal
        self.width = 40
        self.height = 25

        # Warna kapal (hijau kebiruan)
        self.color = (0, 220, 180)

    def handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            dx += self.speed * dt

        self.x += dx

        # Batasi supaya tidak keluar layar
        half_w = self.width / 2
        if self.x < half_w:
            self.x = half_w
        if self.x > self.screen_width - half_w:
            self.x = self.screen_width - half_w

    def update(self, dt: float):
        # Untuk tahap 1, tidak ada update lain.
        # Method ini tetap disediakan agar nanti mudah diperluas.
        self.handle_input(dt)

    def draw(self, surface: pygame.Surface):
        # Gambar kapal sebagai persegi panjang
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.centerx = int(self.x)
        rect.centery = int(self.y)

        pygame.draw.rect(surface, self.color, rect)

        # Tambahan kecil: segitiga di depan agar terlihat seperti spaceship
        nose_points = [
            (rect.centerx, rect.top - 5),
            (rect.left, rect.top + 5),
            (rect.right, rect.top + 5),
        ]
        pygame.draw.polygon(surface, self.color, nose_points)
```

**Penjelasan Singkat:**

* `handle_input` membaca keyboard dan mengubah posisi X.
* `update` memanggil `handle_input` — nanti bisa ditambah logika lain.
* `draw` menggambar kapal dengan `pygame.draw.rect` + segitiga kecil.

---

## 2. Membuat Class Starfield (Background Bintang Bergerak)

Starfield adalah background berupa **bintang-bintang** yang bergerak turun (seolah pesawat maju ke depan).

Tanggung jawab `Starfield`:

* Menyimpan daftar bintang (posisi, kecepatan, ukuran)
* Menggerakkan bintang setiap frame
* Jika bintang lewat bawah layar → muncul lagi di atas

---

### 2.1 Buat file `src/core/starfield.py`

```python
import pygame
import random


class Starfield:
    def __init__(self, screen_width: int, screen_height: int, star_count: int = 80):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.star_count = star_count

        # Setiap star: (x, y, speed, size)
        self.stars: list[tuple[float, float, float, int]] = []
        self._create_stars()

    def _create_stars(self):
        self.stars.clear()
        for _ in range(self.star_count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            speed = random.uniform(40, 160)
            size = random.randint(1, 3)
            self.stars.append([x, y, speed, size])

    def update(self, dt: float):
        for star in self.stars:
            star[1] += star[2] * dt  # y += speed * dt

            # Jika bintang lewat bawah, reset ke atas dengan posisi random
            if star[1] > self.screen_height:
                star[0] = random.randint(0, self.screen_width)
                star[1] = 0
                star[2] = random.uniform(40, 160)
                star[3] = random.randint(1, 3)

    def draw(self, surface: pygame.Surface):
        for x, y, _, size in self.stars:
            pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), size)
```

**Penjelasan Singkat:**

* Bintang disimpan sebagai list `[x, y, speed, size]`.
* Setiap frame, `y` bertambah sesuai `speed * dt`.
* Jika keluar layar, bintang “lahir kembali” di atas.

---

## 3. Membuat Class Game (Komposisi Player + Starfield)

Sekarang kita butuh satu objek yang **menyatukan semuanya**:

* mengelola `Player`
* mengelola `Starfield`
* punya method:

  * `handle_event(event)`
  * `update(dt)`
  * `draw(surface)`

Inilah class `Game`. Inilah contoh **composition**:
`Game` **memiliki** (`has-a`) `Player` dan `Starfield`.

---

### 3.1 Buat file `src/core/game.py`

```python
import pygame
from .player import Player
from .starfield import Starfield


class Game:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Buat background bintang
        self.starfield = Starfield(screen_width, screen_height, star_count=100)

        # Buat player di bawah tengah layar
        self.player = Player(
            x=screen_width / 2,
            y=screen_height - 60,
            speed=300,
            screen_width=screen_width,
        )

        self.background_color = (5, 5, 20)

    def handle_event(self, event: pygame.event.Event):
        # Tahap 1: belum ada event khusus selain QUIT di main loop
        # Method ini tetap disediakan agar nanti mudah diperluas.
        pass

    def update(self, dt: float):
        self.starfield.update(dt)
        self.player.update(dt)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        self.starfield.draw(surface)
        self.player.draw(surface)
```

---

## 4. Membuat Entry Point `main.py`

Sekarang kita perlu **main loop** untuk menjalankan game:

* inisialisasi PyGame
* membuat window
* membuat instance `Game`
* menjalankan loop:

  * baca event
  * update game
  * draw ke layar
  * `pygame.display.flip()`

---

### 4.1 Buat file `src/main.py`

```python
import pygame
from .core.game import Game


def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Galaxy Runner - Stage 1")

    clock = pygame.time.Clock()
    game = Game(screen_width, screen_height)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # detik per frame

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        # Update game state
        game.update(dt)

        # Draw ke layar
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
```

---

## 5. Menjalankan Tahap 1

Di root repo:

```bash
python -m src.main
```

Jika semuanya benar, program akan menampilkan:

* Background hitam kebiruan
* Banyak bintang bergerak ke bawah
* Sebuah pesawat kecil di bagian bawah yang bisa bergerak kiri-kanan dengan tombol **← →**

---
