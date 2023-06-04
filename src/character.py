import random
import kivy.animation
from functools import partial
from kivy.clock import Clock
# from kivy.graphics import Line
# from math import sqrt
from src.enemies_dict import enemies_dict
from src.helper_fns import get_direction_unit_vector, get_triangle_borders_coords
from src.characters_dicts import character_states_to_images
from src.reward import rewards_properties


def start_character_animation_from_dict(self, screen_num, touch_pos, character_dict):
    """
    Starts moving a character after a touch event. Updates the values of each character inside the characters_dict of
    each level
    :param self:
    :param screen_num:
    :param touch_pos:
    :param character_dict: A child dictionary from the characters_dict from each level
    :return:
    """
    curr_screen = self.root.screens[screen_num]
    # screen_size = curr_screen.size  # List [size_x, size_y]
    character_image = curr_screen.ids[character_dict['name'] + str(screen_num)]
    # character_image.im_num = character_image.start_im_num
    character_image_center = character_image.center  # List: [c_x, c_y]
    finish_pos = (touch_pos[0], touch_pos[1])
    direction_unit_vector = get_direction_unit_vector(character_image_center, touch_pos)
    character_dict['is_moving'] = True
    character_dict['finish_point_pos'] = finish_pos
    character_dict['direction_unit_vector'] = direction_unit_vector
    character_dict['current_state'] = 'walking'


def update_characters_from_dict(self, screen_num, dt):
    """
    Updates all characters defined in the characters_dict dictionary that is a property of each level
    :param self:
    :param screen_num:
    :param dt:
    :return:
    """
    curr_screen = self.root.screens[screen_num]
    for character in curr_screen.characters_dict.values():
        if not character['is_killed']:
            if character['is_moving']:
                character_image = curr_screen.ids[character['name'] + str(screen_num)]
                new_x = character_image.center_x + \
                        character['direction_unit_vector'][0] * character['speed'] * dt
                new_y = character_image.center_y + \
                        character['direction_unit_vector'][1] * character['speed'] * dt
                character_image.center_x = new_x
                character_image.center_y = new_y
                # self.char_bounding_box.points = self.get_character_bbox(screen_num)
                # with curr_screen.canvas:
                #     Line(circle=(character_image.center_x, character_image.center_y, 10))
                # Update remaining life bar widget
                remaining_life_percent_lvl_widget = curr_screen.ids[character['life_bar_id'] + str(screen_num)]
                remaining_life_percent_lvl_widget.x = character_image.x
                remaining_life_percent_lvl_widget.y = character_image.top
                # Update special attack radius quad
                if character['shoot_special_state']:
                    self.special_attack_properties['quad'].points = self.get_special_quad_coords(screen_num)
                if curr_screen.move_aux_char_1_state:
                    self.aux_char_1_quad.points = self.get_aux_char_1_quad_coords(screen_num)
                # Check collision with rewards
                self.check_character_collision(character, screen_num)
                # Stop moving character if he arrived to the final point
                if abs(
                        character_image.center_x - character['finish_point_pos'][0]
                ) < self.MOVEMENT_PIXEL_TOLERANCE \
                        and abs(
                    character_image.center_y - character['finish_point_pos'][1]
                ) < self.MOVEMENT_PIXEL_TOLERANCE:
                    character['is_moving'] = False
                    character['current_state'] = 'idle'

        # Update character image regardless of character state
        self.update_character_image_animation(screen_num, character, dt)

    # Update special triangle
    if screen_num >= self.LEVEL_WHEN_SPECIAL_TRIANGLE_IS_ACTIVATED and curr_screen.special_triangle_state:
        self.special_triangle_shape.points = self.get_special_triangle_coords(screen_num)
        self.special_triangle_border.points = get_triangle_borders_coords(self.special_triangle_shape.points)


