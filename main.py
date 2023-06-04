#  Copyright (c) 2023. Daniel Montoya
#  This file is part of Baby Adventures Game.
#
#  Baby Adventures Game is free software: you can redistribute it and/or modify it under the terms of the GNU
#  General Public License as published by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  Baby Adventures Game is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#
#  This package is authored by:
#  Daniel Montoya (https://github.com/danielm322) (main author)
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
from kivy.core.audio import SoundLoader
import kivy.app
import kivy.uix.screenmanager
from kivy.properties import BooleanProperty
from kivy.utils import platform
from src.levels import *
import webbrowser
from src.pause_menu import PauseMenuWidget
from src.helper_fns import read_game_info


# noinspection PyUnresolvedReferences,PyArgumentList
class GameApp(kivy.app.App):
    # Imports: Do not delete even if not used in this file
    from src.character import (
        check_character_collision,
        begin_kill_character,
        get_character_bbox,
        start_character_animation_from_dict,
        update_characters_from_dict,
        get_aux_char_1_quad_coords,
        update_character_image_animation,
        finish_kill_character,
        advance_to_next_phase
    )
    from src.kiss import (
        shoot_kiss,
        check_kiss_collision_with_enemies,
        check_kiss_collision_with_bosses,
        update_kisses,
        KISS_SPEED,
        KISS_HEIGHT,
        KISS_WIDTH
    )
    from src.enemy import (
        spawn_enemy,
        check_enemy_collision,
        enemy_animation_completed,
        update_enemies,
        spawn_rocket_at_enemy_center_to_ch_center,
        kill_enemy,
        remove_fire_from_screen,
        spawn_enemy_underling,
        launch_character
    )
    from src.boss import (
        spawn_boss,
        update_bosses,
        boss_arrives_animation,
        boss_defeat_animation_start,
        boss_defeat_animation_finish,
        check_boss_collision,
        kill_boss
    )
    from src.special_attack_char import (
        shoot_special,
        update_specials,
        check_special_collision,
        enable_special_attack,
        get_special_quad_coords,
        special_attack_properties
    )
    from src.special_attack_fire_triangle import (
        activate_special_fire_triangle,
        get_special_triangle_coords,
        finish_special_triangle,
        enable_special_triangle
    )
    from src.screen_management import (
        screen_on_pre_enter,
        screen_on_enter,
        screen_on_leave,
        update_screen,
        pause_game,
        on_continue_button_pressed,
        on_restart_button_pressed,
        on_go_to_main_menu_button_pressed,
        back_to_main_screen,
        main_screen_on_enter,
        main_screen_on_leave,
        enter_about_section,
        quit_about_section
    )
    from src.state_management import (
        on_special_button_state,
        on_special_triangle_button_state,
        on_toggle_button_state,
        on_move_aux_char_1_button,
        on_move_aux_char_2_button
    )
    from src.reward import spawn_reward, update_rewards
    from src.boss_reward import spawn_boss_reward, boss_reward_animation_completed
    from src.helper_fns import adjust_character_life_bar
    from src.aux_char_1 import auto_shoot

    ####################################################################
    # GAME PARAMETERS
    ####################################################################
    # Auxiliary characters properties
    AUX_CHAR_1_RANGE = 0.3  # In screen proportion (same range in width and height, is a rectangle)
    AUX_CHAR_1_FIRE_INTERVAL = 0.8  # In seconds

    # App properties
    SIDE_BAR_WIDTH = 0.08  # In screen percentage
    APP_TIME_FACTOR = 40  # In number of updates per second
    SCREEN_UPDATE_RATE = 1 / APP_TIME_FACTOR
    MOVEMENT_PIXEL_TOLERANCE = 8  # Number of pixels of tolerance to accept a widget is in a given position
    LEVEL_WHEN_SPECIAL_IS_ACTIVATED = 2
    LEVEL_WHEN_AUX_CHAR_1_ENTERS = 8
    LEVEL_WHEN_AUX_CHAR_2_ENTERS = 6
    LEVEL_WHEN_SPECIAL_TRIANGLE_IS_ACTIVATED = 11

    ####################################################################
    # GAME VARIABLES
    ####################################################################
    # Special ability button
    special_button_enabled = BooleanProperty(True)

    # Auxiliary characters buttons and quad variables
    move_aux_char_1_button_enabled = BooleanProperty(True)
    move_aux_char_2_button_enabled = BooleanProperty(True)
    aux_char_1_quad = None  # Quad to see the aux char 1 range

    # Gameplay variables:
    next_level = 1  # Default first level to be played (Activate just one level)
    clock_update_fn_variable = None
    clock_banana_throw_variable = None

    # Debugging
    # char_bounding_box = None  # Debugging purposes
    # entity_bounding_box = None  # Debugging purposes

    # Triangle special ability variables
    special_triangle_shape = None
    special_triangle_border = None

    # Initialization of audio files
    sound_reward_collected = None
    sound_level_finished = None
    sound_level_play = None
    sound_game_over = None
    sound_baby_laughs = None
    sound_enemy_laughs = None
    sound_enemy_dies = None
    sound_kiss = None
    sound_heal = None
    sound_main_menu = None
    sound_about_section = None

    def on_start(self):
        self.init_audio()
        self.sound_main_menu.play()
        self.next_level = read_game_info(platform)
        self.activate_levels(self.next_level)

    def init_audio(self):
        self.sound_main_menu = SoundLoader.load("audio/a-hero-of-the-80s-126684.ogg")
        self.sound_about_section = SoundLoader.load("audio/8-bit-arcade-138828.ogg")
        self.sound_heal = SoundLoader.load("audio/Heal.ogg")
        self.sound_kiss = SoundLoader.load("audio/kiss_sound.wav")
        self.sound_enemy_dies = SoundLoader.load("audio/goblin_hurt.ogg")
        self.sound_enemy_laughs = SoundLoader.load("audio/goblin_laugh.ogg")
        self.sound_baby_laughs = SoundLoader.load("audio/baby_laughs_special.ogg")
        self.sound_game_over = SoundLoader.load("audio/goblin_laugh_2.ogg")
        self.sound_level_play = SoundLoader.load("audio/superhero-intro-111393.ogg")
        self.sound_level_finished = SoundLoader.load("audio/success-fanfare-trumpets-6185.ogg")
        self.sound_reward_collected = SoundLoader.load(
            "audio/short-success-sound-glockenspiel-treasure-video-game-6346.ogg")

        self.sound_main_menu.loop = True
        self.sound_level_play.loop = True
        self.sound_about_section.loop = True
        self.sound_main_menu.volume = 0.4
        self.sound_level_play.volume = 0.4
        self.sound_about_section.volume = 0.5
        self.sound_game_over.volume = 1
        self.sound_kiss.volume = .5
        self.sound_level_finished.volume = .6
        self.sound_reward_collected.volume = 1.5
        self.sound_enemy_dies.volume = 0.2
        self.sound_enemy_laughs.volume = 0.6
        self.sound_baby_laughs.volume = 0.5
        self.sound_heal.volume = 1.5

    def activate_levels(self, next_level_num):
        num_levels = len(self.root.screens[0].ids['lvls_imagebuttons'].children)

        levels_imagebuttons = self.root.screens[0].ids['lvls_imagebuttons'].children
        for i in range(num_levels - next_level_num, num_levels):
            levels_imagebuttons[i].disabled = False

        for i in range(0, num_levels - next_level_num):
            levels_imagebuttons[i].disabled = True

    def touch_down_handler(self, screen_num, args):
        curr_screen = self.root.screens[screen_num]
        if args[1].psx > self.SIDE_BAR_WIDTH \
                and not curr_screen.state_paused \
                and not curr_screen.characters_dict['character']['is_killed']:
            if not curr_screen.characters_dict['character']['shoot_state'] \
                    and not curr_screen.characters_dict['character']['shoot_special_state'] \
                    and not curr_screen.move_aux_char_1_state \
                    and not curr_screen.move_aux_char_2_state:
                self.start_character_animation_from_dict(screen_num, args[1].ppos,
                                                         curr_screen.characters_dict['character'])
            if not curr_screen.characters_dict['character']['shoot_state'] \
                    and not curr_screen.characters_dict['character']['shoot_special_state'] \
                    and not curr_screen.move_aux_char_2_state \
                    and curr_screen.move_aux_char_1_state:
                self.start_character_animation_from_dict(screen_num, args[1].ppos,
                                                         curr_screen.characters_dict['aux_char_1'])
            if not curr_screen.characters_dict['character']['shoot_state'] \
                    and not curr_screen.characters_dict['character']['shoot_special_state'] \
                    and not curr_screen.move_aux_char_1_state \
                    and curr_screen.move_aux_char_2_state:
                self.start_character_animation_from_dict(screen_num, args[1].ppos,
                                                         curr_screen.characters_dict['aux_char_2'])
            if not curr_screen.characters_dict['character']['shoot_special_state'] \
                    and curr_screen.characters_dict['character']['shoot_state'] \
                    and not curr_screen.move_aux_char_1_state:
                self.shoot_kiss(screen_num, args[1].ppos)
            if not curr_screen.characters_dict['character']['shoot_state'] \
                    and not curr_screen.move_aux_char_1_state \
                    and curr_screen.characters_dict['character']['shoot_special_state']:
                self.shoot_special(screen_num, args[1].ppos)

    @staticmethod
    def email_me():
        webbrowser.open("mailto:daniel.montoyav@gmail.com")

    @staticmethod
    def github_link():
        webbrowser.open("https://github.com/danielm322/Baby_Adventures_Game")

    @staticmethod
    def linkedin_link():
        webbrowser.open("https://www.linkedin.com/in/daniel-montoya-ds/")


class MainScreen(kivy.uix.screenmanager.Screen):
    pass


class About(kivy.uix.screenmanager.Screen):
    pass


class Credits(kivy.uix.screenmanager.Screen):
    pass


if __name__ == "__main__":
    app = GameApp()
    app.run()
