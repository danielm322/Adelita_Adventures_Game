import time
from typing import Tuple
import kivy.uix.image
# from kivy.graphics import Color, Quad
from kivy.utils import platform
from functools import partial
from math import sin

from src.helper_fns import (
    get_direction_unit_vector,
    # get_entity_bbox,
    write_level_passed
)

boss_properties = {
    'level_1': {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 25,
        'damage': 1,
        'speed': 1.5e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/diaper.png",
        'fires_back': False,
        'trajectory_type': 'linear'
    },
    'level_2': {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.6e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': False,
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.2,
        'period': 15
    },
    'level_3': {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.3e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.2,
        'period': 15
    },
    'level_4': {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.3e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.3,
        'period': 15
    },
    'level_6': {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15
    }
}


def spawn_boss(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    screen_size_ratio = curr_screen.size[1] / curr_screen.size[0]
    start_pos = {
        'center_x': 1.0 + curr_screen.boss_props['width'] / 2,
        'center_y': 0.5
    }
    finish_pos = {
        'center_x': 0. + self.SIDE_BAR_WIDTH,
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
    bosses_to_delete = []
    for boss_key, boss in curr_screen.bosses_ids.items():
        boss['is_fighting'], boss_to_eliminate = self.check_boss_collision(boss, screen_num)
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
        if boss['image'].center_x <= self.SIDE_BAR_WIDTH * curr_screen.size[0]:
            self.boss_arrives_animation(screen_num)

        if boss_to_eliminate:
            bosses_to_delete.append(boss_key)

    if len(bosses_to_delete) > 0:
        for boss_key in bosses_to_delete:
            del curr_screen.bosses_ids[boss_key]


def boss_arrives_animation(self, screen_num):
    # Triggered when boss arrives to the finish line
    curr_screen = self.root.screens[screen_num]
    for character in curr_screen.characters_dict.values():
        character['damage_received'] = character['hit_points']
        self.adjust_character_life_bar(screen_num, character)
        self.begin_kill_character(screen_num, character)


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


def check_boss_collision(self, boss_dict, screen_num) -> Tuple[bool, bool]:
    is_fighting_flag = False
    curr_screen = self.root.screens[screen_num]
    # Flag to see if boss has been eliminated by melee attacking
    boss_to_eliminate_flag = False
    gap_x = curr_screen.width * curr_screen.boss_props['width'] / 4
    gap_y = curr_screen.height * curr_screen.boss_props['height'] / 2
    for character in curr_screen.characters_dict.values():
        character_image = curr_screen.ids[character['name'] + str(screen_num)]
        if boss_dict['image'].collide_widget(character_image) and \
                abs(boss_dict['image'].center[0] - character_image.center[0]) <= gap_x and \
                abs(boss_dict['image'].center[1] - character_image.center[1]) <= gap_y:
            is_fighting_flag = True
            character['damage_received'] += curr_screen.boss_props['damage']
            if character['melee_attacks']:
                character['current_state'] = 'melee_attacking'
                character['is_fighting'] = True
                boss_dict['hit_points'] = boss_dict['hit_points'] - character['melee_damage']
                if boss_dict['hit_points'] <= 0:
                    self.kill_boss(boss_dict, screen_num)
                    write_level_passed(platform, screen_num)
                    boss_to_eliminate_flag = True
                    character['current_state'] = 'idle'
                    character['is_fighting'] = False
            if character['damage_received'] > character['hit_points']:
                character['damage_received'] = character['hit_points']
            self.adjust_character_life_bar(screen_num, character)
            if character['damage_received'] >= character['hit_points']:
                if not character['current_state'] == 'dead':
                    self.begin_kill_character(screen_num, character)
    return is_fighting_flag, boss_to_eliminate_flag


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
