import game_world
import game_framework
from pico2d import *


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:

    @staticmethod
    def enter(player, e):
        if player.face_dir == -1:
            player.action = 2
        elif player.face_dir == 1:
            player.action = 3
        player.dir = 0
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)



class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.action, player.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.action, player.face_dir = -1, 0, -1

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def do(player):
        # player.frame = (player.frame + 1) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(25, player.x, 1600-25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


# Player Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Player:
    def __init__(self):
        self.x, self.y = 50, 350
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('resource/image/player_idle.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        pass

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(self.frame) * (self.image.w // FRAMES_PER_ACTION), 0,
                                           self.image.w // FRAMES_PER_ACTION, self.image.h,
                                           0, 'h', self.x, self.y, 49 * 3, 53 * 3)
        else:
            self.image.clip_composite_draw(int(self.frame) * (self.image.w // FRAMES_PER_ACTION), 0,
                                           self.image.w // FRAMES_PER_ACTION, self.image.h,
                                           0, '', self.x, self.y, 49 * 3, 53 * 3)
