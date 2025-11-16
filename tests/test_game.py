# tests/test_game.py
import pygame
import pytest

from src.core.game import Game
from src.core.player import Player
from src.core.starfield import Starfield


@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def test_game_initializes_player_and_starfield():
    width, height = 800, 600
    game = Game(screen_width=width, screen_height=height)

    assert isinstance(game.player, Player)
    assert isinstance(game.starfield, Starfield)

    # Player di dekat bawah layar
    assert game.player.y == pytest.approx(height - 60)

    # Starfield punya jumlah bintang sesuai konfigurasi
    assert len(game.starfield.stars) == 100


def test_game_update_calls_components_update(monkeypatch):
    width, height = 800, 600
    game = Game(screen_width=width, screen_height=height)

    called_player = {"count": 0}
    called_starfield = {"count": 0}

    # Monkeypatch method update dari player & starfield
    def fake_player_update(dt):
        called_player["count"] += 1

    def fake_starfield_update(dt):
        called_starfield["count"] += 1

    game.player.update = fake_player_update
    game.starfield.update = fake_starfield_update

    dt = 0.016  # ~1 frame (60 FPS)
    game.update(dt)

    assert called_player["count"] == 1
    assert called_starfield["count"] == 1
