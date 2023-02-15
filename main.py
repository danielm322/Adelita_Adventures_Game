import random
import time

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '400')
import kivy.uix.image
import kivy.app
import kivy.uix.screenmanager
import kivy.animation
import kivy.core.audio
from os import getcwd
import kivy.uix.label
from functools import partial
from kivy.properties import Clock
import kivy.clock


class GameApp(kivy.app.App):
    from character import start_character_animation, check_character_collision
    from kiss import shoot_kiss, check_kiss_collision, kiss_animation_completed
    from enemy import spawn_enemy, check_enemy_collision, enemy_animation_completed
    from reward import spawn_reward, reward_animation_completed
    from boss import spawn_boss, start_boss_animation, boss_animation_completed, check_boss_collision
    side_bar_width = 0.08  # In screen percentage
    enemy_width = 0.15
    enemy_height = 0.18
    kiss_width = 0.04
    kiss_height = 0.04
    kiss_duration = 0.3  # In seconds to arrive to the endpoint
    reward_size = 0.1
    reward_duration = 10  # In seconds to disappear

    def screen_on_leave(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        for _, enemy in curr_screen.enemies_ids.items():
            kivy.animation.Animation.cancel_all(enemy)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy)
        curr_screen.enemies_ids = {}
        for _, reward in curr_screen.rewards_ids.items():
            kivy.animation.Animation.cancel_all(reward)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward)
        curr_screen.rewards_ids = {}
        for _, kiss in curr_screen.kisses_ids.items():
            kivy.animation.Animation.cancel_all(kiss)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss)
        curr_screen.kisses_ids = {}
        for _, boss in curr_screen.bosses_ids.items():
            kivy.animation.Animation.cancel_all(boss['image'])
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(boss['image'])
        curr_screen.bosses_ids = {}
        curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"

    def screen_on_enter(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        curr_screen.character_killed = False
        if not curr_screen.phase_1_completed:
            curr_screen.rewards_gathered = 0
            Clock.schedule_interval(partial(self.spawn_enemy, screen_num), curr_screen.enemy_spawn_interval)
        else:
            self.spawn_boss(screen_num)
            for _, boss in curr_screen.bosses_ids.items():
                boss['hitpoints'] = curr_screen.boss_hitpoints
        curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = "Stars " + str(
            curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_1)

    def touch_down_handler(self, screen_num, args):
        # print(args[1].is_double_tap)
        curr_screen = self.root.screens[screen_num]
        if not curr_screen.character_killed and args[1].psx > self.side_bar_width and not curr_screen.shoot_state:
            self.start_character_animation(screen_num, args[1].ppos)
        if not curr_screen.character_killed and args[1].psx > self.side_bar_width and curr_screen.shoot_state:
            self.shoot_kiss(screen_num, args[1].ppos)

    def on_toggle_button_state(self, widget, screen_num):
        curr_screen = self.root.screens[screen_num]
        if widget.state == "normal":
            curr_screen.shoot_state = False
        else:
            curr_screen.shoot_state = True

    def back_to_main_screen(self, screenManager, *args):
        screenManager.current = "main"


class MainScreen(kivy.uix.screenmanager.Screen):
    pass


class Level1(kivy.uix.screenmanager.Screen):
    character_killed = False
    shoot_state = False
    phase_1_completed = False
    level_completed = False
    char_anim_duration = 0.7
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    enemy_anim_duration_min = 6.0
    enemy_anim_duration_max = 9.0
    enemy_spawn_interval = 4  # In seconds
    rewards_gathered = 0
    rewards_to_win_ph_1 = 3
    boss_width = 0.4
    boss_height = 0.45
    boss_intro_duration = 10
    boss_movement_duration = 6
    boss_hitpoints = 5


class Level2(kivy.uix.screenmanager.Screen):
    character_killed = False
    shoot_state = False
    phase_1_completed = False
    level_completed = False
    char_anim_duration = 0.7
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    enemy_anim_duration_min = 4.0
    enemy_anim_duration_max = 7.0
    enemy_spawn_interval = 3  # In seconds
    rewards_gathered = 0
    rewards_to_win_ph_1 = 6
    boss_width = 0.4
    boss_height = 0.45
    boss_intro_duration = 10
    boss_movement_duration = 6
    boss_hitpoints = 5

app = GameApp()
app.run()
