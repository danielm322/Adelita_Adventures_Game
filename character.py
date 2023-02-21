import kivy.animation
from functools import partial
from kivy.clock import Clock
from math import sqrt, fabs


def start_character_animation(self, screen_num, touch_pos):
    curr_screen = self.root.screens[screen_num]
    screen_size = curr_screen.size  # List [size_x, size_y]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    # character_image.im_num = character_image.start_im_num
    character_image_center = character_image.center  # List: [c_x, c_y]
    # finish_pos = (touch_pos[0] - character_image.size[0] / 2,
    #               touch_pos[1] - character_image.size[1] / 2)
    finish_pos = (touch_pos[0],
                  touch_pos[1])
    unit_vector_norm = sqrt(
        (finish_pos[0] - character_image_center[0]) ** 2 + (finish_pos[1] - character_image_center[1]) ** 2
    )
    direction_unit_vector = ((finish_pos[0] - character_image_center[0]) / unit_vector_norm,
                             (finish_pos[1] - character_image_center[1]) / unit_vector_norm)
    # char_anim = kivy.animation.Animation(
    #     # pos_hint={'x': (touch_pos[0] - character_image.size_hint[0] / 2),
    #     #           'y': touch_pos[1] - character_image.size_hint[1] / 2},
    #     pos=(touch_pos[0] - character_image.size[0] / 2,
    #          touch_pos[1] - character_image.size[1] / 2),
    #     duration=curr_screen.char_anim_duration
    # )
    # char_anim.bind(on_progress=partial(self.check_character_collision, character_image, screen_num))
    # char_anim.start(character_image)
    curr_screen.character_dict['is_moving'] = True
    curr_screen.character_dict['finish_point_pos'] = finish_pos
    curr_screen.character_dict['direction_unit_vector'] = direction_unit_vector


def update_character(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    if curr_screen.character_dict['is_moving']:
        character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
        new_x = character_image.x + curr_screen.character_dict['direction_unit_vector'][0] * curr_screen.character_dict['speed'] * dt
        new_y = character_image.y + curr_screen.character_dict['direction_unit_vector'][1] * curr_screen.character_dict['speed'] * dt
        character_image.x = new_x
        character_image.y = new_y
        self.check_character_collision(character_image, screen_num)
        if fabs(
            character_image.center_x - curr_screen.character_dict['finish_point_pos'][0]
            ) < self.MOVEMENT_PIXEL_TOLERANCE and \
           fabs(
            character_image.center_y - curr_screen.character_dict['finish_point_pos'][1]
            ) < self.MOVEMENT_PIXEL_TOLERANCE:
            curr_screen.character_dict['is_moving'] = False


def check_character_collision(self, character_image, screen_num):
    curr_screen = self.root.screens[screen_num]
    gap_x = curr_screen.width * self.reward_size / 1
    gap_y = curr_screen.height * self.reward_size / 1
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        if character_image.collide_widget(reward['image']) and \
                abs(character_image.center[0] - reward['image'].center[0]) <= gap_x and \
                abs(character_image.center[1] - reward['image'].center[1]) <= gap_y:
            rewards_to_delete.append(reward_key)
            # kivy.animation.Animation.cancel_all(reward)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward['image'])
            curr_screen.rewards_gathered += 1
            self.sound_reward_collected.play()
            if curr_screen.rewards_gathered == curr_screen.rewards_to_win_ph_1:
                # Stop spawning enemies
                Clock.unschedule(partial(self.spawn_enemy, screen_num))
                self.clock_spawn_enemies_variable.cancel()
                curr_screen.phase_1_completed = True
                self.spawn_boss(screen_num)
            if curr_screen.rewards_gathered > curr_screen.rewards_to_win_ph_1:
                curr_screen.rewards_gathered = curr_screen.rewards_to_win_ph_1
            curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
                curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_1)

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]


def kill_character(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.character_dict['killed'] = True
    self.sound_level_play.stop()
    self.sound_game_over.play()
    curr_screen.character_dict['is_moving'] = False
    if not curr_screen.phase_1_completed:
        # Stop enemy spawning
        Clock.unschedule(partial(self.spawn_enemy, screen_num))
        self.clock_spawn_enemies_variable.cancel()
    # kivy.animation.Animation.cancel_all(character_image)
    # Stop enemies, and bosses
    for _, enemy in curr_screen.enemies_ids.items():
        enemy['speed_x'] = 0.
    for _, boss in curr_screen.bosses_ids.items():
        boss['speed_x'] = 0.
    kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 3)
