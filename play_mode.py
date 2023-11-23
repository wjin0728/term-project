from pico2d import *
import game_framework
import menu_mode
import game_world
import random
import server

from background import Background
from ground import Ground
from player import Player
from Player2 import Player2


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(menu_mode)
        else:
            server.player_one.handle_event(event)
            server.player_two.handle_event(event)


def init():
    server.player_one = Player()
    server.player_two = Player2()
    game_world.add_object(Background('1'))
    game_world.add_object(Ground('1'), 1)
    game_world.add_object(server.player_one, 2)
    game_world.add_object(server.player_two, 2)
    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
