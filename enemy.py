import random
import time
import kivy.uix.image
from helper_fns import _get_enemy_start_end_positions, _find_kiss_endpoint_fast, get_direction_unit_vector
from enemies_dict import enemies_dict


def spawn_enemy(self, screen_num, enemy_type, enemy_level, *args):
    curr_screen = self.root.screens[screen_num]
    # Randomly sample enemy speed
    r_speed = random.uniform(enemies_dict[enemy_type][enemy_level]['speed_min'],
                             enemies_dict[enemy_type][enemy_level]['speed_max'])
    # Get enemy start and end positions
    start_pos, finish_pos = _get_enemy_start_end_positions(self.side_bar_width,
                                                           enemy_type,
                                                           enemy_level,
                                                           curr_screen.size)
    # Get enemy direction unit vector
    enemy_direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    # Instantiate image
    enemy = kivy.uix.image.Image(source=enemies_dict[enemy_type][enemy_level]['source'],
                                 size_hint=(enemies_dict[enemy_type][enemy_level]['width'],
                                            enemies_dict[enemy_type][enemy_level]['height']),
                                 pos=start_pos,
                                 # pos_hint=start_pos,
                                 allow_stretch=True)
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
                                                      'direction_u_vector': enemy_direction_unit_vector,
                                                      'speed': r_speed}


def spawn_rocket_at_enemy_center_to_ch_center(self, screen_num, enemy_center, rocket_type, rocket_level):
    curr_screen = self.root.screens[screen_num]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    r_speed = random.uniform(enemies_dict[rocket_type][rocket_level]['speed_min'],
                             enemies_dict[rocket_type][rocket_level]['speed_max'])
    finish_pos = _find_kiss_endpoint_fast(enemy_center,
                                          character_image_center,
                                          curr_screen.size,
                                          enemies_dict[rocket_type][rocket_level]['width'],
                                          enemies_dict[rocket_type][rocket_level]['height'],
                                          self.side_bar_width)
    direction_unit_vector = get_direction_unit_vector(enemy_center, finish_pos)
    rocket = kivy.uix.image.Image(source=enemies_dict[rocket_type][rocket_level]['source'],
                                  size_hint=(enemies_dict[rocket_type][rocket_level]['width'],
                                             enemies_dict[rocket_type][rocket_level]['height']),
                                  pos=enemy_center,
                                  allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(rocket, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.enemies_ids['rocket_' + time_stamp] = {'image': rocket,
                                                       'type': rocket_type,
                                                       'level': rocket_level,
                                                       'finish_pos': finish_pos,
                                                       'fires_back': enemies_dict[rocket_type][rocket_level][
                                                           'fires_back'],
                                                       'hit_points':
                                                           enemies_dict[rocket_type][rocket_level][
                                                               'hit_points'],
                                                       'direction_u_vector': direction_unit_vector,
                                                       'speed': r_speed}


def update_enemies(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        new_x = enemy['image'].x + enemy['direction_u_vector'][0] * enemy['speed'] * dt
        new_y = enemy['image'].y + enemy['direction_u_vector'][1] * enemy['speed'] * dt
        enemy['image'].x = new_x
        enemy['image'].y = new_y
        # new_x = enemy['image'].pos_hint['x'] + enemy['direction_u_vector'][0] * enemy['speed'] * dt
        # new_y = enemy['image'].pos_hint['y'] + enemy['direction_u_vector'][1] * enemy['speed'] * dt
        # enemy['image'].pos_hint['x'] = new_x
        # enemy['image'].pos_hint['y'] = new_y
        self.check_enemy_collision(enemy, screen_num)
        if enemy['type'] == 'fire' and enemy['direction_u_vector'][0] > 0 and new_x >= enemy['finish_pos'][0]:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        elif enemy['type'] == 'fire' and enemy['direction_u_vector'][0] < 0 and new_x <= enemy['finish_pos'][0]:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        elif enemy['type'] != 'fire' and new_x <= enemy['finish_pos'][0]:
        # elif enemy['type'] != 'fire' and new_x <= enemy['finish_pos']['x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]


def check_enemy_collision(self, enemy, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    if enemy['type'] != 'fire':
        gap_x = curr_screen.width * enemies_dict[enemy['type']][enemy['level']]['width'] / 3
        gap_y = curr_screen.height * enemies_dict[enemy['type']][enemy['level']]['height'] / 1
    else:
        gap_x = curr_screen.width * enemies_dict[enemy['type']][enemy['level']]['width'] / 1.2
        gap_y = curr_screen.height * enemies_dict[enemy['type']][enemy['level']]['height'] / 0.8
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
