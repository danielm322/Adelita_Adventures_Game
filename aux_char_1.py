import time

import kivy.uix.image

from helper_fns import _find_kiss_endpoint_fast, get_direction_unit_vector


def auto_shoot(self, screen_num, *args):
    curr_screen = self.root.screens[screen_num]
    # screen_size = curr_screen.size  # List [size_x, size_y]
    aux_char_1_image = curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)]
    aux_char_1_image_center = aux_char_1_image.center  # List: [c_x, c_y]
    if len(curr_screen.enemies_ids) > 0:
        # enemy_to_shoot_center = curr_screen.enemies_ids[0]['image'].center
        # oldest_enemy = list(curr_screen.enemies_ids.values())[0]
        for enemy in curr_screen.enemies_ids.values():
            if enemy['type'] != 'fire' \
                    and (
                    abs(aux_char_1_image_center[0] - enemy['image'].center_x) < self.aux_char_1_range *
                    curr_screen.size[0]
                    and abs(aux_char_1_image_center[1] - enemy['image'].center_y) < self.aux_char_1_range *
                    curr_screen.size[1]
            ):
                enemy_to_shoot_center = enemy['image'].center
                start_pos = [aux_char_1_image_center[0] - self.kiss_width * curr_screen.size[0] / 2,
                             aux_char_1_image_center[1]]

                finish_pos = _find_kiss_endpoint_fast(start_pos,
                                                      enemy_to_shoot_center,
                                                      curr_screen.size,
                                                      self.kiss_width,
                                                      self.kiss_height,
                                                      self.side_bar_width)
                direction_unit_vector = get_direction_unit_vector(start_pos, finish_pos)
                banana = kivy.uix.image.Image(source="graphics/entities/banana_small.png",
                                              size_hint=(self.kiss_width, self.kiss_height),
                                              pos=start_pos,
                                              allow_stretch=True,
                                              keep_ratio=False)
                curr_screen.add_widget(banana, index=-1)
                # create a unique identifier for each enemy
                time_stamp = str(time.time())
                curr_screen.kisses_ids['banana_' + time_stamp] = {'image': banana,
                                                                  'finish_pos': finish_pos,
                                                                  'direction_u_vector': direction_unit_vector}
                # self.sound_kiss.play()
                break
