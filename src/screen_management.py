import random
from functools import partial
import kivy.animation
from kivy.clock import Clock
from kivy.utils import platform
from src.enemies_dict import enemies_dict
from src.helper_fns import read_game_info


def screen_on_leave(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    # REMOVE
    # Enemies
    for _, enemy in curr_screen.enemies_ids.items():
        curr_screen.remove_widget(enemy['image'])
    curr_screen.enemies_ids.clear()
    # Rewards
    for _, reward in curr_screen.rewards_ids.items():
        curr_screen.remove_widget(reward['image'])
    curr_screen.rewards_ids.clear()
    # Kisses
    for _, kiss in curr_screen.kisses_ids.items():
        curr_screen.remove_widget(kiss['image'])
    curr_screen.kisses_ids.clear()
    # Bosses
    for _, boss in curr_screen.bosses_ids.items():
        kivy.animation.Animation.cancel_all(boss['image'])
        curr_screen.remove_widget(boss['image'])
    curr_screen.bosses_ids.clear()
    # Toggle kiss button
    if screen_num >= self.LEVEL_WHEN_SPECIAL_IS_ACTIVATED:
        curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
    curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"
    # Stop level music
    if self.sound_level_play.state == 'play':
        self.sound_level_play.stop()
    # Stop Schedule to spawn enemies
    if len(curr_screen.spawn_enemies_clock_variables) > 0:
        for i in range(len(curr_screen.spawn_enemies_clock_variables)):
            curr_screen.spawn_enemies_clock_variables[i].cancel()
            curr_screen.spawn_enemies_clock_variables[i] = None

        curr_screen.spawn_enemies_clock_variables.clear()
        assert len(curr_screen.spawn_enemies_clock_variables) == 0
    # Unschedule the update function
    if self.clock_update_fn_variable is not None:
        self.clock_update_fn_variable.cancel()
        self.clock_update_fn_variable = None
    # Delete special attack quad
    if self.special_attack_properties['quad'] is not None:
        self.special_attack_properties['quad'] = None
    # Stop auto shoot of aux char 1
    if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS and self.clock_banana_throw_variable is not None:
        self.clock_banana_throw_variable.cancel()
        self.clock_banana_throw_variable = None


def screen_on_pre_enter(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.current_phase = 1
    curr_screen.ids['num_waves_lvl' + str(screen_num)].text = str(
        curr_screen.current_phase) + "/" + str(curr_screen.number_of_phases)
    for character in curr_screen.characters_dict.values():
        character['is_killed'] = False
        character['current_state'] = 'idle'
        character['damage_received'] = 0
        character['is_dead_image_counter'] = 1.0
        self.adjust_character_life_bar(screen_num, character)

    # Disable aux characters buttons by default, the activate if appropriate
    self.move_aux_char_1_button_enabled = False
    self.move_aux_char_2_button_enabled = False
    self.special_button_enabled = False

    # Enable special attack button
    if screen_num >= self.LEVEL_WHEN_SPECIAL_IS_ACTIVATED:
        self.special_button_enabled = True
    # In case Aux Char 1 was dead (& opaque):
    if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS:
        curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)].opacity = 1
        curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)].center_x = 0.25 * curr_screen.size[0]
        curr_screen.ids['aux_char_1_image_lvl' + str(screen_num)].center_y = 0.25 * curr_screen.size[1]
        curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state = "normal"
        self.move_aux_char_1_button_enabled = True
    # In case Aux Char 2 was dead (& opaque):
    if screen_num >= self.LEVEL_WHEN_AUX_CHAR_2_ENTERS:
        curr_screen.ids['aux_char_2_image_lvl' + str(screen_num)].opacity = 1
        curr_screen.ids['aux_char_2_image_lvl' + str(screen_num)].center_x = 0.25 * curr_screen.size[0]
        curr_screen.ids['aux_char_2_image_lvl' + str(screen_num)].center_y = 0.75 * curr_screen.size[1]
        curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state = "normal"
        self.move_aux_char_2_button_enabled = True
    if screen_num >= self.LEVEL_WHEN_SPECIAL_TRIANGLE_IS_ACTIVATED:
        curr_screen.ids['special_triangle_button_lvl' + str(screen_num)].state = 'normal'
        curr_screen.ids['special_triangle_button_lvl' + str(screen_num)].disabled = False
    curr_screen.state_paused = False
    curr_screen.rewards_gathered = 0
    curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
        curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_phases[0])
    # Make Pause menu widget invisible
    pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
    pause_menu_widget.opacity = 0.
    # If new enemies have gaussian distribution of spawn and end points, initialize those values:
    for enemy in curr_screen.enemies_phases[curr_screen.current_phase - 1].values():
        if enemies_dict[enemy['type']][enemy['level']]['spawn_function'] == 'gaussian':
            enemies_dict[enemy['type']][enemy['level']]['spawn_point'] = random.random()
            enemies_dict[enemy['type']][enemy['level']]['end_point'] = random.random()
            if enemy['type'] == 'yellow':
                enemies_dict[enemy['type']][enemy['level']]['spawn_point'] *= 0.9
                enemies_dict[enemy['type']][enemy['level']]['end_point'] *= 0.9


