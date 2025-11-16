# tests/test_player.py
import pygame
import pytest

from src.core.player import Player


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    # Inisialisasi pygame sekali untuk modul ini
    pygame.init()
    yield
    pygame.quit()


class DummyKeys:
    """
    Objek sederhana yang meniru hasil pygame.key.get_pressed().
    Kita hanya peduli pada K_LEFT dan K_RIGHT.
    """
    def __init__(self, pressed_map: dict[int, bool]):
        self.pressed_map = pressed_map

    def __getitem__(self, key: int) -> bool:
        return self.pressed_map.get(key, False)


def test_player_moves_left_and_right(monkeypatch):
    screen_width = 800
    player = Player(x=400, y=550, speed=200, screen_width=screen_width)

    # dt = 1 detik supaya hitungan gampang
    dt = 1.0

    # --- Gerak ke kiri ---
    def fake_get_pressed_left():
        return DummyKeys({pygame.K_LEFT: True})

    monkeypatch.setattr(pygame.key, "get_pressed", fake_get_pressed_left)

    player.update(dt)

    # Karena speed = 200 dan dt = 1, posisi harus berkurang 200
    assert player.x == pytest.approx(200)

    # --- Gerak ke kanan ---
    def fake_get_pressed_right():
        return DummyKeys({pygame.K_RIGHT: True})

    monkeypatch.setattr(pygame.key, "get_pressed", fake_get_pressed_right)

    player.update(dt)

    # Dari x=200, +200 → kembali ke 400
    assert player.x == pytest.approx(400)


def test_player_clamped_to_screen(monkeypatch):
    screen_width = 800
    player = Player(x=400, y=550, speed=500, screen_width=screen_width)
    dt = 1.0

    # Tekan kiri terus sampai harusnya lewat layar kiri
    def fake_get_pressed_left():
        return DummyKeys({pygame.K_LEFT: True})

    monkeypatch.setattr(pygame.key, "get_pressed", fake_get_pressed_left)

    player.update(dt)

    # half width
    half_w = player.width / 2
    # Tidak boleh kurang dari half_w
    assert player.x >= half_w

    # Tekan kanan terus sampai harusnya lewat layar kanan
    def fake_get_pressed_right():
        return DummyKeys({pygame.K_RIGHT: True})

    monkeypatch.setattr(pygame.key, "get_pressed", fake_get_pressed_right)

    player.update(dt)

    # Tidak boleh lebih dari screen_width - half_w
    assert player.x <= screen_width - half_w
