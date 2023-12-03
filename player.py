import game_world
import game_framework
from pico2d import *
import server
from Sword import *


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def D_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def D_key_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def A_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def A_key_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def F_KEY_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f


# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Idle:

    @staticmethod
    def enter(player, e):
        player.colWidth = 30
        player.colHeight = 60
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
    def handle_event(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame) * (player.image.w // FRAMES_PER_ACTION), 0,
                                         player.image.w // FRAMES_PER_ACTION, player.image.h,
                                         0, player.face_dir, player.x, player.y, (player.image.w // 6) * 3,
                                         player.image.h * 3)


class Run:

    @staticmethod
    def enter(player, e):
        player.colWidth = 30
        player.colHeight = 60
        if D_key_down(e) or A_key_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir = 1, ''
        elif A_key_down(e) or D_key_up(e):  # 왼쪽으로 RUN
            player.dir, player.face_dir = -1, 'h'

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def handle_event(player, e):
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
                                             0, player.face_dir, player.x, player.y, (player.image_run.w // 8) * 3,
                                             player.image_run.h * 3)


class Jump:

    @staticmethod
    def enter(player, e):
        player.colWidth = 35
        player.colHeight = 35
        player.velocity = 7
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        player.y = 350
        pass

    @staticmethod
    def handle_event(player, e):
        if D_key_down(e) and player.dir == 0:  # 오른쪽으로 RUN
            player.dir, player.face_dir = 1, ''
        elif (D_key_up(e) and player.dir == 1) or (A_key_up(e) and player.dir == -1):
            player.dir = 0
        elif (D_key_down(e) and player.dir == -1) or (A_key_down(e) and player.dir == 1):
            player.dir = 0
        elif A_key_down(e) and player.dir == 0:  # 왼쪽으로 RUN
            player.dir, player.face_dir = -1, 'h'
        elif D_key_up(e) and player.dir == 0:
            player.dir, player.face_dir = -1, 'h'
        elif A_key_up(e) and player.dir == 0:
            player.dir, player.face_dir = 1, ''

    @staticmethod
    def do(player):
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(50, player.x, game_framework.screen_width - 50)
        player.frame = (player.frame + 9 * ACTION_PER_TIME * game_framework.frame_time) % 9
        if player.y + player.velocity >= 350:
            player.y += player.velocity
            player.velocity += player.gravity
        else:
            player.y = 350
            player.colWidth = 30
            player.colHeight = 60
            if player.dir != 0:
                player.state_machine.cur_state = Run
            else:
                player.dir = 0
                player.frame = 0
                player.state_machine.cur_state = Idle
            return

    @staticmethod
    def draw(player):
        player.image_jump.clip_composite_draw(int(player.frame) * (player.image_jump.w // 9), 0,
                                              player.image_jump.w // 9, player.image_jump.h,
                                              0, player.face_dir, player.x, player.y, (player.image_jump.w // 9) * 3,
                                              player.image_jump.h * 3)


class Attack:
    @staticmethod
    def enter(player, e):
        player.colWidth = 30
        player.colHeight = 60
        player.frame = 0
        player.attackSound.play(1)

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def handle_event(player, e):
        if D_key_down(e) and player.dir == 0:  # 오른쪽으로 RUN
            player.dir = 1
        elif (D_key_up(e) and player.dir == 1) or (A_key_up(e) and player.dir == -1):
            player.dir = 0
        elif (D_key_down(e) and player.dir == -1) or (A_key_down(e) and player.dir == 1):
            player.dir = 0
        elif A_key_down(e) and player.dir == 0:  # 왼쪽으로 RUN
            player.dir = -1
        elif D_key_up(e) and player.dir == 0:
            player.dir = -1
        elif A_key_up(e) and player.dir == 0:
            player.dir = 1

    @staticmethod
    def do(player):

        from Player2 import Player2
        if int(player.frame) == 2 and player.sword is None:
            if player.face_dir == '':
                p1 = (player.x, player.y - 40)
                p2 = (player.x + 150, player.y + 120)
                player.sword = Sword(p1, p2)
                game_world.add_object(player.sword, 1)
            elif player.face_dir == 'h':
                p1 = (player.x - 150, player.y - 40)
                p2 = (player.x, player.y + 120)
                player.sword = Sword(p1, p2)
                game_world.add_object(player.sword, 1)
            game_world.add_collision_pair("player2 : sword", None, player.sword)
        if player.frame >= 4.8:
            if player.dir != 0:
                player.state_machine.cur_state = Run
                game_world.remove_object(player.sword)
                player.sword = None
            else:
                player.dir = 0
                player.frame = 0
                player.state_machine.cur_state = Idle
                game_world.remove_object(player.sword)
                player.sword = None
            return
        player.frame = (player.frame + 5 * (1.0 / 0.3) * game_framework.frame_time) % 5

    @staticmethod
    def draw(player):
        player.image_attack.clip_composite_draw(int(player.frame) * (player.image_attack.w // 5), 0,
                                                player.image_attack.w // 5, player.image_attack.h,
                                                0, player.face_dir, player.x, player.y,
                                                (player.image_attack.w // 5) * 3,
                                                player.image_attack.h * 3)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = None
        self.transitions = {
            Idle: {D_key_down: Run, A_key_down: Run, A_key_up: Run, D_key_up: Run, space_down: Jump,
                   F_KEY_down: Attack},
            Run: {D_key_down: Idle, A_key_down: Idle, D_key_up: Idle, A_key_up: Idle, space_down: Jump,
                  F_KEY_down: Attack},
            Jump: {},
            Attack: {}
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
        self.cur_state.handle_event(self.player, e)
        return False

    def draw(self):
        self.cur_state.draw(self.player)


# Player Action Speed


class Player:
    def __init__(self):
        self.x, self.y = 100, 350
        self.frame = 0
        self.action = 3
        self.face_dir = ''
        self.dir = 0
        self.gravity = -0.07
        self.velocity = 0
        self.colWidth = 0
        self.colHeight = 0
        self.hp = 5
        self.image = load_image('resource/image/player1_idle.png')
        self.image_run = load_image('resource/image/player1_run.png')
        self.image_jump = load_image('resource/image/player1_jump.png')
        self.image_attack = load_image('resource/image/player1_attack.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.sword = None
        self.invincible = False
        self.alpha = 1.0
        self.attackSound = load_wav('resource/sound/attack.wav')
        self.hurt = load_wav('resource/sound/hurt.wav')
        self.attackSound.set_volume(30)
        self.hurt.set_volume(30)

    def update(self):
        self.state_machine.update()
        self.image.opacify(self.alpha)
        self.image_attack.opacify(self.alpha)
        self.image_jump.opacify(self.alpha)
        self.image_run.opacify(self.alpha)
        if int(self.invincible) > 0:
            self.invincible -= game_framework.frame_time
            self.alpha = math.sin(((5 - self.invincible) / 0.8) * math.pi)
        if int(self.invincible) == 0:
            self.alpha = 1

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def get_bb(self):
        return self.x - self.colWidth, self.y - self.colHeight, self.x + self.colWidth, self.y + self.colHeight

    def handle_collision(self, group, other):
        if group == 'player1 : sword' and int(self.invincible) == 0:
            self.invincible = 3.0
            self.hp -= 1
            self.alpha = 0.5
            self.hurt.play(1)
