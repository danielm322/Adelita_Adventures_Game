# import time
# from kivy.config import Config
# import os
import random
from kivy.graphics import Color, Quad

# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '400')
from kivy.core.audio import SoundLoader
import kivy.uix.image
import kivy.app
import kivy.uix.screenmanager
import kivy.animation
import kivy.uix.label
from functools import partial
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.utils import platform
from levels import Level1, Level2
from pause_menu import PauseMenuWidget
from helper_fns import read_game_info
from enemies_dict import enemies_dict


class GameApp(kivy.app.App):
    from character import start_character_animation, check_character_collision, update_character, kill_character
    from kiss import shoot_kiss, check_kiss_collision_with_enemies, check_kiss_collision_with_bosses, update_kisses
    from enemy import spawn_enemy, check_enemy_collision, enemy_animation_completed, update_enemies, spawn_rocket_at_enemy_center_to_ch_center
    # from enemy_red import spawn_enemy_red
    # from enemy_yellow import spawn_enemy_yellow
    from reward import spawn_reward, update_rewards
    from boss import spawn_boss, update_bosses, boss_arrives_animation, boss_defeat_animation_start, \
        boss_defeat_animation_finish, check_boss_collision, kill_boss
    from boss_reward import spawn_boss_reward, boss_reward_animation_completed
    from helper_fns import adjust_character_life_bar
    from special_attack_char import shoot_special, update_specials, check_special_collision, enable_special_attack, \
        get_special_quad_coords
    # pause_menu_widget = ObjectProperty()
    side_bar_width = 0.08  # In screen percentage
    next_level = 1  # Default first level to be played (Activate just one level)
    clock_spawn_enemies_variable = None
    clock_update_fn_variable = None
    kiss_width = 0.04
    kiss_height = 0.04
    kiss_speed = 25
    special_attack_properties = {
        'init_width': 0.04,
        'init_height': 0.04,
        'max_width': 0.32,
        'max_height': 0.32,
        'extra_height_parabola': 0.35,  # Extra height of parabola in screen proportion
        'time_to_land': 2.0,
        'attack_radius': 0.16,  # In screen proportion
        'quad': None,
        'damage': 10,
        'reload_time': 8,
        # 'button_enabled': BooleanProperty(True),
        # 'grow_size_factor': 400,
        'grow_size_factor': 10,
        'min_dist_x': 0.15,  # In screen proportion
        'source_img': "graphics/entities/diaper.png",
    }
    # special_attack_init_width = 0.04
    # special_attack_init_height = 0.04
    # special_extra_height = 0.35  # Extra height of parabola in screen proportion
    # special_attack_speed_x = 7
    # special_attack_radius = 0.15  # In screen proportion
    # special_attack_quad = None
    # special_attack_damage = 10
    # special_attack_reload_time = 8
    special_button_enabled = BooleanProperty(True)
    # special_grow_size_factor = 400
    # special_min_dist_x = 0.15  # In screen proportion
    reward_size = 0.1
    reward_duration = 12  # In seconds to disappear
    boss_reward_initial_size_hint = (0.05, 0.05)
    boss_reward_animation_duration = 6
    APP_TIME_FACTOR = 40  # In number of updates per second
    SCREEN_UPDATE_RATE = 1 / APP_TIME_FACTOR
    # CHARACTER_HITPOINTS = 100
    MOVEMENT_PIXEL_TOLERANCE = 4  # Number of pixels of tolerance to accept a widget is in a given position

    def on_start(self):
        self.init_audio()
        self.sound_main_menu.play()
        self.next_level = read_game_info(platform)
        self.activate_levels(self.next_level)

    def init_audio(self):
        self.sound_main_menu = SoundLoader.load("audio/a-hero-of-the-80s-126684.ogg")
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
        self.sound_main_menu.volume = 0.4
        self.sound_level_play.volume = 0.4
        self.sound_game_over.volume = 1
        self.sound_kiss.volume = .5
        self.sound_level_finished.volume = .6
        self.sound_reward_collected.volume = 1.5
        self.sound_enemy_dies.volume = 0.2
        self.sound_enemy_laughs.volume = 0.6
        self.sound_baby_laughs.volume = 0.5

    def activate_levels(self, next_level_num):
        num_levels = len(self.root.screens[0].ids['lvls_imagebuttons'].children)

        levels_imagebuttons = self.root.screens[0].ids['lvls_imagebuttons'].children
        for i in range(num_levels - next_level_num, num_levels):
            levels_imagebuttons[i].disabled = False
            # levels_imagebuttons[i].color = [1, 1, 1, 1]

        for i in range(0, num_levels - next_level_num):
            levels_imagebuttons[i].disabled = True
            # levels_imagebuttons[i].color = [1, 1, 1, 0.5]

    def screen_on_leave(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        # REMOVE
        # Enemies
        for _, enemy in curr_screen.enemies_ids.items():
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy['image'])
        curr_screen.enemies_ids.clear()
        # Rewards
        for _, reward in curr_screen.rewards_ids.items():
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward['image'])
        curr_screen.rewards_ids.clear()
        # Kisses
        for _, kiss in curr_screen.kisses_ids.items():
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss['image'])
        curr_screen.kisses_ids.clear()
        # Bosses
        for _, boss in curr_screen.bosses_ids.items():
            kivy.animation.Animation.cancel_all(boss['image'])
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(boss['image'])
        curr_screen.bosses_ids.clear()
        # Toggle kiss button
        if screen_num > 1:
            curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
        curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"
        # Stop level music
        if self.sound_level_play.state == 'play':
            self.sound_level_play.stop()
        # Stop Schedule to spawn enemies
        if self.clock_spawn_enemies_variable is not None:
            self.clock_spawn_enemies_variable.cancel()
            self.clock_spawn_enemies_variable = None
        # Unschedule the update function
        # Clock.unschedule(partial(self.update_screen, screen_num))
        if self.clock_update_fn_variable is not None:
            self.clock_update_fn_variable.cancel()
            self.clock_update_fn_variable = None
        # Delete special attack quad
        if self.special_attack_quad is not None:
            self.special_attack_quad = None

    def screen_on_pre_enter(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        curr_screen.character_dict['killed'] = False
        curr_screen.state_paused = False
        curr_screen.phase_1_completed = False
        if curr_screen.number_of_phases == 3:
            curr_screen.phase_2_completed = False
        curr_screen.rewards_gathered = 0
        curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
            curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_1)
        curr_screen.character_dict['damage_received'] = 0
        self.adjust_character_life_bar(screen_num)
        # if self.sound_main_menu.state == "play":
        #     self.sound_main_menu.stop()
        pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
        pause_menu_widget.opacity = 0.
        if enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_function'] == 'gaussian':
            enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_point'] = random.random()
            enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['end_point'] = random.random()
            if curr_screen.enemy_phase_1['type'] == 'yellow':
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_point'] *= 0.9
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['end_point'] *= 0.9

    def screen_on_enter(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        # Always begin now in the first phase
        if self.clock_spawn_enemies_variable is None:
            self.clock_spawn_enemies_variable = Clock.schedule_interval(
                # partial(self.spawn_enemy, screen_num), curr_screen.enemy_spawn_interval
                # partial(eval(curr_screen.phases_spawn_fns['phase_1']), screen_num),
                partial(self.spawn_enemy,
                        screen_num,
                        curr_screen.enemy_phase_1['type'],
                        curr_screen.enemy_phase_1['level']),
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_interval']
            )
        self.sound_level_play.play()
        # Start update screen function
        self.clock_update_fn_variable = Clock.schedule_interval(partial(self.update_screen, screen_num),
                                                                self.SCREEN_UPDATE_RATE)

    def update_screen(self, screen_num, *args):
        if not self.root.screens[screen_num].state_paused:
            # This factor standardizes the passage of time in one cycle, as is a proportion to the expected timestep
            cycle_time_factor = args[0] * self.APP_TIME_FACTOR
            self.update_enemies(screen_num, dt=cycle_time_factor)
            self.update_kisses(screen_num, dt=cycle_time_factor)
            self.update_specials(screen_num, dt=args[0])  # We pass actual seconds
            self.update_character(screen_num, dt=cycle_time_factor)
            self.update_rewards(screen_num, dt=args[0])  # We pass actual seconds
            if self.root.screens[screen_num].phase_1_completed:
                self.update_bosses(screen_num, dt=cycle_time_factor)

    def touch_down_handler(self, screen_num, args):
        # print(args[1].is_double_tap)
        curr_screen = self.root.screens[screen_num]
        if not curr_screen.character_dict['killed'] \
                and args[1].psx > self.side_bar_width \
                and not curr_screen.character_dict['shoot_state'] \
                and not curr_screen.character_dict['shoot_special_state'] \
                and not curr_screen.state_paused:
            self.start_character_animation(screen_num, args[1].ppos)
        if not curr_screen.character_dict['killed'] \
                and args[1].psx > self.side_bar_width \
                and not curr_screen.character_dict['shoot_special_state'] \
                and curr_screen.character_dict['shoot_state'] \
                and not curr_screen.state_paused:
            self.shoot_kiss(screen_num, args[1].ppos)
        if not curr_screen.character_dict['killed'] \
                and args[1].psx > self.side_bar_width \
                and not curr_screen.character_dict['shoot_state'] \
                and curr_screen.character_dict['shoot_special_state'] \
                and not curr_screen.state_paused:
            self.shoot_special(screen_num, args[1].ppos)

    def on_special_button_state(self, widget, screen_num):
        curr_screen = self.root.screens[screen_num]
        if widget.state == "normal":
            curr_screen.character_dict['shoot_special_state'] = False
            curr_screen.canvas.remove_group(u"special_radius")
        else:
            if curr_screen.ids['kiss_button_lvl' + str(screen_num)].state == "down":
                curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"

            curr_screen.character_dict['shoot_special_state'] = True
            # Draw rectangle with the minimum distance to fire special
            quad_coords = self.get_special_quad_coords(screen_num)
            with curr_screen.canvas:
                Color(0, 0, 0, 0.2)
                self.special_attack_properties['quad'] = Quad(points=quad_coords, group=u"special_radius")

    def on_toggle_button_state(self, widget, screen_num):
        curr_screen = self.root.screens[screen_num]
        if widget.state == "normal":
            widget.source = "graphics/entities/kiss1_bw.png"
            curr_screen.character_dict['shoot_state'] = False
        else:
            if screen_num > 1 and curr_screen.ids['special_button_lvl' + str(screen_num)].state == "down":
                curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
            widget.source = "graphics/entities/kiss1.png"
            curr_screen.character_dict['shoot_state'] = True

    def pause_game(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        curr_screen.state_paused = True
        pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
        pause_menu_widget.opacity = 1.
        if not curr_screen.phase_1_completed \
                or (curr_screen.number_of_phases == 3 and not curr_screen.phase_2_completed):
            # Stop enemy spawning
            if self.clock_spawn_enemies_variable is not None:
                self.clock_spawn_enemies_variable.cancel()


    def on_continue_button_pressed(self, *args):
        curr_screen = args[0]
        screen_num = int(curr_screen.name[5:])
        curr_screen.state_paused = False
        pause_menu_widget = curr_screen.ids['pause_menu_lvl' + str(screen_num)]
        pause_menu_widget.opacity = 0.
        if not curr_screen.phase_1_completed:
            # Restart enemy spawning
            self.clock_spawn_enemies_variable = Clock.schedule_interval(
                partial(self.spawn_enemy,
                        screen_num,
                        curr_screen.enemy_phase_1['type'],
                        curr_screen.enemy_phase_1['level']),
                enemies_dict[curr_screen.enemy_phase_1['type']][curr_screen.enemy_phase_1['level']]['spawn_interval']
            )
        elif curr_screen.number_of_phases == 3 and not curr_screen.phase_2_completed:
            # Restart enemy spawning
            self.clock_spawn_enemies_variable = Clock.schedule_interval(
                partial(self.spawn_enemy,
                        screen_num,
                        curr_screen.enemy_phase_2['type'],
                        curr_screen.enemy_phase_2['level']),
                enemies_dict[curr_screen.enemy_phase_2['type']][curr_screen.enemy_phase_2['level']]['spawn_interval']
            )

    def on_restart_button_pressed(self, *args):
        curr_screen = args[0]
        screen_num = int(curr_screen.name[5:])
        self.screen_on_leave(screen_num)
        self.screen_on_pre_enter(screen_num)
        self.screen_on_enter(screen_num)

    def on_go_to_main_menu_button_pressed(self, *args):
        curr_screen = args[0]
        # screen_num = int(curr_screen.name[5:])
        # self.sound_level_play.stop()
        self.back_to_main_screen(curr_screen.parent)

    def back_to_main_screen(self, screenManager, *args):
        screenManager.current = "main"
        # self.sound_main_menu.play()

    def main_screen_on_enter(self):
        self.sound_main_menu.play()
        self.next_level = read_game_info(platform)
        self.activate_levels(self.next_level)

    def main_screen_on_leave(self):
        self.sound_main_menu.stop()


class MainScreen(kivy.uix.screenmanager.Screen):
    pass


app = GameApp()
app.run()
