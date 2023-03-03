import time
# import random
import kivy.uix.image
from functools import partial

from helper_fns import get_direction_unit_vector


def spawn_boss(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    # spawn_pos = (curr_screen.size[0],
    #              curr_screen.size[1] * (0.5 - curr_screen.boss_props['height'] / 2))
    screen_size_ratio = curr_screen.size[1] / curr_screen.size[0]
    start_pos = {
        'x': 1.0,
        'y': 0.5 - curr_screen.boss_props['height'] / 2
    }
    # finish_pos = (0,
    #               curr_screen.size[1] * (0.5 - curr_screen.boss_props['height'] / 2))
    finish_pos = {
        'x': 0.,
        'y': 0.5 - curr_screen.boss_props['height'] / 2
    }
    direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    boss = kivy.uix.image.Image(source=curr_screen.boss_props['source'],
                                size_hint=(curr_screen.boss_props['width'] * screen_size_ratio,
                                           curr_screen.boss_props['height']),
                                # pos=spawn_pos,
                                pos_hint=start_pos,
                                allow_stretch=True,
                                keep_ratio=False)
    curr_screen.add_widget(boss, index=-1)
    time_stamp = str(time.time())
    curr_screen.bosses_ids['boss_' + time_stamp] = {'image': boss,
                                                    'hit_points': curr_screen.boss_props['hit_points'],
                                                    'finish_pos': finish_pos,
                                                    'speed': curr_screen.boss_props['speed'],
                                                    'direction_u_vector': direction_unit_vector,
                                                    }


def update_bosses(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    for boss_key, boss in curr_screen.bosses_ids.items():
        new_x = boss['image'].pos_hint['x'] + boss['direction_u_vector'][0] * boss['speed'] * dt
        new_y = boss['image'].pos_hint['y'] + boss['direction_u_vector'][1] * boss['speed'] * dt
        boss['image'].pos_hint['x'] = new_x
        boss['image'].pos_hint['y'] = new_y
        boss['image'].x = new_x * curr_screen.size[0]
        boss['image'].y = new_y * curr_screen.size[1]

        # boss['image'].x = boss['image'].x + boss['speed_x'] * dt
        self.check_boss_collision(boss['image'], screen_num)

        if boss['image'].x <= 0. - boss['image'].width / 4:
            self.boss_arrives_animation(screen_num)


def boss_arrives_animation(self, screen_num):
    # Triggered when boss arrives to the finish line
    curr_screen = self.root.screens[screen_num]
    curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
    self.adjust_character_life_bar(screen_num)
    self.kill_character(screen_num)


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


def check_boss_collision(self, boss_image, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * curr_screen.boss_props['width'] / 4
    gap_y = curr_screen.height * curr_screen.boss_props['height'] / 2
    if boss_image.collide_widget(character_image) and \
            abs(boss_image.center[0] - character_image.center[0]) <= gap_x and \
            abs(boss_image.center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_dict['damage_received'] += curr_screen.boss_props['damage']
        if curr_screen.character_dict['damage_received'] > curr_screen.character_dict['hit_points']:
            curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
            self.adjust_character_life_bar(screen_num)
        if curr_screen.character_dict['damage_received'] == curr_screen.character_dict['hit_points']:
            self.kill_character(screen_num)


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