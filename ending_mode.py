from pico2d import *
import game_framework
import menu_mode
import game_world
import random
import server


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(menu_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(menu_mode)


def init():
    server.p1_win = load_image('resource/image/p1.png')
    server.p2_win = load_image('resource/image/p2.png')
    pass


def finish():
    server.who_win = 0
    pass


def update():
    pass


def draw():
    clear_canvas()
    if server.who_win == 1:
        server.p1_win.clip_draw(0, 0, server.p1_win.w, server.p1_win.h,
                                game_framework.screen_width // 2, game_framework.screen_height // 2
                                )
    elif server.who_win == 2:
        server.p2_win.clip_draw(0, 0, server.p2_win.w, server.p2_win.h,
                                game_framework.screen_width // 2, game_framework.screen_height // 2
                                )
    update_canvas()


def pause():
    pass


def resume():
    pass
