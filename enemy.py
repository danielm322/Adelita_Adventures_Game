import random
import time
import kivy.uix.image
from functools import partial
from helper_fns import get_enemy_start_end_positions


def spawn_enemy(self, screen_num, *largs):
    curr_screen = self.root.screens[screen_num]
    if not curr_screen.character_killed and not curr_screen.phase_1_completed:
        r_duration = random.uniform(curr_screen.enemy_anim_duration_min,
                                    curr_screen.enemy_anim_duration_max)
        spawn_pos, finish_pos = get_enemy_start_end_positions(self.side_bar_width,
                                                              self.enemy_width,
                                                              self.enemy_height)
        enemy = kivy.uix.image.Image(source="graphics/entities/enemy.png",
                                     size_hint=(self.enemy_width, self.enemy_height),
                                     pos_hint=spawn_pos, allow_stretch=True)
        curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(enemy, index=-1)
        # create a unique identifier for each enemy
        time_stamp = str(time.time())
        curr_screen.enemies_ids['enemy_' + time_stamp] = enemy
        enemy_anim = kivy.animation.Animation(pos_hint=finish_pos,
                                              duration=r_duration)
        enemy_anim.bind(on_progress=partial(self.check_enemy_collision, enemy, screen_num))
        enemy_anim.bind(on_complete=partial(self.enemy_animation_completed, enemy, time_stamp, screen_num))
        enemy_anim.start(enemy)


def check_enemy_collision(self, enemy, screen_num, *args):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * self.enemy_width / 3
    gap_y = curr_screen.height * self.enemy_height / 3
    if enemy.collide_widget(character_image) and \
            abs(enemy.center[0] - character_image.center[0]) <= gap_x and \
            abs(enemy.center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_killed = True
        kivy.animation.Animation.cancel_all(character_image)
        for enemy_key, enemy in curr_screen.enemies_ids.items():
            kivy.animation.Animation.cancel_all(enemy)
        kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 2)

def enemy_animation_completed(self, enemy, time_stamp, screen_num, *args):
    # enemy_image = args[1]
    curr_screen = enemy.parent.parent.parent
    # kivy.animation.Animation.cancel_all(enemy)
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy)
    del curr_screen.enemies_ids['enemy_' + time_stamp]
