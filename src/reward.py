import time
import kivy.uix.image
import random

rewards_properties = {
    'star': {
        'image_source': "graphics/entities/star_small.png",
        'width': 0.05,
        'height': 0.1,
        'duration': 12,  # In seconds to disappear
        # Having only two possible rewards, the next ratio is just in what proportion
        # a star will appear, and the rest of the probability will be the heart
        'probability_proportion': 0.7
    },
    'heart': {
        'image_source': "graphics/entities/heart.png",
        'width': 0.05,
        'height': 0.1,
        'duration': 10,  # In seconds to disappear
        'heal_proportion': 0.20
    }
}


def spawn_reward(self, enemy_center, screen_num):
    curr_screen = self.root.screens[screen_num]
    # Determine if the reward will be a star or a heart. If false, the reward will be a heart
    if random.random() < rewards_properties['star']['probability_proportion']:
        reward_to_spawn = 'star'
    else:
        reward_to_spawn = 'heart'
    reward = kivy.uix.image.Image(source=rewards_properties[reward_to_spawn]['image_source'],
                                  size_hint=(rewards_properties[reward_to_spawn]['width'],
                                             rewards_properties[reward_to_spawn]['height']),
                                  pos=[enemy_center[0] -
                                       rewards_properties[reward_to_spawn]['width'] * curr_screen.size[0] / 2,
                                       enemy_center[1] -
                                       rewards_properties[reward_to_spawn]['height'] * curr_screen.size[1] / 2],
                                  allow_stretch=True,
                                  keep_ratio=False)
    curr_screen.add_widget(reward, index=-1)
    # create a unique identifier for each reward
    time_stamp = str(time.time())
    curr_screen.rewards_ids['reward_' + time_stamp] = {'image': reward,
                                                       'time_elapsed': 0.0,
                                                       'type': reward_to_spawn}


def update_rewards(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        reward['time_elapsed'] += dt
        reward['image'].opacity = 1. - reward['time_elapsed'] / rewards_properties[reward['type']]['duration']
        if reward['image'].opacity <= 0:
            rewards_to_delete.append(reward_key)
            curr_screen.remove_widget(reward['image'])

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]

# def reward_animation_completed(self, reward, time_stamp, screen_num, *args):
#     # enemy_image = args[1]
#     curr_screen = reward.parent.parent.parent
#     # kivy.animation.Animation.cancel_all(kiss)
#     curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward)
#     del curr_screen.rewards_ids['reward_' + time_stamp]
