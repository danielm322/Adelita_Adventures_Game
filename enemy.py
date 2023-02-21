import random
import time
import kivy.uix.image
from kivy.clock import Clock
from functools import partial
from helper_fns import _get_enemy_start_end_positions

enemy_hit_points = 6


def spawn_enemy(self, screen_num, *args):
    # Updating an enemy will need the save of an endpoint, line parameters, and enemy speed
    curr_screen = self.root.screens[screen_num]
    if not curr_screen.character_dict['killed'] and not curr_screen.phase_1_completed:
        r_speed_x = random.uniform(curr_screen.enemy_speed_min,
                                   curr_screen.enemy_speed_max)
        spawn_pos, finish_pos = _get_enemy_start_end_positions(self.side_bar_width,
                                                               self.enemy_width,
                                                               self.enemy_height)
        # Straight line equation parameters
        divisor = (finish_pos['x'] - spawn_pos['x'])
        if divisor == 0:
            divisor = 1e-6
        line_slope = (finish_pos['y'] - spawn_pos['y']) / divisor
        line_intercept = spawn_pos['y'] - spawn_pos['x'] * line_slope

        enemy = kivy.uix.image.Image(source="graphics/entities/enemy.png",
                                     size_hint=(self.enemy_width, self.enemy_height),
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


def update_enemies(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        previous_x = enemy['image'].pos_hint['x']
        new_x = previous_x + enemy['speed_x'] * dt
        enemy['image'].pos_hint = {'x': new_x,
                                   'y': enemy['line_slope'] * new_x + enemy['line_intercept']}
        self.check_enemy_collision(enemy['image'], screen_num)
        if new_x <= enemy['finish_pos']['x']:
            enemies_to_delete.append(enemy_key)
            self.enemy_animation_completed(enemy['image'], screen_num)

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]


def check_enemy_collision(self, enemy, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * self.enemy_width / 3
    gap_y = curr_screen.height * self.enemy_height / 2
    if enemy.collide_widget(character_image) and \
            abs(enemy.center[0] - character_image.center[0]) <= gap_x and \
            abs(enemy.center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_dict['damage_received'] += 1
        if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
            curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']

        self.adjust_character_life_bar(screen_num)
        if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
            self.kill_character(screen_num)


def enemy_animation_completed(self, enemy, screen_num):
    curr_screen = enemy.parent.parent.parent
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy)
    curr_screen.character_dict['damage_received'] += curr_screen.enemy_finishes_damage
    if curr_screen.character_dict['damage_received'] >= curr_screen.character_dict['hit_points']:
        curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
        self.kill_character(screen_num)

    self.adjust_character_life_bar(screen_num)


