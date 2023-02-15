import time
import kivy.uix.image
from functools import partial

def spawn_reward(self, enemy_center, screen_num):
    curr_screen = self.root.screens[screen_num]
    reward = kivy.uix.image.Image(source="graphics/entities/star_small.png",
                                  size_hint=(self.reward_size, self.reward_size),
                                  pos=[enemy_center[0] - self.reward_size * curr_screen.size[0] / 2,
                                       enemy_center[1] - self.reward_size * curr_screen.size[1] / 2],
                                  allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(reward, index=-1)
    # create a unique identifier for each reward
    time_stamp = str(time.time())
    curr_screen.rewards_ids['reward_' + time_stamp] = reward
    # Animate reward to disappear
    reward_anim = kivy.animation.Animation(opacity=0, duration=self.reward_duration)
    reward_anim.bind(on_complete=partial(self.reward_animation_completed, reward, time_stamp, screen_num))
    reward_anim.start(reward)

def reward_animation_completed(self, reward, time_stamp, screen_num, *args):
    # enemy_image = args[1]
    curr_screen = reward.parent.parent.parent
    # kivy.animation.Animation.cancel_all(kiss)
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward)
    del curr_screen.rewards_ids['reward_' + time_stamp]
