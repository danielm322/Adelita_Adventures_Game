# import random
import kivy.uix.screenmanager
from characters_dicts import main_character_dict, aux_char_1_dict, aux_char_2_dict

class Level1(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 2
    current_phase = 1
    rewards_to_win_phases = [5]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'green',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict)
    }
    boss_props = {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 25,
        'damage': 1,
        'speed': 1.5e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/diaper.png",
        'fires_back': False,
        'trajectory_type': 'linear'
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level2(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 3
    current_phase = 1
    rewards_to_win_phases = [4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'red',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'green',
            'level': 'level_2'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict)
    }
    boss_props = {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.6e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': False,
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.2,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level3(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 3
    current_phase = 1
    rewards_to_win_phases = [4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'red',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict)
    }
    boss_props = {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.3e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.2,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level4(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 3
    current_phase = 1
    rewards_to_win_phases = [5, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'blue',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict)
    }
    boss_props = {
        'width': 0.391,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.3e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.3,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level5(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 3
    current_phase = 1
    rewards_to_win_phases = [4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'purple',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'blue',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level6(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 4
    current_phase = 1
    rewards_to_win_phases = [4, 4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'red',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'purple',
            'level': 'level_1'
        }
        },
    ]
    characters_dict = {
        'character': dict(main_character_dict),
        'aux_char_2': dict(aux_char_2_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level7(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 4
    current_phase = 1
    rewards_to_win_phases = [4, 4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'orange',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'blue',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'underlings',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict),
        'aux_char_2': dict(aux_char_2_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level8(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 4
    current_phase = 1
    rewards_to_win_phases = [4, 4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'purple',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'orange',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict),
        'aux_char_1': dict(aux_char_1_dict),
        'aux_char_2': dict(aux_char_2_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level9(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 4
    current_phase = 1
    rewards_to_win_phases = [4, 4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        },
            'enemy_2': {
                'type': 'red',
                'level': 'level_1'
            }
        },
        {'enemy_1': {
            'type': 'purple',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'blue',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict),
        'aux_char_1': dict(aux_char_1_dict),
        'aux_char_2': dict(aux_char_2_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15,
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}


class Level10(kivy.uix.screenmanager.Screen):
    state_paused = False
    number_of_phases = 4
    current_phase = 1
    rewards_to_win_phases = [5, 4, 4]
    rewards_gathered = 0
    move_aux_char_1_state = False
    move_aux_char_2_state = False
    spawn_enemies_clock_variables = []
    # This list will hold enemies for either several phases and/or several enemies par phase
    enemies_phases = [
        {'enemy_1': {
            'type': 'blue',
            'level': 'level_1'
        },
            'enemy_2': {
                'type': 'red',
                'level': 'level_1'
            }
        },
        {'enemy_1': {
            'type': 'yellow',
            'level': 'level_1'
        }
        },
        {'enemy_1': {
            'type': 'orange',
            'level': 'level_1'
        }
        }
    ]
    characters_dict = {
        'character': dict(main_character_dict),
        'aux_char_1': dict(aux_char_1_dict),
        'aux_char_2': dict(aux_char_2_dict)
    }
    boss_props = {
        'width': 0.4,
        'height': 0.45,
        'hit_points': 30,
        'damage': 1.5,
        'speed': 1.0e-3,
        'source': "graphics/entities/boss_1.png",
        'boss_reward_image_source': "graphics/entities/boss_reward_key.png",
        'fires_back': True,
        'fire_type': 'fire',
        'fire_level': 'level_2',
        'trajectory_type': 'non_linear',
        'trajectory_function': 'sine',
        'amplitude': 0.15,
        'period': 15,
    }
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}
