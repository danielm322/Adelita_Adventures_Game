import random

import kivy.animation
from functools import partial
from kivy.clock import Clock
# from kivy.graphics import Line

# from math import sqrt

from enemies_dict import enemies_dict
from helper_fns import get_direction_unit_vector


def start_character_animation(self, screen_num, touch_pos):
    curr_screen = self.root.screens[screen_num]
    # screen_size = curr_screen.size  # List [size_x, size_y]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    # character_image.im_num = character_image.start_im_num
    character_image_center = character_image.center  # List: [c_x, c_y]
    finish_pos = (touch_pos[0], touch_pos[1])
    direction_unit_vector = get_direction_unit_vector(character_image_center, touch_pos)
    curr_screen.character_dict['is_moving'] = True
    curr_screen.character_dict['finish_point_pos'] = finish_pos
    curr_screen.character_dict['direction_unit_vector'] = direction_unit_vector


def update_character(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    if curr_screen.character_dict['is_moving'] and not curr_screen.character_dict['killed']:
        character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
        new_x = character_image.center_x +\
                curr_screen.character_dict['direction_unit_vector'][0] * curr_screen.character_dict['speed'] * dt
        new_y = character_image.center_y +\
                curr_screen.character_dict['direction_unit_vector'][1] * curr_screen.character_dict['speed'] * dt
        character_image.center_x = new_x
        character_image.center_y = new_y
        # self.char_bounding_box.points = self.get_character_bbox(screen_num)
        # with curr_screen.canvas:
        #     Line(circle=(character_image.center_x, character_image.center_y, 10))
        # Update special attack radius quad
        if curr_screen.character_dict['shoot_special_state']:
            self.special_attack_properties['quad'].points = self.get_special_quad_coords(screen_num)
        # Check collision
        self.check_character_collision(character_image, screen_num)
        # Stop moving character if he arrived to the final point
        if abs(
                character_image.center_x - curr_screen.character_dict['finish_point_pos'][0]
        ) < self.MOVEMENT_PIXEL_TOLERANCE \
                and abs(
            character_image.center_y - curr_screen.character_dict['finish_point_pos'][1]
        ) < self.MOVEMENT_PIXEL_TOLERANCE:
            curr_screen.character_dict['is_moving'] = False


def check_character_collision(self, character_image, screen_num):
    curr_screen = self.root.screens[screen_num]
    gap_x = curr_screen.width * self.reward_width / 3
    gap_y = curr_screen.height * self.reward_height / 1.5
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        if character_image.collide_widget(reward['image']) and \
                abs(character_image.center[0] - reward['image'].center[0]) <= gap_x and \
                abs(character_image.center[1] - reward['image'].center[1]) <= gap_y:
            rewards_to_delete.append(reward_key)
            curr_screen.remove_widget(reward['image'])
            curr_screen.rewards_gathered += 1
            self.sound_reward_collected.play()
            # Update reward widget
            if not curr_screen.phase_1_completed:
                if curr_screen.rewards_gathered > curr_screen.rewards_to_win_ph_1:
                    curr_screen.rewards_gathered = curr_screen.rewards_to_win_ph_1

                curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
                    curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_1)
            elif curr_screen.phase_1_completed and curr_screen.number_of_phases == 3:
                if curr_screen.rewards_gathered > curr_screen.rewards_to_win_ph_2:
                    curr_screen.rewards_gathered = curr_screen.rewards_to_win_ph_2

                curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
                    curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_2)
            if not curr_screen.phase_1_completed and curr_screen.rewards_gathered == curr_screen.rewards_to_win_ph_1:
                # Stop spawning enemies phase 1
                self.clock_spawn_enemies_variable.cancel()
                self.clock_spawn_enemies_variable = None
                curr_screen.phase_1_completed = True
                if curr_screen.number_of_phases == 2:
                    self.spawn_boss(screen_num)

                elif curr_screen.number_of_phases == 3:
                    if enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                        'spawn_function'] == 'gaussian':
                        enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                            'spawn_point'] = random.random()
                        enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                            'end_point'] = random.random()
                        if curr_screen.enemy_phase_2['type'] == 'yellow':
                            enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                                'spawn_point'] *= 0.9
                            enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                                'end_point'] *= 0.9
                    self.clock_spawn_enemies_variable = Clock.schedule_interval(
                        partial(self.spawn_enemy,
                                screen_num,
                                curr_screen.enemy_phase_2['type'],
                                curr_screen.enemy_phase_2['level']),
                        enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']][
                            'spawn_interval']
                    )
                    curr_screen.rewards_gathered = 0
                    curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
                        curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_2)

            elif curr_screen.number_of_phases == 3 \
                    and not curr_screen.phase_2_completed \
                    and curr_screen.phase_1_completed \
                    and curr_screen.rewards_gathered == curr_screen.rewards_to_win_ph_2:
                # Stop spawning enemies phase 2
                self.clock_spawn_enemies_variable.cancel()
                self.clock_spawn_enemies_variable = None
                curr_screen.phase_2_completed = True
                self.spawn_boss(screen_num)

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]


def kill_character(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.character_dict['killed'] = True
    self.sound_level_play.stop()
    self.sound_game_over.play()
    curr_screen.character_dict['is_moving'] = False
    if not curr_screen.phase_1_completed \
            or (curr_screen.number_of_phases == 3 and not curr_screen.phase_2_completed):
        # Stop enemy spawning
        self.clock_spawn_enemies_variable.cancel()
    # Stop enemies, and bosses
    for _, enemy in curr_screen.enemies_ids.items():
        enemy['speed'] = 0.
    for _, boss in curr_screen.bosses_ids.items():
        boss['speed'] = 0.
    kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 4)


# For debugging purposes:
def get_character_bbox(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    x1 = character_image.x
    y1 = character_image.y
    x2 = character_image.x
    y2 = character_image.top
    x3 = character_image.right
    y3 = character_image.top
    x4 = character_image.right
    y4 = character_image.y
    return [x1, y1, x2, y2, x3, y3, x4, y4]
