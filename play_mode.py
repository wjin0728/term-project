from pico2d import *
import game_framework
import random

menu = None
font = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    global menu
    global font
    menu = load_image('resource/image/menu.png')
    font = load_font('resource/font/main.TTF', 16)
    pass


def finish():
    pass


def update():
    pass


def draw():
    global menu
    clear_canvas()
    menu.clip_draw(0, 0, game_framework.screen_width, game_framework.screen_height, game_framework.screen_width//2, game_framework.screen_height//2)
    update_canvas()


def pause():
    pass


def resume():
    pass
