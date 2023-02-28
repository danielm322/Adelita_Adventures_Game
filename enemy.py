import random
import time
import kivy.uix.image
from helper_fns import _get_enemy_start_end_positions, _get_line_slope_intercept, _find_kiss_endpoint_fast
from enemies_dict import enemies_dict


def spawn_enemy(self, screen_num, enemy_type, enemy_level, *args):
    curr_screen = self.root.screens[screen_num]
    # Randomly sample enemy speed
    r_speed_x = random.uniform(enemies_dict[enemy_type][enemy_level]['speed_min'],
                               enemies_dict[enemy_type][enemy_level]['speed_max'])
    # Get enemy start and end positions
    spawn_pos, finish_pos = _get_enemy_start_end_positions(self.side_bar_width,
                                                           enemy_type,
                                                           enemy_level)
    line_slope, line_intercept = _get_line_slope_intercept(spawn_pos, finish_pos)
    enemy = kivy.uix.image.Image(source=enemies_dict[enemy_type][enemy_level]['source'],
                                 size_hint=(enemies_dict[enemy_type][enemy_level]['width'],
                                            enemies_dict[enemy_type][enemy_level]['height']),
                                 pos_hint=spawn_pos, allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.enemies_ids['enemy_' + time_stamp] = {'image': enemy,
                                                      'type': enemy_type,
                                                      'level': enemy_level,
                                                      'finish_pos': finish_pos,
                                                      'fires_back': enemies_dict[enemy_type][enemy_level][
                                                              'fires_back'],
                                                      'hit_points':
                                                          enemies_dict[enemy_type][enemy_level][
                                                              'hit_points'],
                                                      'line_slope': line_slope,
                                                      'line_intercept': line_intercept,
                                                      'speed_x': - r_speed_x}  # Speed should be negative


def spawn_rocket_at_enemy_center_to_ch_center(self, screen_num, enemy_center, rocket_type, rocket_level):
    curr_screen = self.root.screens[screen_num]
    # enemy_center = enemy['image'].center  # List: [c_x, c_y]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    r_speed_x = random.uniform(enemies_dict[rocket_type][rocket_level]['speed_min'],
                               enemies_dict[rocket_type][rocket_level]['speed_max'])
    if enemy_center[0] > character_image_center[0]:
        r_speed_x = -r_speed_x
    finish_pos = _find_kiss_endpoint_fast(enemy_center,
                                          character_image_center,
                                          curr_screen.size,
                                          enemies_dict[rocket_type][rocket_level]['width'],
                                          enemies_dict[rocket_type][rocket_level]['height'],
                                          self.side_bar_width)
    start_pos_dict = {'x': enemy_center[0] * (1-self.side_bar_width) / curr_screen.size[0], 'y': enemy_center[1] / curr_screen.size[1]}
    finish_pos_dict = {'x': finish_pos[0] / curr_screen.size[0], 'y': finish_pos[1] / curr_screen.size[1]}
    line_slope, line_intercept = _get_line_slope_intercept(start_pos_dict, finish_pos_dict)
    rocket = kivy.uix.image.Image(source=enemies_dict[rocket_type][rocket_level]['source'],
                                  size_hint=(enemies_dict[rocket_type][rocket_level]['width'],
                                             enemies_dict[rocket_type][rocket_level]['height']),
                                  pos_hint=start_pos_dict, allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(rocket, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())

    curr_screen.enemies_ids['rocket_' + time_stamp] = {'image': rocket,
                                                       'type': rocket_type,
                                                       'level': rocket_level,
                                                       'finish_pos': finish_pos_dict,
                                                       'fires_back': enemies_dict[rocket_type][rocket_level][
                                                           'fires_back'],
                                                       'hit_points':
                                                           enemies_dict[rocket_type][rocket_level][
                                                               'hit_points'],
                                                       'line_slope': line_slope,
                                                       'line_intercept': line_intercept,
                                                       'speed_x': r_speed_x}


'''
def spawn_enemy(self, screen_num, *args):
    # Updating an enemy will need the save of an endpoint, line parameters, and enemy speed
    curr_screen = self.root.screens[screen_num]
    if not curr_screen.character_dict['killed']:
        r_speed_x = random.uniform(curr_screen.enemy_props['speed_min'],
                                   curr_screen.enemy_props['speed_max'])
        spawn_pos, finish_pos = _get_uniform_enemy_start_end_positions(self.side_bar_width,
                                                                       curr_screen.enemy_props['width'],
                                                                       curr_screen.enemy_props['height'])
        # Straight line equation parameters
        divisor = (finish_pos['x'] - spawn_pos['x'])
        if divisor == 0:
            divisor = 1e-6
        line_slope = (finish_pos['y'] - spawn_pos['y']) / divisor
        line_intercept = spawn_pos['y'] - spawn_pos['x'] * line_slope

        enemy = kivy.uix.image.Image(source="graphics/entities/enemy.png",
                                     size_hint=(curr_screen.enemy_props['width'], curr_screen.enemy_props['height']),
                                     pos_hint=spawn_pos, allow_stretch=True)
        curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
        # create a unique identifier for each enemy
        time_stamp = str(time.time())
        curr_screen.enemies_ids['enemy_' + time_stamp] = {'image': enemy,
                                                          'finish_pos': finish_pos,
                                                          'hitpoints': enemy_hit_points,
                                                          'line_slope': line_slope,
                                                          'line_intercept': line_intercept,
                                                          'speed_x': - r_speed_x}  # Speed should be negative
'''


def update_enemies(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        previous_x = enemy['image'].pos_hint['x']
        new_x = previous_x + enemy['speed_x'] * dt
        enemy['image'].pos_hint = {'x': new_x,
                                   'y': enemy['line_slope'] * new_x + enemy['line_intercept']}
        self.check_enemy_collision(enemy, screen_num)
        if enemy['type'] == 'fire' and enemy['speed_x'] > 0 and new_x >= enemy['finish_pos']['x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        elif enemy['type'] == 'fire' and enemy['speed_x'] < 0 and new_x <= enemy['finish_pos']['x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        elif enemy['type'] != 'fire' and new_x <= enemy['finish_pos']['x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]


def check_enemy_collision(self, enemy, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * enemies_dict[enemy['type']][enemy['level']]['width'] / 3
    gap_y = curr_screen.height * enemies_dict[enemy['type']][enemy['level']]['height'] / 1
    if enemy['image'].collide_widget(character_image) and \
            abs(enemy['image'].center[0] - character_image.center[0]) <= gap_x and \
            abs(enemy['image'].center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_dict['damage_received'] += enemies_dict[enemy['type']][enemy['level']]['damage']
        if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
            curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']

        self.adjust_character_life_bar(screen_num)
        if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
            self.kill_character(screen_num)


def enemy_animation_completed(self, enemy, screen_num):
    curr_screen = enemy['image'].parent.parent.parent
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy['image'])
    curr_screen.character_dict['damage_received'] += enemies_dict[enemy['type']][enemy['level']]['finishes_damage']
    if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
        curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
        self.kill_character(screen_num)

    self.adjust_character_life_bar(screen_num)
    if enemy['type'] != 'fire':
        self.sound_enemy_laughs.play()
