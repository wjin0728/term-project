from pico2d import *
import game_framework
import play_mode

menu = None
font = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)


def init():
    global menu
    global font
    menu = load_image('resource/image/menu.png')
    font = load_font('resource/font/main.TTF', 16)


def finish():
    menu.__del__()


def update():
    pass


def draw():
    global menu
    clear_canvas()
    menu.clip_draw(0, 0, game_framework.screen_width, game_framework.screen_height,
                   game_framework.screen_width//2, game_framework.screen_height//2
                   )
    update_canvas()


def pause():
    pass


def resume():
    pass