def screen_on_enter(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    # Strangely, adjusting character speed works well here, but not on pre enter:
    for character in curr_screen.characters_dict.values():
        # Set characters speed
        character['speed'] = (curr_screen.size[0] + curr_screen.size[1]) * character['speed_factor']
        # Update remaining life bar widget
        remaining_life_percent_lvl_widget = curr_screen.ids[character['life_bar_id'] + str(screen_num)]
        character_image = curr_screen.ids[character['name'] + str(screen_num)]
        remaining_life_percent_lvl_widget.x = character_image.x
        remaining_life_percent_lvl_widget.y = character_image.top
    # Each character's speed can be modified to have different speeds for each character,
    # adding a speed factor to each character
    # Always begin in the first phase
    for enemy in curr_screen.enemies_phases[0].values():
        curr_screen.spawn_enemies_clock_variables.append(
            Clock.schedule_interval(
                partial(self.spawn_enemy,
                        screen_num,
                        enemy['type'],
                        enemy['level']),
                enemies_dict[enemy['type']][enemy['level']]['spawn_interval']
            )
        )
    self.sound_level_play.play()
    # Start update screen function
    self.clock_update_fn_variable = Clock.schedule_interval(partial(self.update_screen, screen_num),
                                                            self.SCREEN_UPDATE_RATE)
    if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS:
        self.clock_banana_throw_variable = Clock.schedule_interval(
            partial(self.auto_shoot, screen_num),
            self.AUX_CHAR_1_FIRE_INTERVAL
        )
    # with curr_screen.canvas:
    #     Color(1, 0, 0, 0.2)
    #     self.char_bounding_box = Quad(points=self.get_character_bbox(screen_num))


def update_screen(self, screen_num, *args):
    if not self.root.screens[screen_num].state_paused:
        # This factor standardizes the passage of time in one cycle, as is a proportion to the expected timestep
        cycle_time_factor = args[0] * self.APP_TIME_FACTOR
        self.update_enemies(screen_num, dt=cycle_time_factor)
        self.update_specials(screen_num, dt=args[0])  # We pass actual seconds
        self.update_characters_from_dict(screen_num, dt=cycle_time_factor)
        self.update_kisses(screen_num, dt=cycle_time_factor)
        self.update_rewards(screen_num, dt=args[0])  # We pass actual seconds
        if self.root.screens[screen_num].current_phase == self.root.screens[screen_num].number_of_phases:
            self.update_bosses(screen_num, dt=cycle_time_factor)


def pause_game(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    curr_screen.state_paused = True
    pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
    pause_menu_widget.opacity = 1.
    # Cancel enemy spawning
    if len(curr_screen.spawn_enemies_clock_variables) > 0:
        for i in range(len(curr_screen.spawn_enemies_clock_variables)):
            curr_screen.spawn_enemies_clock_variables[i].cancel()
            curr_screen.spawn_enemies_clock_variables[i] = None

        curr_screen.spawn_enemies_clock_variables.clear()
        # Check all clock variables have been canceled and eliminated
        assert len(curr_screen.spawn_enemies_clock_variables) == 0
    # Make enemies opaque on pause since I couldn't find a way to make the pause menu to be above the enemies
    for _, enemy in curr_screen.enemies_ids.items():
        enemy['image'].opacity = 0.1
    for _, special in curr_screen.specials_ids.items():
        special['image'].opacity = 0.1
    for _, boss in curr_screen.bosses_ids.items():
        boss['image'].opacity = 0.1


def on_continue_button_pressed(self, *args):
    curr_screen = args[0]
    screen_num = int(curr_screen.name[5:])
    curr_screen.state_paused = False
    pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
    pause_menu_widget.opacity = 0.
    # Restart spawning of enemies if phase is not last
    if curr_screen.current_phase < curr_screen.number_of_phases:
        for enemy in curr_screen.enemies_phases[curr_screen.current_phase - 1].values():
            curr_screen.spawn_enemies_clock_variables.append(
                Clock.schedule_interval(
                    partial(self.spawn_enemy,
                            screen_num,
                            enemy['type'],
                            enemy['level']),
                    enemies_dict[enemy['type']][enemy['level']]['spawn_interval']
                )
            )
        assert len(curr_screen.spawn_enemies_clock_variables) == len(
            curr_screen.enemies_phases[curr_screen.current_phase - 1]
        )
    # Reestablish opacity to one on un-pause
    for _, enemy in curr_screen.enemies_ids.items():
        enemy['image'].opacity = 1
    for _, special in curr_screen.specials_ids.items():
        special['image'].opacity = 1
    for _, boss in curr_screen.bosses_ids.items():
        boss['image'].opacity = 1


def on_restart_button_pressed(self, *args):
    curr_screen = args[0]
    screen_num = int(curr_screen.name[5:])
    self.screen_on_leave(screen_num)
    self.screen_on_pre_enter(screen_num)
    self.screen_on_enter(screen_num)


def on_go_to_main_menu_button_pressed(self, *args):
    curr_screen = args[0]
    self.back_to_main_screen(curr_screen.parent)


def back_to_main_screen(self, screen_manager, *args):
    screen_manager.current = "main"


def main_screen_on_enter(self):
    self.sound_main_menu.play()
    self.next_level = read_game_info(platform)
    self.activate_levels(self.next_level)


def main_screen_on_leave(self):
    self.sound_main_menu.stop()


def enter_about_section(self, screen_manager):
    screen_manager.transition.direction = 'left'
    self.root.current = "about"
    self.sound_about_section.play()


def quit_about_section(self):
    if self.root.current == "main":
        self.sound_about_section.stop()
