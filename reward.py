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
    curr_screen.rewards_ids['reward_' + time_stamp] = {'image': reward,
                                                       'time_elapsed': 0.0}
    # Animate reward to disappear
    # reward_anim = kivy.animation.Animation(opacity=0, duration=self.reward_duration)
    # reward_anim.bind(on_complete=partial(self.reward_animation_completed, reward, time_stamp, screen_num))
    # reward_anim.start(reward)


def update_rewards(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        reward['time_elapsed'] += dt
        reward['image'].opacity = 1. - reward['time_elapsed'] / self.reward_duration
        if reward['image'].opacity <= 0:
            rewards_to_delete.append(reward_key)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward['image'])

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]

# def reward_animation_completed(self, reward, time_stamp, screen_num, *args):
#     # enemy_image = args[1]
#     curr_screen = reward.parent.parent.parent
#     # kivy.animation.Animation.cancel_all(kiss)
#     curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward)
#     del curr_screen.rewards_ids['reward_' + time_stamp]
