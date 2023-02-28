import kivy.uix.image
import time
from functools import partial


def spawn_boss_reward(self, boss_center, screen_num):
    curr_screen = self.root.screens[screen_num]
    boss_reward = kivy.uix.image.Image(source=curr_screen.boss_props['boss_reward_image_source'],
                                       size_hint=self.boss_reward_initial_size_hint,
                                       pos=boss_center, allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(boss_reward, index=-1)
    time_stamp = str(time.time())
    curr_screen.bosses_rewards_ids['boss_reward_' + time_stamp] = boss_reward
    boss_reward_anim = kivy.animation.Animation(size_hint=(1, 1),
                                                pos=(0, 0),
                                                duration=self.boss_reward_animation_duration)
    boss_reward_anim.bind(on_complete=partial(self.boss_reward_animation_completed, time_stamp, screen_num))
    boss_reward_anim.start(boss_reward)


def boss_reward_animation_completed(self,  time_stamp, screen_num, *args):
    boss_reward = args[1]
    curr_screen = self.root.screens[screen_num]
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(boss_reward)
    del curr_screen.bosses_rewards_ids['boss_reward_' + time_stamp]
