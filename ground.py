from pico2d import *
from game_framework import *
from game_world import *


class Ground:
    image = None

    def __init__(self, num):
        if self.image is None:
            self.image = load_image("resource/image/ground" + num + '.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, screen_width // 2, 150,
                             screen_width, 300)
