from pico2d import *
from game_framework import *
from game_world import *


class Background:
    image = None

    def __init__(self, num):
        if self.image is None:
            self.image = load_image("resource/image/background" + num + '.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, screen_width // 2, screen_height // 2,
                             screen_width, screen_height)
