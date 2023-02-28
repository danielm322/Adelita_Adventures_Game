import random
import time

import kivy.uix.image
from kivy.clock import Clock
from kivy.utils import platform

from enemies_dict import enemies_dict
from helper_fns import calc_parabola_vertex, write_level_passed


def shoot_special(self, screen_num, touch_point):
    curr_screen = self.root.screens[screen_num]
    screen_size = curr_screen.size  # List [size_x, size_y]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    # Check minimum radius for shooting special
    if check_minimum_radius_to_shoot_special(screen_size, character_image_center, self.special_min_dist_x, touch_point):
        char_height = curr_screen.ids['character_image_lvl' + str(screen_num)].height
        char_width = curr_screen.ids['character_image_lvl' + str(screen_num)].width
        start_point = (character_image_center[0] + char_width / 5,
                       character_image_center[1] + char_height / 2)
        # end_point = (touch_point[0] - screen_size[0] * self.special_attack_init_width / 2,
        #              touch_point[1] - screen_size[1] * self.special_attack_init_height / 2)
        end_point = (touch_point[0],
                     touch_point[1])
        # Special has a parabolic trajectory, so we need to calculate a third point to uniquely define a parabola
        if start_point[1] > end_point[1]:
            height_mid_point = start_point[1] + self.special_extra_height * screen_size[1]
        else:
            height_mid_point = end_point[1] + self.special_extra_height * screen_size[1]
        mid_point = ((end_point[0] + start_point[0]) / 2.,
                     height_mid_point)
        parabola_params = calc_parabola_vertex(start_point, mid_point, end_point)
        # We need to know the direction of the parabola
        if start_point[0] < end_point[0]:
            direction = 1  # Right
        else:
            direction = -1  # Left

        special_attack = kivy.uix.image.Image(source="graphics/entities/diaper.png",
                                              size_hint=(
                                                self.special_attack_init_width, self.special_attack_init_height
                                              ),
                                              center_x=start_point[0],
                                              center_y=start_point[1],
                                              allow_stretch=True)
        curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(special_attack, index=2)
        # create a unique identifier for each enemy
        time_stamp = str(time.time())
        curr_screen.specials_ids['special_' + time_stamp] = {'image': special_attack,
                                                             'finish_pos': end_point,
                                                             'a': parabola_params[0],
                                                             'b': parabola_params[1],
                                                             'c': parabola_params[2],
                                                             'direction': direction}

        curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
        self.special_button_enabled = False
        curr_screen.canvas.remove_group(u"special_radius")
        self.sound_baby_laughs.play()
        Clock.schedule_once(self.enable_special_attack, self.special_attack_reload_time)


def update_specials(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    specials_to_delete = []
    for special_key, special in curr_screen.specials_ids.items():
        new_center_x = special['image'].center_x + self.special_attack_speed_x * special['direction'] * dt
        special['image'].center_x = new_center_x
        special['image'].center_y = special['a'] * new_center_x ** 2 + special['b'] * new_center_x + special['c']
        # Make special image grow
        special['image'].size_hint = [special['image'].size_hint[0] + dt / self.special_grow_size_factor,
                                      special['image'].size_hint[1] + dt / self.special_grow_size_factor]
        # Stop special movement
        if special['direction'] == 1 and new_center_x > special['finish_pos'][0]:
            specials_to_delete.append(special_key)
            self.check_special_collision(special, screen_num)
        elif special['direction'] == -1 and new_center_x < special['finish_pos'][0]:
            specials_to_delete.append(special_key)
            self.check_special_collision(special, screen_num)

    if len(specials_to_delete) > 0:
        for special_key in specials_to_delete:
            del curr_screen.specials_ids[special_key]


def check_special_collision(self, special, screen_num):
    curr_screen = self.root.screens[screen_num]
    enemies_to_delete = []
    enemies_to_spawn_fire = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        if abs(special['image'].center[0] - enemy['image'].center[0]) <= self.special_attack_radius * curr_screen.size[
            0] and \
                abs(special['image'].center[1] - enemy['image'].center[1]) <= self.special_attack_radius * \
                curr_screen.size[1]:
            enemy['hit_points'] = enemy['hit_points'] - self.special_attack_damage
            if enemy['fires_back']:
                enemies_to_spawn_fire.append(enemy['image'].center)

            if enemy['hit_points'] <= 0:
                self.sound_enemy_dies.play()
                enemy_center = enemy['image'].center
                enemies_to_delete.append(enemy_key)
                curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy['image'])
                # Spawn reward with probability defined per level
                if random.random() < enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_reward_probability']:
                    self.spawn_reward(enemy_center, screen_num)

    bosses_to_delete = []
    for boss_key, boss in curr_screen.bosses_ids.items():
        if abs(special['image'].center[0] - boss['image'].center[0]) <= self.special_attack_radius * curr_screen.size[
            0] and \
                abs(special['image'].center[1] - boss['image'].center[1]) <= self.special_attack_radius * \
                curr_screen.size[1]:
            boss['hit_points'] = boss['hit_points'] - self.special_attack_damage
            if boss['hit_points'] <= 0:
                self.kill_boss(boss, screen_num)
                bosses_to_delete.append(boss_key)
                write_level_passed(platform, screen_num)

    if len(enemies_to_spawn_fire) > 0:
        for enemy_center in enemies_to_spawn_fire:
            self.spawn_rocket_at_enemy_center_to_ch_center(screen_num,
                                                           enemy_center,
                                                           'fire',
                                                           'level_1')

    # Remove special widget
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(special['image'])
    if len(bosses_to_delete) > 0:
        for boss_key in bosses_to_delete:
            del curr_screen.bosses_ids[boss_key]

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]


def enable_special_attack(self, dt):
    self.special_button_enabled = True


def get_special_quad_coords(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center
    x1 = character_image_center[0] - self.special_min_dist_x * curr_screen.size[0]
    y1 = 0
    x2 = character_image_center[0] - self.special_min_dist_x * curr_screen.size[0]
    y2 = curr_screen.size[1]
    x3 = character_image_center[0] + self.special_min_dist_x * curr_screen.size[0]
    y3 = curr_screen.size[1]
    x4 = character_image_center[0] + self.special_min_dist_x * curr_screen.size[0]
    y4 = 0
    return [x1, y1, x2, y2, x3, y3, x4, y4]


def check_minimum_radius_to_shoot_special(screen_size, character_image_center, special_min_dist_x, touch_point):
    if touch_point[0] > character_image_center[0] + special_min_dist_x * screen_size[0]:
        return True
    if touch_point[0] < character_image_center[0] - special_min_dist_x * screen_size[0]:
        return True
    else:
        return False
