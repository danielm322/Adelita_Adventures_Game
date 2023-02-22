import random
import time

import kivy.uix.image
from kivy.clock import Clock

from helper_fns import calc_parabola_vertex


def shoot_special(self, screen_num, touch_point):
    extra_height = 0.35  # Extra height of parabola
    curr_screen = self.root.screens[screen_num]
    screen_size = curr_screen.size  # List [size_x, size_y]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    start_point = (character_image_center[0],
                   character_image_center[1] + screen_size[1] * self.special_attack_init_height / 2)
    end_point = (touch_point[0] - screen_size[0] * self.special_attack_init_width / 2,
                 touch_point[1] - screen_size[1] * self.special_attack_init_height / 2)
    # Special has a parabolic trajectory, so we need to calculate a third point to uniquely define a parabola
    if start_point[1] > end_point[1]:
        height_mid_point = start_point[1] + extra_height * screen_size[1]
    else:
        height_mid_point = end_point[1] + extra_height * screen_size[1]
    mid_point = ((end_point[0] + start_point[0]) / 2.,
                 height_mid_point)
    parabola_params = calc_parabola_vertex(start_point, mid_point, end_point)
    # We need to know the direction of the parabola
    if start_point[0] < end_point[0]:
        direction = 'right'
    else:
        direction = 'left'

    special_attack = kivy.uix.image.Image(source="graphics/entities/diaper.png",
                                          size_hint=(self.special_attack_init_width, self.special_attack_init_height),
                                          pos=[character_image_center[0] -
                                               self.special_attack_init_width * screen_size[0] / 2,
                                               character_image_center[1]],
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
    # self.sound_kiss.play()

    curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
    self.special_button_enabled = False
    Clock.schedule_once(self.enable_special_attack, self.special_attack_reload_time)

def update_specials(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    specials_to_delete = []
    for special_key, special in curr_screen.specials_ids.items():
        if special['direction'] == 'right':
            speed_x = self.special_attack_speed_x
        else:
            speed_x = -self.special_attack_speed_x
        new_x = special['image'].x + speed_x * dt
        special['image'].x = new_x
        special['image'].y = special['a'] * new_x ** 2 + special['b'] * new_x + special['c']
        # special['image'].size_hint = [special['image'].size_hint[0] + dt / self.special_grow_size_factor,
        #                          special['image'].size_hint[1] + dt / self.special_grow_size_factor]
        # Stop special movement
        if special['direction'] == 'right' and new_x > special['finish_pos'][0]:
            specials_to_delete.append(special_key)
            self.check_special_collision(special, screen_num)
        elif special['direction'] == 'left' and new_x < special['finish_pos'][0]:
            specials_to_delete.append(special_key)
            self.check_special_collision(special, screen_num)

    if len(specials_to_delete) > 0:
        for special_key in specials_to_delete:
            del curr_screen.specials_ids[special_key]


def check_special_collision(self, special, screen_num):
    curr_screen = self.root.screens[screen_num]
    # gap_x = curr_screen.width * self.enemy_width / 3
    # gap_y = curr_screen.height * self.enemy_height / 3
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        if abs(special['image'].center[0] - enemy['image'].center[0]) <= self.special_attack_radius * curr_screen.size[0] and \
           abs(special['image'].center[1] - enemy['image'].center[1]) <= self.special_attack_radius * curr_screen.size[1]:
            enemy['hitpoints'] = enemy['hitpoints'] - self.special_attack_damage
            if enemy['hitpoints'] <= 0:
                enemy_center = enemy['image'].center
                enemies_to_delete.append(enemy_key)
                curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy['image'])
                # Spawn reward with probability defined per level
                if random.random() < curr_screen.enemy_spawn_reward_probability:
                    self.spawn_reward(enemy_center, screen_num)

    bosses_to_delete = []
    for boss_key, boss in curr_screen.bosses_ids.items():
        if abs(special['image'].center[0] - boss['image'].center[0]) <= self.special_attack_radius * curr_screen.size[0] and \
           abs(special['image'].center[1] - boss['image'].center[1]) <= self.special_attack_radius * curr_screen.size[1]:
            boss['hit_points'] = boss['hit_points'] - self.special_attack_damage
            if boss['hit_points'] <= 0:
                self.kill_boss(boss, screen_num)
                bosses_to_delete.append(boss_key)

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
