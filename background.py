from pico2d import *
from game_framework import *
from game_world import *

class Ground:
    image = None

    def __init__(self, num):
        if self.image is None:
            self.image = load_image("resource/image/ground"+num+'.png')


