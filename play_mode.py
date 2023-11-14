from pico2d import *
import game_framework
import menu_mode
import game_world
import random

from background import Background
from ground import Ground
from player import Player


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(menu_mode)
        else:
            player.handle_event(event)


def init():
    global player
    player = Player()
    game_world.add_object(Background('1'))
    game_world.add_object(Ground('1'), 1)
    game_world.add_object(player, 2)
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
