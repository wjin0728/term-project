import game_world
import game_framework
from pico2d import *

# Player Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)


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
