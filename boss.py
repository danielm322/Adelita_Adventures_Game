import time
import random
import kivy.uix.image
from functools import partial


def spawn_boss(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    spawn_pos = (curr_screen.size[0],
                 curr_screen.size[1] * (0.5 - curr_screen.boss_height / 2))
    finish_pos = (0,
                  curr_screen.size[1] * (0.5 - curr_screen.boss_height / 2))
    boss = kivy.uix.image.Image(source=f"graphics/entities/boss_{screen_num}.png",
                                size_hint=(curr_screen.boss_width, curr_screen.boss_height),
                                pos=spawn_pos, allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(boss, index=-1)
    time_stamp = str(time.time())
    curr_screen.bosses_ids['boss_' + time_stamp] = {'image': boss,
                                                    'hitpoints': curr_screen.boss_hitpoints}
    boss_anim = kivy.animation.Animation(pos=finish_pos,
                                         duration=curr_screen.boss_movement_duration)
    boss_anim.bind(on_progress=partial(self.check_boss_collision, time_stamp, screen_num))
    boss_anim.bind(on_complete=partial(self.boss_wins_animation, time_stamp, screen_num))
    boss_anim.start(boss)


def boss_wins_animation(self, time_stamp, screen_num, *args):
    boss = args[1]
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]

    curr_screen.character_killed = True
    kivy.animation.Animation.cancel_all(character_image)
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        kivy.animation.Animation.cancel_all(enemy['image'])
    kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 2)


def boss_defeat_animation_start(self, boss, screen_num):
    curr_screen = self.root.screens[screen_num]
    new_pos = (curr_screen.size[0],
               curr_screen.size[1] * 0.5)
    boss_defeat_anim = kivy.animation.Animation(pos=new_pos,
                                                size_hint=(0.1, 0.1),
                                                duration=0.6)
    boss_defeat_anim.bind(on_complete=partial(self.boss_defeat_animation_finish, screen_num))
    boss_defeat_anim.start(boss)


def boss_defeat_animation_finish(self, screen_num, *args):
    boss = args[1]
    curr_screen = self.root.screens[screen_num]
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(boss)


def check_boss_collision(self, time_stamp, screen_num, *args):
    boss = args[1]
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * curr_screen.boss_width / 4
    gap_y = curr_screen.height * curr_screen.boss_height / 2
    if boss.collide_widget(character_image) and \
            abs(boss.center[0] - character_image.center[0]) <= gap_x and \
            abs(boss.center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_killed = True
        kivy.animation.Animation.cancel_all(character_image)
        kivy.animation.Animation.cancel_all(boss)
        for enemy_key, enemy in curr_screen.enemies_ids.items():
            kivy.animation.Animation.cancel_all(enemy['image'])
        kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 2)
