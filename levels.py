import kivy.uix.screenmanager


class Level1(kivy.uix.screenmanager.Screen):
    phase_1_completed = False
    state_paused = False
    level_completed = False
    enemy_spawn_reward_probability = 0.15
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    character_dict = {
        'shoot_state': False,
        'killed': False,
        'speed': 5,
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
        'speed_x': -1
    }
    enemy_speed_min = 3e-4
    enemy_speed_max = 6e-4
    enemy_spawn_interval = 4  # In seconds
    rewards_gathered = 0
    rewards_to_win_ph_1 = 4
    enemy_finishes_damage = 30


class Level2(kivy.uix.screenmanager.Screen):
    phase_1_completed = False
    state_paused = False
    level_completed = False
    enemy_spawn_reward_probability = 0.13
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    character_dict = {
        'shoot_state': False,
        'killed': False,
        'speed': 5,
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
        'speed_x': -1
    }
    enemy_speed_min = 3e-4
    enemy_speed_max = 6e-4
    enemy_spawn_interval = 2.5  # In seconds
    rewards_gathered = 0
    rewards_to_win_ph_1 = 6
    enemy_finishes_damage = 30
