import game_world
import game_framework
from pico2d import *
import server


class Sword:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.p1[0], self.p1[1], self.p2[0], self.p2[1]

    def handle_collision(self, group, other):
        pass
