import random
from helper_fns import _find_kiss_endpoint_fast
import kivy.uix.image
import time
from functools import partial


def shoot_kiss(self, screen_num, touch_point):
    curr_screen = self.root.screens[screen_num]
    screen_size = curr_screen.size  # List [size_x, size_y]
    character_image_center = curr_screen.ids['character_image_lvl' + str(screen_num)].center  # List: [c_x, c_y]
    kiss_end_point = _find_kiss_endpoint_fast(character_image_center,
                                              touch_point,
                                              screen_size,
                                              self.kiss_width,
                                              self.kiss_height,
                                              self.side_bar_width)
    kiss = kivy.uix.image.Image(source="graphics/entities/kiss1.png",
                                size_hint=(self.kiss_width, self.kiss_height),
                                pos=[character_image_center[0] - self.kiss_width * screen_size[0] / 2,
                                     character_image_center[1]], allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(kiss, index=2)
    # create a unique identifier for each enemy
    time_stamp = str(time.time())
    curr_screen.kisses_ids['kiss_' + time_stamp] = kiss
    kiss_anim = kivy.animation.Animation(pos=kiss_end_point,
                                         duration=self.kiss_duration)
    kiss_anim.bind(on_progress=partial(self.check_kiss_collision, kiss, time_stamp, screen_num))
    kiss_anim.bind(on_complete=partial(self.kiss_animation_completed, kiss, time_stamp, screen_num))
    kiss_anim.start(kiss)
    self.sound_kiss.play()


def kiss_animation_completed(self, kiss, time_stamp, screen_num, *args):
    # enemy_image = args[1]
    curr_screen = kiss.parent.parent.parent
    # kivy.animation.Animation.cancel_all(kiss)
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss)
    del curr_screen.kisses_ids['kiss_' + time_stamp]


def check_kiss_collision(self, kiss, time_stamp, screen_num, *args):
    kiss_already_hit = False
    curr_screen = self.root.screens[screen_num]
    gap_x = curr_screen.width * self.enemy_width / 3
    gap_y = curr_screen.height * self.enemy_height / 3
    enemies_to_delete = []
    for enemy_key, enemy in curr_screen.enemies_ids.items():
        if not kiss_already_hit and kiss.collide_widget(enemy['image']) and \
                abs(enemy['image'].center[0] - kiss.center[0]) <= gap_x and \
                abs(enemy['image'].center[1] - kiss.center[1]) <= gap_y:
            enemy['hitpoints'] = enemy['hitpoints'] - 1
            kivy.animation.Animation.cancel_all(kiss)
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss)
            del curr_screen.kisses_ids['kiss_' + time_stamp]
            kiss_already_hit = True
            if enemy['hitpoints'] == 0:
                enemy_center = enemy['image'].center
                enemies_to_delete.append(enemy_key)
                kivy.animation.Animation.cancel_all(enemy['image'])
                curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(enemy['image'])
                # Spawn reward with probability defined per level
                if random.random() < curr_screen.enemy_spawn_reward_probability:
                    self.spawn_reward(enemy_center, screen_num)

    if len(enemies_to_delete) > 0:
        for enemy_key in enemies_to_delete:
            del curr_screen.enemies_ids[enemy_key]

    # Boss collision check
    if curr_screen.phase_1_completed and not kiss_already_hit:
        gap_x = curr_screen.width * curr_screen.boss_width / 3
        gap_y = curr_screen.height * curr_screen.boss_height / 3
        bosses_to_delete = []
        for boss_key, boss in curr_screen.bosses_ids.items():
            if kiss.collide_widget(boss['image']) and \
                    abs(boss['image'].center[0] - kiss.center[0]) <= gap_x and \
                    abs(boss['image'].center[1] - kiss.center[1]) <= gap_y:
                boss['hitpoints'] = boss['hitpoints'] - 1
                kivy.animation.Animation.cancel_all(kiss)
                curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(kiss)
                del curr_screen.kisses_ids['kiss_' + time_stamp]
                if boss['hitpoints'] == 0:
                    self.sound_level_play.stop()
                    self.sound_level_finished.play()
                    bosses_to_delete.append(boss_key)
                    boss_center = boss['image'].center
                    kivy.animation.Animation.cancel_all(boss['image'])
                    # Stop enemies animations if they exist
                    for _, enemy in curr_screen.enemies_ids.items():
                        kivy.animation.Animation.cancel_all(enemy['image'])
                    # Animate boss killing
                    self.boss_defeat_animation_start(boss['image'], screen_num)
                    # Spawn boss reward
                    self.spawn_boss_reward(boss_center, screen_num)
                    curr_screen.phase_1_completed = False
                    kivy.clock.Clock.schedule_once(partial(self.back_to_main_screen, curr_screen.parent), 6)

        if len(bosses_to_delete) > 0:
            for boss_key in bosses_to_delete:
                del curr_screen.bosses_ids[boss_key]
