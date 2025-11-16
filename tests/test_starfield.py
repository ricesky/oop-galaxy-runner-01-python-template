# tests/test_starfield.py
import pygame
import pytest

from src.core.starfield import Starfield


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def test_starfield_moves_stars_down():
    width, height = 800, 600
    starfield = Starfield(screen_width=width, screen_height=height, star_count=0)

    # Override daftar stars: [x, y, speed, size]
    starfield.stars = [
        [100.0, 10.0, 100.0, 2],  # y=10, speed=100
    ]

    dt = 0.5  # 0.5 detik
    starfield.update(dt)

    x, y, speed, size = starfield.stars[0]

    # y bertambah sebesar speed * dt = 100 * 0.5 = 50 → 60
    assert y == pytest.approx(60.0)


def test_starfield_wraps_stars_from_bottom_to_top():
    width, height = 800, 600
    starfield = Starfield(screen_width=width, screen_height=height, star_count=0)

    # Bintang ini akan lewat bawah layar setelah update
    starfield.stars = [
        [200.0, 590.0, 50.0, 2],  # y=590, speed=50 → 590 + 50*0.3 = 605 > 600
    ]

    dt = 0.3
    starfield.update(dt)

    x, y, speed, size = starfield.stars[0]

    # Setelah lewat bawah, logika Starfield meng-set y = 0 dan x random
    assert y == 0
    assert 0 <= x <= width
    assert 40 <= speed <= 160
    assert 1 <= size <= 3
