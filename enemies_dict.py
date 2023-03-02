enemy_types = ['green', 'red', 'yellow']

enemies_dict = {
    'green': {
        'level_1': {
            'hit_points': 6,
            'shield': 0,
            'damage': 1,
            'fires_back': False,
            # 'speed_min': 3e-4,
            'speed_min': 1,
            # 'speed_max': 6e-4,
            'speed_max': 1.3,
            'spawn_point': None,
            'end_point': None,
            'spawn_interval': 4,  # In seconds
            'finishes_damage': 30,
            'spawn_reward_probability': 0.15,
            'width': 0.15,
            'height': 0.18,
            'spawn_function': 'uniform',
            'source': "graphics/entities/enemy_green.png"
        },
        'level_2': {
            'hit_points': 6,
            'shield': 0,
            'damage': 1,
            'fires_back': False,
            'speed_min': 1.3,
            'speed_max': 1.6,
            'spawn_point': None,
            'end_point': None,
            'spawn_interval': 2.5,  # In seconds
            'finishes_damage': 30,
            'spawn_reward_probability': 0.10,
            'width': 0.15,
            'height': 0.18,
            'spawn_function': 'uniform',
            'source': "graphics/entities/enemy_green.png"
        }
    },
    'red': {
        'level_1': {
            'hit_points': 10,
            'shield': 0,
            'damage': 1,
            'fires_back': False,
            'speed_min': 0.5,
            'speed_max': 0.8,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.08,
            'spawn_interval': 2,  # In seconds
            'finishes_damage': 35,
            'spawn_reward_probability': 0.09,
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
            'damage': 1,
            'fires_back': False,
            'speed_min': 1.8,
            'speed_max': 2.1,
            'spawn_point': None,
            'end_point': None,
            'trajectory_variance': 0.15,
            'spawn_interval': 2,  # In seconds
            'finishes_damage': 20,
            'spawn_reward_probability': 0.11,
            # 'spawn_reward_probability': 11,
            'width': 0.1,
            'height': 0.13,
            'spawn_function': 'gaussian',
            'source': "graphics/entities/enemy_yellow.png"
        }
    },
    'purple': {
        'level_1': {
            'hit_points': 8,
            'shield': 0,
            'damage': 1,
            'fires_back': True,
            'speed_min': 1,
            'speed_max': 1.2,
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
    'fire': {
        'level_1': {
            'hit_points': 100,
            'shield': 0,
            'damage': 1,
            'fires_back': False,
            'speed_min': 2.4,
            'speed_max': 2.6,
            'spawn_point': None,
            'end_point': None,
            'finishes_damage': 0,
            'width': 0.05,
            'height': 0.05,
            'spawn_function': 'enemy_center',
            'source': "graphics/entities/fire.png"
        }
    }
}
