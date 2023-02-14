import random
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
import kivy.uix.image
import kivy.app
import kivy.uix.screenmanager
import kivy.animation
import kivy.core.audio
from os import getcwd
import kivy.uix.label
import time
from functools import partial

from kivy.properties import Clock


class GameApp(kivy.app.App):
    # side_bar_width = 0.05  # In screen percentage

    def screen_on_enter(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        Clock.schedule_interval(partial(self.spawn_enemy, screen_num), curr_screen.enemy_spawn_interval)

    def touch_down_handler(self, screen_num, args):
        # print(args[1].is_double_tap)
        curr_screen = self.root.screens[screen_num]
        if not curr_screen.character_killed and not args[1].is_double_tap:
            self.start_char_animation(screen_num, args[1].spos)

    # def on_toggle_button_state(self, widget, screen_num):
    #     curr_screen = self.root.screens[screen_num]
    #     # print("Toggle state:" + widget.state)
    #     if widget.state == "normal":
    #         curr_screen.shoot_state = False
    #     else:
    #         curr_screen.shoot_state = True

    def start_char_animation(self, screen_num, touch_pos):
        curr_screen = self.root.screens[screen_num]
        character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
        # character_image.im_num = character_image.start_im_num
        char_anim = kivy.animation.Animation(
            pos_hint={'x': (touch_pos[0] - character_image.size_hint[0] / 2),
                      'y': touch_pos[1] - character_image.size_hint[1] / 2},
            # pos=(touch_pos[0] - character_image.size[0] / 2,
            #      touch_pos[1] - character_image.size[1] / 2),
            duration=curr_screen.char_anim_duration
        )
        char_anim.start(character_image)

    def spawn_enemy(self, screen_num, *largs):
        enemy_width = 0.1
        enemy_height = 0.1
        curr_screen = self.root.screens[screen_num]
        # Choose starting side randomly: 0:left, 1:up, 2:right, 3:down
        r1_start = random.randint(0, 3)
        r2_start = random.random()
        r_finish = random.random()
        r_duration = random.uniform(curr_screen.enemy_anim_duration_min,
                                    curr_screen.enemy_anim_duration_max)
        if r1_start == 0:  # left
            spawn_pos = {'x': 0.0 - enemy_width, 'y': r2_start}
            finish_pos = {'x': 1.0, 'y': r_finish}
        elif r1_start == 1:  # up
            spawn_pos = {'x': r2_start, 'y': 1.0}
            finish_pos = {'x': r_finish, 'y': 0.0 - enemy_height}
        elif r1_start == 2:  # right
            spawn_pos = {'x': 1.0, 'y': r2_start}
            finish_pos = {'x': 0.0 - enemy_width, 'y': r_finish}
        else:  # down
            spawn_pos = {'x': r2_start, 'y': 0.0 - enemy_height}
            finish_pos = {'x': r_finish, 'y': 1.0}
        enemy = kivy.uix.image.Image(source="graphics/entities/enemy.png",
                                     size_hint=(enemy_width, enemy_height),
                                     pos_hint=spawn_pos, allow_stretch=True)
        curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
        # create a unique identifier for each enemy
        time_stamp = str(time.time())
        curr_screen.enemies_ids['enemy_' + time_stamp] = enemy
        enemy_anim = kivy.animation.Animation(pos_hint=finish_pos,
                                              duration=r_duration)
        enemy_anim.bind(on_complete=partial(self.enemy_animation_completed, enemy, time_stamp, screen_num))
        enemy_anim.start(enemy)

    def enemy_animation_completed(self, enemy, time_stamp, screen_num, *args):
        # enemy_image = args[1]
        curr_screen = enemy.parent.parent
        kivy.animation.Animation.cancel_all(enemy)
        curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy)
        del curr_screen.enemies_ids['enemy_' + time_stamp]


class MainScreen(kivy.uix.screenmanager.Screen):
    pass


class Level1(kivy.uix.screenmanager.Screen):
    character_killed = False
    shoot_state = False
    char_anim_duration = 0.7
    rewards_ids = {}
    enemies_ids = {}
    enemy_anim_duration_min = 4.0
    enemy_anim_duration_max = 7.0
    enemy_spawn_interval = 3  # In seconds


class Level2(kivy.uix.screenmanager.Screen):
    character_killed = False
    shoot_state = False
    char_anim_duration = 0.7
    rewards_ids = {}
    enemies_ids = {}
    enemy_anim_duration_min = 4.0
    enemy_anim_duration_max = 7.0
    enemy_spawn_interval = 3  # In seconds


app = GameApp()
app.run()
