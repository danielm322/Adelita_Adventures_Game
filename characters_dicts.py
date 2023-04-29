main_character_dict = {
    'name': 'character_image_lvl',
    'life_bar_id': 'remaining_life_percent_lvl',
    'shoot_state': False,
    'shoot_special_state': False,
    'current_state': 'idle',
    'is_moving': False,
    'is_killed': False,
    'is_fighting': False,
    'hit_points': 80,
    'damage_received': 0,
    'finish_point_pos': (0., 0.),
    'direction_unit_vector': (0., 0.),
    'speed': None,
    'melee_attacks': False,
    'is_idle_image_counter': 1.0,
    'is_walking_image_counter': 1.0,
    'has_idle_state_animation': True,
    'has_walking_state_animation': True,
    'walking_images_file_names': 'graphics/entities/Enchantress/Run_',
    'idle_images_file_names': 'graphics/entities/Enchantress/Idle_',
    'number_of_walking_images': 8,
    'number_of_idle_images': 5,
    'walking_animation_speed': 0.3,
    'idle_animation_speed': 0.1
}

aux_char_1_dict = {
    'name': 'aux_char_1_image_lvl',
    'life_bar_id': 'remaining_life_percent_aux_char_1_lvl',
    'shoot_special_state': False,
    'current_state': 'idle',
    'is_moving': False,
    'is_killed': False,
    'is_fighting': False,
    'hit_points': 80,
    'damage_received': 0,
    'finish_point_pos': (0, 0),
    'direction_unit_vector': (0, 0),
    'speed': None,
    'melee_attacks': False,
    'has_idle_state_animation': False,
    'has_walking_state_animation': False,
}

aux_char_2_dict = {
    'name': 'aux_char_2_image_lvl',
    'life_bar_id': 'remaining_life_percent_aux_char_2_lvl',
    'shoot_special_state': False,
    'current_state': 'idle',
    'is_moving': False,
    'is_killed': False,
    'is_fighting': False,
    'hit_points': 200,
    'damage_received': 0,
    'finish_point_pos': (0, 0),
    'direction_unit_vector': (0, 0),
    'speed': None,
    'melee_attacks': True,
    'melee_damage': 0.1,
    'is_fighting_image_counter': 1.0,
    'is_walking_image_counter': 1.0,
    'has_idle_state_animation': False,
    'has_walking_state_animation': True,
    'walking_images_file_names': 'graphics/entities/BadKidUdo/BadKidUno-walk',
    'melee_attack_file_names': 'graphics/entities/BadKidUdo/BadKidUno-attack',
    'number_of_walking_images': 9,
    'number_of_fight_images': 8,
    'walking_animation_speed': 0.3,
    'fighting_animation_speed': 0.4
}

character_states_to_images = {
    'idle': {
        'counter': 'is_idle_image_counter',
        'file_names': 'idle_images_file_names',
        'number_of_images': 'number_of_idle_images',
        'animation_speed': 'idle_animation_speed'
    },
    'walking': {
        'counter': 'is_walking_image_counter',
        'file_names': 'walking_images_file_names',
        'number_of_images': 'number_of_walking_images',
        'animation_speed': 'walking_animation_speed'
    },
    'melee_attacking': {
        'counter': 'is_fighting_image_counter',
        'file_names': 'melee_attack_file_names',
        'number_of_images': 'number_of_fight_images',
        'animation_speed': 'fighting_animation_speed'
    },
}
