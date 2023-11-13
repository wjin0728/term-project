import game_world
import game_framework
from pico2d import *


# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Player:
    def __init__(self):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('resource/image/player_idle.png')

    def update(self):

        pass

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(self.frame) * (self.image.w//6), 0, self.image.w//6, self.image.h,
                                          0, 'h', self.x, self.y, 49*3, 53*3)
        else:
            self.image.clip_composite_draw(int(self.frame) * (self.image.w//6), 0, self.image.w//6, self.image.h,
                                          0, '', self.x, self.y, 49*3, 53*3)