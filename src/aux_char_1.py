import time

import kivy.uix.image

from src.helper_fns import _find_kiss_endpoint_fast, get_direction_unit_vector
from src.characters_dicts import aux_char_1_dict


def auto_shoot(self, screen_num, *args):
    """
    This function is automatically called with a frequency defined in the main with the parameter
    AUX_CHAR_1_FIRE_INTERVAL
    :param screen_num: Screen number
    :param args: Automatically called by the Kivy Clock scheduler. Do not remove.
    :return: None
    """
    curr_screen = self.root.screens[screen_num]
    # screen_size = curr_screen.size  # List [size_x, size_y]
    aux_char_1_image = curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)]
    aux_char_1_image_center = aux_char_1_image.center  # List: [c_x, c_y]
    # Define a flag to know if the rocket has been fired
    is_fired_flag = False
    if len(curr_screen.enemies_ids) > 0:
        for enemy in curr_screen.enemies_ids.values():
            if enemy['type'] != 'fire' \
                    and (
                    abs(aux_char_1_image_center[0] - enemy['image'].center_x) < self.AUX_CHAR_1_RANGE *
                    curr_screen.size[0]
                    and abs(aux_char_1_image_center[1] - enemy['image'].center_y) < self.AUX_CHAR_1_RANGE *
                    curr_screen.size[1]
            ):
                enemy_to_shoot_center = enemy['image'].center
                start_pos = [aux_char_1_image_center[0] - self.KISS_WIDTH * curr_screen.size[0] / 2,
                             aux_char_1_image_center[1]]

                finish_pos = _find_kiss_endpoint_fast(start_pos,
                                                      enemy_to_shoot_center,
                                                      curr_screen.size,
                                                      aux_char_1_dict['rocket_width'],
                                                      aux_char_1_dict['rocket_height'],
                                                      self.SIDE_BAR_WIDTH)
                direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
                rocket = kivy.uix.image.Image(source=aux_char_1_dict['rocket_image_source'],
                                              size_hint=(aux_char_1_dict['rocket_width'],
                                                         aux_char_1_dict['rocket_height']),
                                              pos=start_pos,
                                              allow_stretch=True,
                                              keep_ratio=False)
                curr_screen.add_widget(rocket, index=-1)
                # create a unique identifier for each enemy
                time_stamp = str(time.time())
                curr_screen.kisses_ids['aux_char_1_rkt_' + time_stamp] = {'image': rocket,
                                                                          'finish_pos': finish_pos,
                                                                          'direction_u_vector': direction_unit_vector}
                # self.sound_kiss.play()
                is_fired_flag = True
                # Change aux char 1 state
                curr_screen.characters_dict['aux_char_1']['current_state'] = 'throwing'
                break

    # Shoot to bosses if no enemy around
    if not is_fired_flag:
        if len(curr_screen.bosses_ids) > 0:
            for boss in curr_screen.bosses_ids.values():
                if abs(aux_char_1_image_center[0] - boss['image'].center_x) < \
                        self.AUX_CHAR_1_RANGE * curr_screen.size[0] \
                        and abs(aux_char_1_image_center[1] - boss['image'].center_y) < \
                        self.AUX_CHAR_1_RANGE * curr_screen.size[1]:
                    boss_to_shoot_center = boss['image'].center
                    start_pos = [aux_char_1_image_center[0] - self.KISS_WIDTH * curr_screen.size[0] / 2,
                                 aux_char_1_image_center[1]]

                    finish_pos = _find_kiss_endpoint_fast(start_pos,
                                                          boss_to_shoot_center,
                                                          curr_screen.size,
                                                          aux_char_1_dict['rocket_width'],
                                                          aux_char_1_dict['rocket_height'],
                                                          self.SIDE_BAR_WIDTH)
                    direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
                    rocket = kivy.uix.image.Image(source=aux_char_1_dict['rocket_image_source'],
                                                  size_hint=(aux_char_1_dict['rocket_width'],
                                                             aux_char_1_dict['rocket_height']),
                                                  pos=start_pos,
                                                  allow_stretch=True,
                                                  keep_ratio=False)
                    curr_screen.add_widget(rocket, index=-1)
                    # create a unique identifier for each enemy
                    time_stamp = str(time.time())
                    curr_screen.kisses_ids['aux_char_1_rkt_' + time_stamp] = {'image': rocket,
                                                                              'finish_pos': finish_pos,
                                                                              'direction_u_vector': direction_unit_vector}
                    # self.sound_kiss.play()
                    # Change aux char 1 state
                    curr_screen.characters_dict['aux_char_1']['current_state'] = 'throwing'
                    break
