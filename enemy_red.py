import random
import time
import kivy.uix.image
from helper_fns import _get_red_enemy_start_end_positions

red_enemy_hit_points = 10


def spawn_enemy_red(self, screen_num, *args):
    # Updating an enemy will need the save of an endpoint, line parameters, and enemy speed
    curr_screen = self.root.screens[screen_num]
    if not curr_screen.character_dict['killed'] and not curr_screen.phase_1_completed:
        r_speed_x = random.uniform(curr_screen.red_enemy_speed_min,
                                   curr_screen.red_enemy_speed_max)
        spawn_pos, finish_pos = _get_red_enemy_start_end_positions(self.side_bar_width,
                                                                   curr_screen.red_enemy_spawn_point,
                                                                   curr_screen.red_enemy_end_point,
                                                                   curr_screen.red_enemy_trajectory_variance,
                                                                   self.red_enemy_width,
                                                                   self.red_enemy_height)
        # Straight line equation parameters
        divisor = (finish_pos['x'] - spawn_pos['x'])
        if divisor == 0:
            divisor = 1e-6
        line_slope = (finish_pos['y'] - spawn_pos['y']) / divisor
        line_intercept = spawn_pos['y'] - spawn_pos['x'] * line_slope

        enemy = kivy.uix.image.Image(source="graphics/entities/enemy_red.png",
                                     size_hint=(self.red_enemy_width, self.red_enemy_height),
                                     pos_hint=spawn_pos, allow_stretch=True)
        curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
        # create a unique identifier for each enemy
        time_stamp = str(time.time())

        curr_screen.enemies_ids['enemy_red_' + time_stamp] = {'image': enemy,
                                                              'finish_pos': finish_pos,
                                                              'hitpoints': red_enemy_hit_points,
                                                              'line_slope': line_slope,
                                                              'line_intercept': line_intercept,
                                                              'speed_x': - r_speed_x}  # Speed should be negative


