import kivy.uix.screenmanager
from characters_dicts import main_character_dict, aux_char_1_dict, aux_char_2_dict
from boss import boss_properties


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
    boss_props = dict(boss_properties['level_1'])
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
    boss_props = dict(boss_properties['level_2'])

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
    boss_props = dict(boss_properties['level_3'])
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
    boss_props = dict(boss_properties['level_4'])
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
    boss_props = dict(boss_properties['level_4'])
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
    boss_props = dict(boss_properties['level_6'])
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
    boss_props = dict(boss_properties['level_6'])
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
    boss_props = dict(boss_properties['level_6'])
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
    boss_props = dict(boss_properties['level_6'])
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
    boss_props = dict(boss_properties['level_6'])
    # Entities Ids dicts to be used during gameplay
    kisses_ids = {}
    rewards_ids = {}
    enemies_ids = {}
    bosses_ids = {}
    bosses_rewards_ids = {}
    specials_ids = {}
