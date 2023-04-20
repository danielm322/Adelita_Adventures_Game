import time
# import random
import kivy.uix.image
from kivy.graphics import Color, Quad
from functools import partial
from math import sin

from helper_fns import get_direction_unit_vector, get_entity_bbox


def spawn_boss(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    screen_size_ratio = curr_screen.size[1] / curr_screen.size[0]
    start_pos = {
        'center_x': 1.0 + curr_screen.boss_props['width'] / 2,
        'center_y': 0.5
    }
    finish_pos = {
        'center_x': 0. + self.side_bar_width,
        'center_y': 0.5
    }
    direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    boss = kivy.uix.image.Image(source=curr_screen.boss_props['source'],
                                size_hint=(curr_screen.boss_props['width'] * screen_size_ratio,
                                           curr_screen.boss_props['height']),
                                pos_hint=start_pos,
                                allow_stretch=True,
                                keep_ratio=False)
    curr_screen.add_widget(boss, index=-1)
    time_stamp = str(time.time())
    curr_screen.bosses_ids['boss_' + time_stamp] = {'image': boss,
                                                    'hit_points': curr_screen.boss_props['hit_points'],
                                                    'direction_u_vector': direction_unit_vector,
                                                    'is_fighting': False
                                                    }
    # For debugging: show the bounding box of the boss
    # with curr_screen.canvas:
    #     Color(1, 0, 0, 0.2)
    #     self.entity_bounding_box = Quad(points=get_entity_bbox(boss))


def update_bosses(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    for boss_key, boss in curr_screen.bosses_ids.items():
        boss['is_fighting'] = self.check_boss_collision(boss['image'], screen_num)
        if not boss['is_fighting']:
            new_x = boss['image'].pos_hint['center_x'] + \
                    boss['direction_u_vector'][0] * curr_screen.boss_props['speed'] * dt
            if curr_screen.boss_props['trajectory_type'] == 'linear':
                new_y = boss['image'].pos_hint['center_y'] + \
                        boss['direction_u_vector'][1] * curr_screen.boss_props['speed'] * dt
            else:
                if curr_screen.boss_props['trajectory_function'] == 'sine':
                    new_y = 0.5 + curr_screen.boss_props['amplitude'] * sin(curr_screen.boss_props['period'] * new_x)**2
            boss['image'].pos_hint['center_x'] = new_x
            boss['image'].pos_hint['center_y'] = new_y
            boss['image'].center_x = new_x * curr_screen.size[0]
            boss['image'].center_y = new_y * curr_screen.size[1]
        # self.entity_bounding_box.points = get_entity_bbox(boss['image'])

        # if boss['image'].x <= boss['finish_pos']['x'] * curr_screen.size[0]:
        if boss['image'].center_x <= self.side_bar_width * curr_screen.size[0]:
            self.boss_arrives_animation(screen_num)


def boss_arrives_animation(self, screen_num):
    # Triggered when boss arrives to the finish line
    curr_screen = self.root.screens[screen_num]
    for character in curr_screen.characters_dict.values():
        character['damage_received'] = character['hit_points']
        self.adjust_character_life_bar(screen_num, character)
        self.kill_character(screen_num, character)


def boss_defeat_animation_start(self, boss, screen_num):
    # Triggered when boss is defeated
    curr_screen = self.root.screens[screen_num]
    # new_pos = (curr_screen.size[0],
    #            curr_screen.size[1] * 0.5)
    new_pos = {
        'x': 1,
        'y': 0.5 - curr_screen.boss_props['height'] / 2
    }
    boss_defeat_anim = kivy.animation.Animation(pos_hint=new_pos,
                                                size_hint=(0.1, 0.1),
                                                duration=0.6,
                                                transition='in_out_elastic')
    boss_defeat_anim.bind(on_complete=partial(self.boss_defeat_animation_finish, screen_num))
    boss_defeat_anim.start(boss)


def boss_defeat_animation_finish(self, screen_num, *args):
    boss = args[1]
    curr_screen = self.root.screens[screen_num]
    curr_screen.remove_widget(boss)


def check_boss_collision(self, boss_image, screen_num) -> bool:
    is_fighting_flag = False
    curr_screen = self.root.screens[screen_num]

    gap_x = curr_screen.width * curr_screen.boss_props['width'] / 4
    gap_y = curr_screen.height * curr_screen.boss_props['height'] / 2
    for character in curr_screen.characters_dict.values():
        character_image = curr_screen.ids[character['name'] + str(screen_num)]
        if boss_image.collide_widget(character_image) and \
                abs(boss_image.center[0] - character_image.center[0]) <= gap_x and \
                abs(boss_image.center[1] - character_image.center[1]) <= gap_y:
            is_fighting_flag = True
            character['damage_received'] += curr_screen.boss_props['damage']
            if character['damage_received'] > character['hit_points']:
                character['damage_received'] = character['hit_points']
            self.adjust_character_life_bar(screen_num, character)
            if character['damage_received'] == character['hit_points']:
                self.kill_character(screen_num, character)
    return is_fighting_flag


def kill_boss(self, boss, screen_num):
    curr_screen = self.root.screens[screen_num]
    self.sound_level_play.stop()
    self.sound_level_finished.play()
    boss_center = boss['image'].center
    # Stop enemies animations if they exist
    for _, enemy in curr_screen.enemies_ids.items():
        enemy['speed'] = 0.
    # Animate boss killing
    self.boss_defeat_animation_start(boss['image'], screen_num)
    # Spawn boss reward
    self.spawn_boss_reward(boss_center, screen_num)
    # curr_screen.phase_1_completed = False
    kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 6)