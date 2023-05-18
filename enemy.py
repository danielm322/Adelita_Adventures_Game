import random
import time
from typing import Tuple

import kivy.uix.image
# from kivy.graphics import Line

from helper_fns import _get_enemy_start_end_positions, _find_kiss_endpoint_fast, get_direction_unit_vector
from enemies_dict import enemies_dict
from character import update_character_image_animation


def spawn_enemy(self, screen_num, enemy_type, enemy_level, *args):
    curr_screen = self.root.screens[screen_num]
    screen_size_ratio = curr_screen.size[1] / curr_screen.size[0]
    # Randomly sample enemy speed
    r_speed = random.uniform(enemies_dict[enemy_type][enemy_level]['speed_min'],
                             enemies_dict[enemy_type][enemy_level]['speed_max'])
    # Get enemy start and end positions
    start_pos, finish_pos = _get_enemy_start_end_positions(self.SIDE_BAR_WIDTH,
                                                           enemy_type,
                                                           enemy_level,
                                                           curr_screen.size)
    # Get enemy direction unit vector
    enemy_direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    # Instantiate image
    enemy = kivy.uix.image.Image(source=enemies_dict[enemy_type][enemy_level]['source'],
                                 # size_hint=(None,
                                 size_hint=(enemies_dict[enemy_type][enemy_level]['width'] * screen_size_ratio,
                                            enemies_dict[enemy_type][enemy_level]['height']),
                                 # pos=start_pos,
                                 pos_hint=start_pos,
                                 allow_stretch=True,
                                 keep_ratio=False)
    # curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
    curr_screen.add_widget(enemy, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.enemies_ids['enemy_' + time_stamp] = {'image': enemy,
                                                      'type': enemy_type,
                                                      'level': enemy_level,
                                                      'finish_pos': finish_pos,
                                                      'hit_points':
                                                          enemies_dict[enemy_type][enemy_level][
                                                              'hit_points'],
                                                      'direction_u_vector': enemy_direction_unit_vector,
                                                      'is_fighting': False,
                                                      'reward_probability': enemies_dict[enemy_type][enemy_level][
                                                          'spawn_reward_probability'],
                                                      'speed': r_speed}


def spawn_rocket_at_enemy_center_to_ch_center(self,
                                              screen_num: int,
                                              enemy_center_pixels: tuple,
                                              rocket_key: str,
                                              rocket_type: str,
                                              rocket_level: str):
    """
    Spawns fire from an enemy to the character center that shot the rocket on the neemy
    :param screen_num: Screen number
    :param enemy_center_pixels: Center of the enemy that received the rocket and who will spawn fire
    :param rocket_key: Name of the rocket that already impacted the enemy (Rocket started from a character).
        Can be a kiss, special starting from the main character, or a banana, starting from Aux char 1
    :param rocket_type: Rocket type that will be shot by the enemy
    :param rocket_level: Rocket level that will be shot by the enemy
    :return: None
    """
    curr_screen = self.root.screens[screen_num]
    # This would mean the main character shot the rocket
    if ('kiss' in rocket_key) or ('special' in rocket_key):
        character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    # This would mean the aux char 1 shot the rocket
    elif 'aux_char_1' in rocket_key:
        character_image_center = curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    r_speed = random.uniform(enemies_dict[rocket_type][rocket_level]['speed_min'],
                             enemies_dict[rocket_type][rocket_level]['speed_max'])
    finish_pos_pixels = _find_kiss_endpoint_fast(enemy_center_pixels,
                                                 character_image_center,
                                                 curr_screen.size,
                                                 enemies_dict[rocket_type][rocket_level]['width'],
                                                 enemies_dict[rocket_type][rocket_level]['height'],
                                                 self.SIDE_BAR_WIDTH)
    start_pos = {
        'center_x': enemy_center_pixels[0] / curr_screen.size[0],
        'center_y': enemy_center_pixels[1] / curr_screen.size[1],
    }
    finish_pos = {
        'center_x': finish_pos_pixels[0] / curr_screen.size[0],
        'center_y': finish_pos_pixels[1] / curr_screen.size[1]
    }
    direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    rocket = kivy.uix.image.Image(source=enemies_dict[rocket_type][rocket_level]['source'],
                                  size_hint=(enemies_dict[rocket_type][rocket_level]['width'],
                                             enemies_dict[rocket_type][rocket_level]['height']),
                                  pos_hint=start_pos,
                                  allow_stretch=True,
                                  keep_ratio=False)
    curr_screen.add_widget(rocket, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.enemies_ids['rocket_' + time_stamp] = {'image': rocket,
                                                       'type': rocket_type,
                                                       'level': rocket_level,
                                                       'finish_pos': finish_pos,
                                                       'hit_points':
                                                           enemies_dict[rocket_type][rocket_level][
                                                               'hit_points'],
                                                       'direction_u_vector': direction_unit_vector,
                                                       'speed': r_speed}


def spawn_enemy_underling(self, screen_num, start_pos, finish_pos, underlings_level):
    curr_screen = self.root.screens[screen_num]
    screen_size_ratio = curr_screen.size[1] / curr_screen.size[0]
    # Randomly sample enemy speed
    r_speed = random.uniform(enemies_dict['underlings'][underlings_level]['speed_min'],
                             enemies_dict['underlings'][underlings_level]['speed_max'])
    # Get enemy direction unit vector
    enemy_direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    # Instantiate image
    enemy = kivy.uix.image.Image(source=enemies_dict['underlings'][underlings_level]['source'],
                                 # size_hint=(None,
                                 size_hint=(enemies_dict['underlings'][underlings_level]['width'] * screen_size_ratio,
                                            enemies_dict['underlings'][underlings_level]['height']),
                                 # pos=start_pos,
                                 pos_hint=start_pos,
                                 allow_stretch=True,
                                 keep_ratio=False)
    # curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
    curr_screen.add_widget(enemy, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.enemies_ids['enemy_' + time_stamp] = {'image': enemy,
                                                      'type': 'underlings',
                                                      'level': underlings_level,
                                                      'finish_pos': finish_pos,
                                                      'hit_points':
                                                          enemies_dict['underlings'][underlings_level][
                                                              'hit_points'],
                                                      'direction_u_vector': enemy_direction_unit_vector,
                                                      'is_fighting': False,
                                                      'reward_probability': enemies_dict['underlings'][underlings_level][
                                                          'spawn_reward_probability'],
                                                      'speed': r_speed}


def update_enemies(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        enemy['is_fighting'], to_eliminate_flag = self.check_enemy_collision(enemy, screen_num, dt)
        if enemy['type'] == 'fire' or not enemy['is_fighting']:
            new_x = enemy['image'].pos_hint['center_x'] + enemy['direction_u_vector'][0] * enemy['speed'] * dt
            new_y = enemy['image'].pos_hint['center_y'] + enemy['direction_u_vector'][1] * enemy['speed'] * dt
            enemy['image'].pos_hint['center_x'] = new_x
            enemy['image'].pos_hint['center_y'] = new_y
            enemy['image'].center_x = new_x * curr_screen.size[0]
            enemy['image'].center_y = new_y * curr_screen.size[1]

        # with curr_screen.canvas:
        #     Line(circle=(enemy['image'].center_x, enemy['image'].center_y, 20))
        # Remove fire if it has reached any border of the screen:
        if enemy['type'] == 'fire' \
                and (
                   (enemy['direction_u_vector'][0] < 0 and new_x <= enemy['finish_pos']['center_x'])
                or (enemy['direction_u_vector'][0] > 0 and new_x >= enemy['finish_pos']['center_x'])
                or (enemy['direction_u_vector'][1] > 0 and new_y >= enemy['finish_pos']['center_y'])
                or (enemy['direction_u_vector'][1] < 0 and new_y <= enemy['finish_pos']['center_y'])
        ):
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        # Remove fire if it has collided with a character:
        if enemy['type'] == 'fire' and to_eliminate_flag:
            self.remove_fire_from_screen(enemy['image'], screen_num)
            enemies_to_delete.append(enemy_key)
        # Remove enemies that have reached the left side of the screen and apply their damage
        elif enemy['type'] != 'fire' and enemy['image'].pos_hint['center_x'] <= enemy['finish_pos']['center_x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy, screen_num)
        # Remove other enemies that have died because of melee attacks from a character
        if enemy['type'] != 'fire' and to_eliminate_flag:
            enemies_to_delete.append(enemy_key)

    if len(enemies_to_delete) > 0:
        # First convert to set to remove possible duplicates
        clear_list = list(set(enemies_to_delete))
        for enemy_key in clear_list:
            del curr_screen.enemies_ids[enemy_key]


def check_enemy_collision(self, enemy, screen_num, dt) -> Tuple[bool, bool]:
    # Flag to check if an enemy is colliding with a character, it stops its movement to deal damage (fight)
    is_fighting = False
    # Flag to check if an enemy has to be eliminated because of losing its hit points in melee fight
    # or because it is a fire, and it collides with a character
    to_eliminate_flag = False
    curr_screen = self.root.screens[screen_num]
    if enemy['type'] != 'fire':
        gap_x = curr_screen.width * enemies_dict[enemy['type']][enemy['level']]['width'] / 4
        gap_y = curr_screen.height * enemies_dict[enemy['type']][enemy['level']]['height'] / 1.5
    else:
        gap_x = curr_screen.width * enemies_dict[enemy['type']][enemy['level']]['width'] / 1.2
        gap_y = curr_screen.height * enemies_dict[enemy['type']][enemy['level']]['height'] / 0.8
    for character in curr_screen.characters_dict.values():
        # Safe proof that if character is not fighting their not fighting flag is false
        # In this context fighting means dealing melee damage
        character['is_fighting'] = False
        character_image = curr_screen.ids[character['name'] + str(screen_num)]
        if enemy['image'].collide_widget(character_image) and \
                abs(enemy['image'].center[0] - character_image.center[0]) <= gap_x and \
                abs(enemy['image'].center[1] - character_image.center[1]) <= gap_y:
            # This flag is for the enemy
            is_fighting = True
            # Enemy deals damage to character
            character['damage_received'] += enemies_dict[enemy['type']][enemy['level']]['damage']
            # If character deals melee damage, character deals damage to enemy
            if character['melee_attacks']:
                character['current_state'] = 'melee_attacking'
                character['is_fighting'] = True
                enemy['hit_points'] = enemy['hit_points'] - character['melee_damage']
                # Update image of fighting character
                # update_character_image_animation(self, screen_num, character, dt)
                if enemy['hit_points'] <= 0:
                    to_eliminate_flag = True
                    self.kill_enemy(enemy['image'], screen_num, enemy['reward_probability'])
                    character['current_state'] = 'idle'
                    character['is_fighting'] = False

            if character['damage_received'] >= character['hit_points']:
                character['damage_received'] = character['hit_points']
            # Implement special ability of launching a character
            if 'launches_character' in enemies_dict[enemy['type']][enemy['level']].keys():
                self.launch_character(character, enemy, screen_num)

            self.adjust_character_life_bar(screen_num, character)
            if character['damage_received'] >= character['hit_points']:
                if not character['current_state'] == 'dead':
                    self.begin_kill_character(screen_num, character)
            # Eliminate fires at first collision
            if enemy['type'] == 'fire':
                to_eliminate_flag = True

    return is_fighting, to_eliminate_flag


def launch_character(self, character_dict, enemy, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids[character_dict['name'] + str(screen_num)]
    random_number = random.randint(0, 1)
    if random_number == 0:
        new_y = character_image.center_y + enemies_dict[enemy['type']][enemy['level']]['character_y_displacement'] * \
            curr_screen.size[1]
    else:
        new_y = character_image.center_y - enemies_dict[enemy['type']][enemy['level']]['character_y_displacement'] * \
            curr_screen.size[1]
    character_image.center_y = new_y
    remaining_life_percent_lvl_widget = curr_screen.ids[character_dict['life_bar_id'] + str(screen_num)]
    remaining_life_percent_lvl_widget.x = character_image.x
    remaining_life_percent_lvl_widget.y = character_image.top
    character_dict['is_moving'] = False


def enemy_animation_completed(self, enemy, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.remove_widget(enemy['image'])
    for character in curr_screen.characters_dict.values():
        character['damage_received'] += enemies_dict[enemy['type']][enemy['level']]['finishes_damage']
        if character['damage_received'] >= character['hit_points']:
            character['damage_received'] = character['hit_points']
            if not character['current_state'] == 'dead':
                self.begin_kill_character(screen_num, character)
        
        self.adjust_character_life_bar(screen_num, character)
        if enemy['type'] != 'fire':
            self.sound_enemy_laughs.play()


def kill_enemy(self, enemy_image, screen_num, reward_probability):
    curr_screen = self.root.screens[screen_num]
    self.sound_enemy_dies.play()
    enemy_center = enemy_image.center
    curr_screen.remove_widget(enemy_image)
    # Spawn reward with probability defined per level and per enemy
    if random.random() < reward_probability:
        self.spawn_reward(enemy_center, screen_num)


def remove_fire_from_screen(self, enemy_image, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.remove_widget(enemy_image)