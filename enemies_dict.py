enemy_types = ['green', 'red', 'yellow']

enemies_dict = {
    'green': {
        'level_1': {
            'hit_points': 6,
            'shield': 0,
            'damage': 0.3,
            'speed_min': 1e-3,
            'speed_max': 1.5e-3,
            'spawn_point': None,
            'end_point': None,
            'spawn_interval': 4,  # In seconds
            'finishes_damage': 30,
            'spawn_reward_probability': 0.15,
            'width': 0.156,  # 0.869 aspect ratio wrt height
            'height': 0.18,
            'spawn_function': 'uniform',
            'source': "graphics/entities/enemy_green.png"
        },
        'level_2': {
            'hit_points': 6,
            'shield': 0,
            'damage': 0.3,
            'speed_min': 1.3e-3,
            'speed_max': 1.8e-3,
            'spawn_point': None,
            'end_point': None,
            'spawn_interval': 2.5,  # In seconds
            'finishes_damage': 30,
            'spawn_reward_probability': 0.15,
            'width': 0.156,
            'height': 0.18,
            'spawn_function': 'uniform',
            'source': "graphics/entities/enemy_green_2.png"
        }
    },
    'red': {
        'level_1': {
            'hit_points': 10,
            'shield': 0,
            'damage': 0.5,
            'speed_min': 0.7e-3,
            'speed_max': 0.9e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.08,
            'spawn_interval': 2,  # In seconds
            'finishes_damage': 35,
            'spawn_reward_probability': 0.10,
            # 'spawn_reward_probability': 9,
            'width': 0.2,
            'height': 0.23,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_red.png"
        }
    },
    'yellow': {
        'level_1': {
            'hit_points': 3,
            'shield': 0,
            'damage': 0.2,
            'speed_min': 2e-3,
            'speed_max': 2.3e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.08,
            'spawn_interval': 2,  # In seconds
            'finishes_damage': 20,
            'spawn_reward_probability': 0.11,
            # 'spawn_reward_probability': 11,
            'width': 0.113,
            'height': 0.13,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_yellow.png"
        }
    },
    'purple': {
        'level_1': {
            'hit_points': 8,
            'shield': 0,
            'damage': 0.3,
            'fires_back': True,
            'speed_min': 0.7e-3,
            'speed_max': 1.2e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.12,
            'spawn_interval': 2.5,  # In seconds
            'finishes_damage': 20,
            # 'spawn_reward_probability': 11,
            'spawn_reward_probability': 0.11,
            'width': 0.13,
            'height': 0.15,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_purple.png"
        }
    },
    'blue': {
        'level_1': {
            'hit_points': 4,
            'shield': 0,
            'damage': 0.3,
            'splits_in_half': True,
            'split_distance': 0.10,  # In screen height proportion
            'underlings_level': 'level_1',
            'speed_min': 0.7e-3,
            'speed_max': 1.2e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.10,
            'spawn_interval': 3.0,  # In seconds
            'finishes_damage': 20,
            # 'spawn_reward_probability': 11,
            'spawn_reward_probability': 0.11,
            'width': 0.173,
            'height': 0.20,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_blue.png"
        },
    },
    'orange': {
        'level_1': {
            'hit_points': 8,
            'shield': 0,
            'damage': 10,
            'launches_character': True,
            'character_y_displacement': 0.4,
            'speed_min': 0.7e-3,
            'speed_max': 1.2e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.10,
            'spawn_interval': 3.0,  # In seconds
            'finishes_damage': 20,
            # 'spawn_reward_probability': 11,
            'spawn_reward_probability': 0.11,
            'width': 0.173,
            'height': 0.20,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_orange.png"
        },
    },
    'underlings': {
        'level_1': {
            'hit_points': 2,
            'shield': 0,
            'damage': 0.2,
            'speed_min': 2.3e-3,
            'speed_max': 2.5e-3,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.07,
            'spawn_interval': 0.9,  # In seconds
            'finishes_damage': 10,
            # 'spawn_reward_probability': 11,
            'spawn_reward_probability': 0.11,
            'width': 0.097,
            'height': 0.12,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_blue_clear.png"
        }
    },
    'fire': {
        'level_1': {
            'hit_points': 100,
            'shield': 0,
            'damage': 5,
            'speed_min': 2.5e-3,
            'speed_max': 2.7e-3,
            'spawn_point': None,
            'end_point': None,
            'finishes_damage': 0,
            'width': 0.02,
            'height': 0.05,
            'spawn_function': 'enemy_center',
            'source': "graphics/entities/fire.png"
        },
        'level_2': {
            'hit_points': 100,
            'shield': 0,
            'damage': 10,
            'speed_min': 3.9e-3,
            'speed_max': 4.2e-3,
            'spawn_point': None,
            'end_point': None,
            'finishes_damage': 0,
            'width': 0.04,
            'height': 0.08,
            'spawn_function': 'enemy_center',
            'source': "graphics/entities/fire.png"
        }
    }
}