def check_character_collision(self, character, screen_num):
    """
    This function checks collision with rewards only. Updates the rewards counter and activates other game phases when
    the required rewards for each phase are collected
    :param self:
    :param character: Character dictionary
    :param screen_num:
    :return:
    """
    curr_screen = self.root.screens[screen_num]
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        gap_x = curr_screen.width * rewards_properties[reward['type']]['width'] / 3
        gap_y = curr_screen.height * rewards_properties[reward['type']]['height'] / 1.5
        character_image = curr_screen.ids[character['name'] + str(screen_num)]
        if character_image.collide_widget(reward['image']) and \
                abs(character_image.center[0] - reward['image'].center[0]) <= gap_x and \
                abs(character_image.center[1] - reward['image'].center[1]) <= gap_y:
            rewards_to_delete.append(reward_key)
            curr_screen.remove_widget(reward['image'])
            if reward['type'] == 'star':
                curr_screen.rewards_gathered += 1
                self.sound_reward_collected.play()
            elif reward['type'] == 'heart':
                self.sound_heal.play()
                character['damage_received'] -= character['hit_points'] * rewards_properties['heart']['heal_proportion']
                if character['damage_received'] < 0.0:
                    character['damage_received'] = 0.0
                self.adjust_character_life_bar(screen_num, character)
            # Update stars counter
            if curr_screen.current_phase < curr_screen.number_of_phases:
                curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = \
                    str(curr_screen.rewards_gathered) + "/" \
                    + str(curr_screen.rewards_to_win_phases[curr_screen.current_phase - 1])
            elif curr_screen.current_phase == curr_screen.number_of_phases:
                curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = \
                    str(curr_screen.rewards_gathered) + "/" \
                    + str(curr_screen.rewards_to_win_phases[curr_screen.current_phase - 2])

            # Pass to next phase
            if curr_screen.current_phase < curr_screen.number_of_phases and \
                    curr_screen.rewards_gathered == curr_screen.rewards_to_win_phases[curr_screen.current_phase - 1]:
                self.advance_to_next_phase(curr_screen, screen_num)

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]


def begin_kill_character(self, screen_num, character_dict):
    curr_screen = self.root.screens[screen_num]
    character_dict['is_killed'] = True
    character_dict['current_state'] = 'dead'
    # Here I handle the main character death
    if character_dict['name'] == 'character_image_lvl':
        self.sound_level_play.stop()
        self.sound_game_over.play()
        character_dict['is_moving'] = False
        # Cancel enemy spawning
        # This for loop is written like this to be able to convert to None the clock variables
        for i in range(len(curr_screen.spawn_enemies_clock_variables)):
            curr_screen.spawn_enemies_clock_variables[i].cancel()
            curr_screen.spawn_enemies_clock_variables[i] = None
        curr_screen.spawn_enemies_clock_variables.clear()
        # Check all clock variables have been canceled and eliminated
        assert len(curr_screen.spawn_enemies_clock_variables) == 0
        # Stop enemies, and bosses
        for _, enemy in curr_screen.enemies_ids.items():
            enemy['speed'] = 0.
        for _, boss in curr_screen.bosses_ids.items():
            boss['speed'] = 0.
        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS:
            self.clock_banana_throw_variable.cancel()

    if character_dict['name'] == 'aux_char_1_image_lvl':
        self.clock_banana_throw_variable.cancel()
        curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state = "normal"
        self.move_aux_char_1_button_enabled = False

    if character_dict['name'] == 'aux_char_2_image_lvl':
        curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state = "normal"
        self.move_aux_char_2_button_enabled = False

    # Control the possibility of using the special triangle when at least one character is dead
    if screen_num >= self.LEVEL_WHEN_SPECIAL_TRIANGLE_IS_ACTIVATED:
        if not curr_screen.special_triangle_state:
            curr_screen.ids['special_triangle_button_lvl' + str(screen_num)].disabled = True
        else:
            self.finish_special_triangle(screen_num)


def finish_kill_character(self, screen_num, character_dict):
    curr_screen = self.root.screens[screen_num]
    if character_dict['name'] == 'character_image_lvl':
        kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 4)
    elif character_dict['name'] == 'aux_char_1_image_lvl':
        character_image = curr_screen.ids[character_dict['name'] + str(screen_num)]
        character_image.opacity = 0
        # Move character out of screen to avoid collision with enemies
        character_image.center_x = -0.5 * curr_screen.size[0]
        character_image.center_y = -0.5 * curr_screen.size[1]
    elif character_dict['name'] == 'aux_char_2_image_lvl':
        character_image = curr_screen.ids[character_dict['name'] + str(screen_num)]
        character_image.opacity = 0
        # self.move_aux_char_2_button_enabled = False
        character_image.center_x = -0.5 * curr_screen.size[0]
        character_image.center_y = -0.5 * curr_screen.size[1]


