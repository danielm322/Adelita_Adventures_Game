import random
import kivy.uix.screenmanager


class Level1(kivy.uix.screenmanager.Screen):
    number_of_phases = 2
    phase_1_completed = False
    state_paused = False
    # level_completed = False
    rewards_gathered = 0
    rewards_to_win_ph_1 = 4
    enemy_phase_1 = {
        'type': 'green',
        'level': 'level_1'
    }
    character_dict = {
        'shoot_state': False,
        'shoot_special_state': False,
        'killed': False,
        'speed': 7,
        'hit_points': 100,
        'damage_received': 0,
        'is_moving': False,
        'finish_point_pos': (0., 0.),
        'direction_unit_vector': (0., 0.)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 25,
        'damage': 20,
        'speed_x': -1,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/diaper.png"
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level2(kivy.uix.screenmanager.Screen):
    number_of_phases = 2
    phase_1_completed = False
    state_paused = False
    # level_completed = False
    rewards_gathered = 0
    rewards_to_win_ph_1 = 6
    enemy_phase_1 = {
        'type': 'green',
        'level': 'level_2'
    }
    character_dict = {
        'shoot_state': False,
        'shoot_special_state': False,
        'killed': False,
        'speed': 7,
        'hit_points': 100,
        'damage_received': 0,
        'is_moving': False,
        'finish_point_pos': (0., 0.),
        'direction_unit_vector': (0., 0.)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 20,
        'speed_x': -1.5,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png"
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level3(kivy.uix.screenmanager.Screen):
    number_of_phases = 2
    phase_1_completed = False
    state_paused = False
    # level_completed = False
    rewards_gathered = 0
    rewards_to_win_ph_1 = 6
    enemy_phase_1 = {
        'type': 'red',
        'level': 'level_1'
    }
    character_dict = {
        'shoot_state': False,
        'shoot_special_state': False,
        'killed': False,
        'speed': 7,
        'hit_points': 100,
        'damage_received': 0,
        'is_moving': False,
        'finish_point_pos': (0., 0.),
        'direction_unit_vector': (0., 0.)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 20,
        'speed_x': -1.5,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png"
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level4(kivy.uix.screenmanager.Screen):
    number_of_phases = 2
    phase_1_completed = False
    state_paused = False
    # level_completed = False
    rewards_gathered = 0
    rewards_to_win_ph_1 = 6
    enemy_phase_1 = {
        'type': 'yellow',
        'level': 'level_1'
    }
    character_dict = {
        'shoot_state': False,
        'shoot_special_state': False,
        'killed': False,
        'speed': 7,
        'hit_points': 100,
        'damage_received': 0,
        'is_moving': False,
        'finish_point_pos': (0., 0.),
        'direction_unit_vector': (0., 0.)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 20,
        'speed_x': -1.5,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png"
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level5(kivy.uix.screenmanager.Screen):
    number_of_phases = 3
    phase_1_completed = False
    phase_2_completed = False
    state_paused = False
    # level_completed = False
    rewards_gathered = 0
    rewards_to_win_ph_1 = 4
    rewards_to_win_ph_2 = 4
    enemy_phase_1 = {
        'type': 'purple',
        'level': 'level_1'
    }
    enemy_phase_2 = {
        'type': 'red',
        'level': 'level_1'
    }
    character_dict = {
        'shoot_state': False,
        'shoot_special_state': False,
        'killed': False,
        'speed': 7,
        'hit_points': 100,
        'damage_received': 0,
        'is_moving': False,
        'finish_point_pos': (0., 0.),
        'direction_unit_vector': (0., 0.)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 20,
        'speed_x': -1.5,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png"
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}
