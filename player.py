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


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


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
        player.frame = (player.frame + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame) * (player.image.w // FRAMES_PER_ACTION), 0,
                                         player.image.w // FRAMES_PER_ACTION, player.image.h,
                                         0, '', player.x, player.y, 49 * 3, 60 * 3)


class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir = -1

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def do(player):
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(50, player.x, game_framework.screen_width - 50)
        player.frame = (player.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        player.image_run.clip_composite_draw(int(player.frame) * (player.image_run.w // 8), 0,
                                         player.image_run.w // 8, player.image_run.h,
                                         0, '', player.x, player.y, (player.image_run.w // 8) * 3, player.image_run.h * 3)


class Jump:

    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir = -1

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def do(player):
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(50, player.x, game_framework.screen_width - 50)
        player.frame = (player.frame + 9 * ACTION_PER_TIME * game_framework.frame_time) % 9

    @staticmethod
    def draw(player):
        player.image_jump.clip_composite_draw(int(player.frame) * (player.image_jump.w // 9), 0,
                                         player.image_jump.w // 9, player.image_jump.h,
                                         0, '', player.x, player.y, (player.image_jump.w // 9) * 3, player.image_jump.h * 3)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
            Jump: {}
        }

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


class Player:
    def __init__(self):
        self.x, self.y = 50, 350
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('resource/image/player_idle.png')
        self.image_run = load_image('resource/image/player_run.png')
        self.image_jump = load_image('resource/image/player_jump.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