def update_character_image_animation(self, screen_num: int, character_dict: dict, dt: float) -> None:
    """
    This function animates the characters independently of their state. The control of availability of
    an animation for a given state for a given character is done before calling this function.
    The function assumes that the passed character in its current state has a well-defined animation sequence.
    The function updates an individual counter by a float quantity. Once the integer of the counter changes,
     the image is updated
    :param screen_num: Screen number
    :param character_dict: The character dictionary as defined per level
    :param dt: Time difference as passed to the update character function
    :return: None
    """
    update_rate = dt * character_dict[character_states_to_images[character_dict['current_state']]['animation_speed']]
    curr_screen = self.root.screens[screen_num]
    current_image_counter = character_states_to_images[character_dict['current_state']]['counter']
    previous_im_number = character_dict[current_image_counter]
    character_dict[current_image_counter] += update_rate
    # Control the maximum number of images
    if character_dict[current_image_counter] >= \
            character_dict[character_states_to_images[character_dict['current_state']]['number_of_images']]:
        character_dict[current_image_counter] = 1.0
        # State dead: finish dead sequence and stop death animation
        if character_dict['current_state'] == 'dead':
            character_dict[current_image_counter] = previous_im_number
            self.finish_kill_character(screen_num, character_dict)
        # State throwing: finish throwing sequence depending on if character is moving or not
        elif character_dict['current_state'] == 'throwing':
            if character_dict['is_moving']:
                character_dict['current_state'] = 'walking'
            else:
                character_dict['current_state'] = 'idle'

    if int(previous_im_number) != int(character_dict[current_image_counter]):
        current_file_names = character_states_to_images[character_dict['current_state']]['file_names']
        curr_screen.ids[character_dict['name'] + str(screen_num)].source = \
            f"{character_dict[current_file_names]}{str(int(character_dict[current_image_counter]))}.png"


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


def get_aux_char_1_quad_coords(self, screen_num):
    """
    Returns Aux-Char-1's range box's (Quad) coordinates.
    :param self:
    :param screen_num: Screen number
    :return: Range box coordinates
    """
    curr_screen = self.root.screens[screen_num]
    aux_char_1_image = curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)]
    x1 = aux_char_1_image.center_x - self.AUX_CHAR_1_RANGE * curr_screen.size[0]
    y1 = aux_char_1_image.center_y - self.AUX_CHAR_1_RANGE * curr_screen.size[1]
    x2 = aux_char_1_image.center_x - self.AUX_CHAR_1_RANGE * curr_screen.size[0]
    y2 = aux_char_1_image.center_y + self.AUX_CHAR_1_RANGE * curr_screen.size[1]
    x3 = aux_char_1_image.center_x + self.AUX_CHAR_1_RANGE * curr_screen.size[0]
    y3 = aux_char_1_image.center_y + self.AUX_CHAR_1_RANGE * curr_screen.size[1]
    x4 = aux_char_1_image.center_x + self.AUX_CHAR_1_RANGE * curr_screen.size[0]
    y4 = aux_char_1_image.center_y - self.AUX_CHAR_1_RANGE * curr_screen.size[1]
    return [x1, y1, x2, y2, x3, y3, x4, y4]


def advance_to_next_phase(self, curr_screen, screen_num):
    curr_screen.current_phase += 1
    # Update phase indicator in screen
    curr_screen.ids['num_waves_lvl' + str(screen_num)].text = str(
        curr_screen.current_phase) + "/" + str(curr_screen.number_of_phases)
    # Cancel enemy spawning
    # This for loop is written like this to be able to convert to None the clock variables
    if len(curr_screen.spawn_enemies_clock_variables) > 0:
        for i in range(len(curr_screen.spawn_enemies_clock_variables)):
            curr_screen.spawn_enemies_clock_variables[i].cancel()
            curr_screen.spawn_enemies_clock_variables[i] = None

        curr_screen.spawn_enemies_clock_variables.clear()
        # Check all clock variables have been canceled and eliminated
        assert len(curr_screen.spawn_enemies_clock_variables) == 0

    if curr_screen.current_phase == curr_screen.number_of_phases:
        self.spawn_boss(screen_num)
    else:
        for enemy in curr_screen.enemies_phases[curr_screen.current_phase - 1].values():
            # If new enemies have gaussian distribution of spawn and end points, initialize those values
            if enemies_dict[enemy['type']][enemy['level']]['spawn_function'] == 'gaussian':
                enemies_dict[enemy['type']][enemy['level']]['spawn_point'] = random.random()
                enemies_dict[enemy['type']][enemy['level']]['end_point'] = random.random()
                # Control amplitude of yellow enemy spawn and end points
                if enemy['type'] == 'yellow':
                    enemies_dict[enemy['type']][enemy['level']]['spawn_point'] *= 0.9
                    enemies_dict[enemy['type']][enemy['level']]['end_point'] *= 0.9
            # Spawn new enemies
            curr_screen.spawn_enemies_clock_variables.append(
                Clock.schedule_interval(
                    partial(self.spawn_enemy,
                            screen_num,
                            enemy['type'],
                            enemy['level']),
                    enemies_dict[enemy['type']][enemy['level']]['spawn_interval']
                )
            )
        curr_screen.rewards_gathered = 0
        curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = \
            str(curr_screen.rewards_gathered) + "/" + \
            str(curr_screen.rewards_to_win_phases[curr_screen.current_phase - 1])
