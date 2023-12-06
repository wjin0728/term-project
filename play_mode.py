from pico2d import *
import game_framework
import menu_mode
import game_world
import random
import server
import ending_mode

from background import Background
from ground import Ground
from player import Player
from Player2 import Player2

health = None


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
    if server.player_one.hp == 0:
        server.who_win = 2
        game_framework.change_mode(ending_mode)
    elif server.player_two.hp == 0:
        server.who_win = 1
        game_framework.change_mode(ending_mode)


def init():
    global health
    health = load_image('resource/image/heart.png')
    server.player_one = Player()
    server.player_two = Player2()
    game_world.add_object(Background('1'))
    game_world.add_object(Ground('1'), 1)
    game_world.add_object(server.player_one, 2)
    game_world.add_object(server.player_two, 2)
    game_world.add_collision_pair("player1 : sword", server.player_one, None)
    game_world.add_collision_pair("player2 : sword", server.player_two, None)
    pass


def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collisions()
    pass


def draw():
    global health
    clear_canvas()
    game_world.render()
    x = 40
    for _ in range(server.player_one.hp):
        health.clip_draw(0, 0, health.w, health.h,
                         x, 800)
        x += 100

    x = 1536 - 40
    for _ in range(server.player_two.hp):
        health.clip_draw(0, 0, health.w, health.h,
                         x, 800)
        x -= 100
    update_canvas()


def pause():
    pass


def resume():
    pass
