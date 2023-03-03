import random
from math import sqrt

# from kivy.graphics import Line
# from kivy.graphics import Line
from kivy.utils import platform
from helper_fns import _find_kiss_endpoint_fast, write_level_passed, get_direction_unit_vector
import kivy.uix.image
import time
from enemies_dict import enemies_dict


def shoot_kiss(self, screen_num, touch_point):
    curr_screen = self.root.screens[screen_num]
    screen_size = curr_screen.size  # List [size_x, size_y]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    start_pos = [character_image_center[0] - self.kiss_width * screen_size[0] / 2,
                 character_image_center[1]]
    finish_pos = _find_kiss_endpoint_fast(start_pos,
                                          touch_point,
                                          screen_size,
                                          self.kiss_width,
                                          self.kiss_height,
                                          self.side_bar_width)
    # with curr_screen.canvas:
    #     Line(circle=(character_image_center[0], character_image_center[1], 20))
    kiss_direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
    kiss = kivy.uix.image.Image(source="graphics/entities/kiss1.png",
                                size_hint=(self.kiss_width, self.kiss_height),
                                pos=start_pos,
                                # center_x=character_image_center[0] + self.kiss_width * screen_size[0] / 2,
                                # center_y=character_image_center[1],
                                allow_stretch=True,
                                keep_ratio=False)
    # curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(kiss, index=2)
    curr_screen.add_widget(kiss, index=-1)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.kisses_ids['kiss_' + time_stamp] = {'image': kiss,
                                                    'finish_pos': finish_pos,
                                                    'direction_u_vector': kiss_direction_unit_vector}
    self.sound_kiss.play()


def update_kisses(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    kisses_to_delete = []
    enemies_to_delete = []
    bosses_to_delete = []
    for kiss_key, kiss in curr_screen.kisses_ids.items():
        # new_x/ = kiss['image'].x + kiss['direction_u_vector'][0] * self.kiss_speed * dt
        # new_y = kiss['image'].y + kiss['direction_u_vector'][1] * self.kiss_speed * dt
        # kiss['image'].x = new_x
        # kiss['image'].y = new_y
        new_x = kiss['image'].center_x + kiss['direction_u_vector'][0] * self.kiss_speed * dt
        new_y = kiss['image'].center_y + kiss['direction_u_vector'][1] * self.kiss_speed * dt
        kiss['image'].center_x = new_x
        kiss['image'].center_y = new_y
        # with curr_screen.canvas:
        #     Line(circle=(kiss['image'].center_x, kiss['image'].center_y, 20))
        kiss_used, enemies_to_eliminate = self.check_kiss_collision_with_enemies(kiss['image'], screen_num)
        if kiss_used:
            kisses_to_delete.append(kiss_key)
            if enemies_to_eliminate:
                enemies_to_delete.extend(enemies_to_eliminate)
        elif curr_screen.phase_1_completed:
            kiss_used, boss_to_eliminate = self.check_kiss_collision_with_bosses(kiss['image'], screen_num)
            if kiss_used:
                kisses_to_delete.append(kiss_key)
                if boss_to_eliminate:
                    bosses_to_delete.extend(boss_to_eliminate)
        elif kiss['image'].center_x > curr_screen.width \
                or (kiss['direction_u_vector'][0] < 0 and kiss['image'].center_x < kiss['finish_pos'][0]) \
                or kiss['image'].y > curr_screen.height \
                or kiss['image'].y < 0 - self.kiss_width * curr_screen.height:
            kisses_to_delete.append(kiss_key)
            # curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss['image'])
            curr_screen.remove_widget(kiss['image'])

    if len(kisses_to_delete) > 0:
        for kiss_key in kisses_to_delete:
            del curr_screen.kisses_ids[kiss_key]

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]

    if len(bosses_to_delete) > 0:
        for boss_key in bosses_to_delete:
            del curr_screen.bosses_ids[boss_key]


def check_kiss_collision_with_enemies(self, kiss, screen_num):
    kiss_already_hit = False
    curr_screen = self.root.screens[screen_num]
    if not curr_screen.phase_1_completed or curr_screen.number_of_phases == 2:
        gap_x = curr_screen.width * \
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['width'] / 3
        gap_y = curr_screen.height * \
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['height'] / 3
    elif curr_screen.phase_1_completed and curr_screen.number_of_phases == 3:
        gap_x = curr_screen.width * \
                enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']]['width'] / 3
        gap_y = curr_screen.height * \
                enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']]['height'] / 3

    enemies_to_delete = []
    enemies_to_spawn_fire = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        # if not kiss_already_hit and check_collision_rect(kiss, enemy['image']) and not enemy['type'] == 'fire':
        if not kiss_already_hit \
                and not enemy['type'] == 'fire' \
                and kiss.collide_widget(enemy['image']) \
                and abs(enemy['image'].center[0] - kiss.center[0]) <= gap_x \
                and abs(enemy['image'].center[1] - kiss.center[1]) <= gap_y:
            enemy['hit_points'] = enemy['hit_points'] - 1
            # curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss)
            curr_screen.remove_widget(kiss)
            kiss_already_hit = True
            if enemy['fires_back']:
                enemies_to_spawn_fire.append(enemy['image'].center)

            if enemy['hit_points'] == 0:
                self.sound_enemy_dies.play()
                enemy_center = enemy['image'].center
                enemies_to_delete.append(enemy_key)
                curr_screen.remove_widget(enemy['image'])
                # Spawn reward with probability defined per level
                if random.random() < \
                        enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']][
                            'spawn_reward_probability']:
                    self.spawn_reward(enemy_center, screen_num)

    if len(enemies_to_spawn_fire) > 0:
        for enemy_center in enemies_to_spawn_fire:
            self.spawn_rocket_at_enemy_center_to_ch_center(screen_num,
                                                           enemy_center,
                                                           'fire',
                                                           'level_1')

    return kiss_already_hit, enemies_to_delete


def check_kiss_collision_with_bosses(self, kiss, screen_num, *args):
    kiss_already_hit = False
    curr_screen = self.root.screens[screen_num]
    # Boss collision check
    gap_x = curr_screen.width * curr_screen.boss_props['width'] / 5
    gap_y = curr_screen.height * curr_screen.boss_props['height'] / 3
    bosses_to_delete = []
    for boss_key, boss in curr_screen.bosses_ids.items():
        if kiss.collide_widget(boss['image']) and \
                abs(boss['image'].center[0] - kiss.center[0]) <= gap_x and \
                abs(boss['image'].center[1] - kiss.center[1]) <= gap_y:
            kiss_already_hit = True
            boss['hit_points'] = boss['hit_points'] - 1
            curr_screen.remove_widget(kiss)
            if boss['hit_points'] <= 0:
                self.kill_boss(boss, screen_num)
                bosses_to_delete.append(boss_key)
                # Write level pass to file
                write_level_passed(platform, screen_num)

    return kiss_already_hit, bosses_to_delete
