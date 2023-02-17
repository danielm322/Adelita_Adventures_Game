import kivy.animation
from functools import partial
from kivy.clock import Clock


def start_character_animation(self, screen_num, touch_pos):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    # character_image.im_num = character_image.start_im_num
    char_anim = kivy.animation.Animation(
        # pos_hint={'x': (touch_pos[0] - character_image.size_hint[0] / 2),
        #           'y': touch_pos[1] - character_image.size_hint[1] / 2},
        pos=(touch_pos[0] - character_image.size[0] / 2,
             touch_pos[1] - character_image.size[1] / 2),
        duration=curr_screen.char_anim_duration
    )
    char_anim.bind(on_progress=partial(self.check_character_collision, character_image, screen_num))
    char_anim.start(character_image)


def check_character_collision(self, character_image, screen_num, *args):
    curr_screen = self.root.screens[screen_num]
    gap_x = curr_screen.width * self.reward_size / 1
    gap_y = curr_screen.height * self.reward_size / 1
    rewards_to_delete = []
    for reward_key, reward in curr_screen.rewards_ids.items():
        if character_image.collide_widget(reward) and \
                abs(character_image.center[0] - reward.center[0]) <= gap_x and \
                abs(character_image.center[1] - reward.center[1]) <= gap_y:
            rewards_to_delete.append(reward_key)
            kivy.animation.Animation.cancel_all(reward)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(reward)
            curr_screen.rewards_gathered += 1
            self.sound_reward_collected.play()
            if curr_screen.rewards_gathered == curr_screen.rewards_to_win_ph_1:
                # Stop spawning enemies
                Clock.unschedule(partial(self.spawn_enemy, screen_num))
                self.clock_spawn_enemies_variable.cancel()
                curr_screen.phase_1_completed = True
                self.spawn_boss(screen_num)
            if curr_screen.rewards_gathered > curr_screen.rewards_to_win_ph_1:
                curr_screen.rewards_gathered = curr_screen.rewards_to_win_ph_1
            curr_screen.ids['num_stars_collected_lvl' + str(screen_num)].text = str(
                curr_screen.rewards_gathered) + "/" + str(curr_screen.rewards_to_win_ph_1)

    if len(rewards_to_delete) > 0:
        for reward_key in rewards_to_delete:
            del curr_screen.rewards_ids[reward_key]
