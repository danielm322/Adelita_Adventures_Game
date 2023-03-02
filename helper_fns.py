import random
from math import sqrt
from os import path, getcwd
from os.path import join
from enemies_dict import enemies_dict

from kivy.utils import platform
if platform == "android":
    # from android.storage import primary_external_storage_path
    from android.storage import app_storage_path


def _get_enemy_start_end_positions(side_bar_width, enemy_type, enemy_level, screen_size):
    spawn_function = enemies_dict[enemy_type][enemy_level]['spawn_function']
    if spawn_function == 'uniform':
        return _get_uniform_enemy_start_end_positions(
            side_bar_width,
            enemies_dict[enemy_type][enemy_level]['width'],
            enemies_dict[enemy_type][enemy_level]['height'],
            screen_size
        )
    elif spawn_function == 'gaussian':
        return _get_gaussian_enemy_start_end_positions(
            side_bar_width,
            enemies_dict[enemy_type][enemy_level]['spawn_point'],
            enemies_dict[enemy_type][enemy_level]['end_point'],
            enemies_dict[enemy_type][enemy_level]['trajectory_variance'],
            enemies_dict[enemy_type][enemy_level]['width'],
            enemies_dict[enemy_type][enemy_level]['height'],
            screen_size
        )


def _get_uniform_enemy_start_end_positions(side_bar_width: float,
                                           enemy_width: float,
                                           enemy_height: float,
                                           screen_size: tuple) -> tuple:
    """
    Enemies start always from the right, and finish always on the left, this function
    chooses randomly start and end points
    :param side_bar_width:
    :param enemy_width:
    :param enemy_height:
    :return:
    """
    r_start = random.random()
    r_finish = random.random()
    start_pos_hint = {'x': 1.0, 'y': r_start * (1 - enemy_height)}
    finish_pos_hint = {'x': side_bar_width - enemy_width / 2, 'y': r_finish * (1 - enemy_height)}
    start_pos = [0, 0]
    finish_pos = [0, 0]
    start_pos[0], start_pos[1] = start_pos_hint['x'] * screen_size[0], start_pos_hint['y'] * screen_size[1]
    finish_pos[0], finish_pos[1] = finish_pos_hint['x'] * screen_size[0], \
                                   finish_pos_hint['y'] * screen_size[1]
    return start_pos, finish_pos
    # return start_pos_hint, finish_pos_hint


def _get_gaussian_enemy_start_end_positions(side_bar_width: float,
                                            gaussian_enemy_spawn_point: float,
                                            gaussian_enemy_end_point: float,
                                            gaussian_enemy_trajectory_variance: float,
                                            enemy_width: float,
                                            enemy_height: float,
                                            screen_size: tuple) -> tuple:
    """
    Enemies start always from the right, and finish always on the left, this function
    chooses randomly start and end points
    :param side_bar_width:
    :param enemy_width:
    :param enemy_height:
    :return:
    """
    r_start = random.gauss(gaussian_enemy_spawn_point, gaussian_enemy_trajectory_variance)
    r_finish = random.gauss(gaussian_enemy_end_point, gaussian_enemy_trajectory_variance)
    start_pos_hint = {'x': 1.0, 'y': r_start * (1 - enemy_height)}
    finish_pos_hint = {'x': side_bar_width - enemy_width / 2, 'y': r_finish * (1 - enemy_height)}
    start_pos = [0, 0]
    finish_pos = [0, 0]
    start_pos[0], start_pos[1] = start_pos_hint['x'] * screen_size[0], start_pos_hint['y'] * screen_size[1]
    finish_pos[0], finish_pos[1] = finish_pos_hint['x'] * screen_size[0], \
                                   finish_pos_hint['y'] * screen_size[1]
    return start_pos, finish_pos


def _get_line_slope_intercept(spawn_pos, finish_pos):
    divisor = (finish_pos['x'] - spawn_pos['x'])
    if divisor == 0:
        divisor = 1e-6
    line_slope = (finish_pos['y'] - spawn_pos['y']) / divisor
    line_intercept = spawn_pos['y'] - spawn_pos['x'] * line_slope
    return line_slope, line_intercept


# def find_line_intersection(line1, line2):
#     xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#     ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
#
#     def det(a, b):
#         return a[0] * b[1] - a[1] * b[0]
#
#     div = det(xdiff, ydiff)
#     if div == 0:
#         raise Exception('lines do not intersect')
#
#     d = (det(*line1), det(*line2))
#     x = det(d, xdiff) / div
#     y = det(d, ydiff) / div
#     return x, y


def find_line_intersection_fast(line_slope: float,
                                line_intercept: float,
                                screen_size: tuple,
                                border: str,
                                *args) -> tuple:
    '''

    :param line_slope:
    :param line_intercept:
    :param screen_size:
    :param border:
    :param args: Optionally contains the sidebar width and the kiss width
    :return:
    '''
    # Args will contain the sidebar width, as optional argument when finish point is on the left
    if line_slope == 0:
        line_slope = 1e-6
    if border == 'up':
        return (screen_size[1] - line_intercept) / line_slope, screen_size[1]
    elif border == 'down':
        return - line_intercept / line_slope, 0.0
    elif border == 'right':
        return screen_size[0], line_slope * screen_size[0] + line_intercept
    else:  # left
        return (args[0] - args[1]/2) * screen_size[0], line_slope * (args[0] - args[1]/2) * screen_size[0] + line_intercept


def _find_kiss_endpoint_fast(character_image_center, touch_point, screen_size, kiss_width, kiss_height, side_bar_width):
    """
    This function takes as arguments the character image center, and the touch point to calculate a
    straight line equation and then calculate the intercepts with the screen borders, which constitute the
    finish point of the shot rockets (kisses)
    :param character_image_center: Tuple, center of character image
    :param touch_point:
    :param screen_size:
    :param kiss_width:
    :param kiss_height:
    :param side_bar_width:
    :return:
    """
    divisor = (touch_point[0] - character_image_center[0])
    if divisor == 0:
        divisor = 1e-6
    line_slope = (touch_point[1] - character_image_center[1]) / divisor
    line_intercept = character_image_center[1] - character_image_center[0] * line_slope
    # Check direction of shooting to decide which screen boundaries to assign
    # Check up and right
    if touch_point[0] > character_image_center[0] and touch_point[1] > character_image_center[1]:
        right_line_intersection_point = find_line_intersection_fast(
            line_slope, line_intercept, screen_size, 'right'
        )
        if right_line_intersection_point[1] <= screen_size[1]:
            return right_line_intersection_point
        else:  # upper line intersection
            return find_line_intersection_fast(
                line_slope, line_intercept, screen_size, 'up'
            )
    # Check down and right
    elif touch_point[0] > character_image_center[0] and touch_point[1] < character_image_center[1]:
        right_line_intersection_point = find_line_intersection_fast(
            line_slope, line_intercept, screen_size, 'right'
        )
        if right_line_intersection_point[1] >= 0:
            return right_line_intersection_point
        else:  # lower line intersection
            lower_line_intersection_point = find_line_intersection_fast(
                line_slope, line_intercept, screen_size, 'down'
            )
            return lower_line_intersection_point[0], lower_line_intersection_point[1] - kiss_height * screen_size[1]
    # Check up and left
    elif touch_point[0] < character_image_center[0] and touch_point[1] > character_image_center[1]:
        left_line_intersection_point = find_line_intersection_fast(
            line_slope, line_intercept, screen_size, 'left', side_bar_width, kiss_width
        )
        if left_line_intersection_point[1] <= screen_size[1]:
            # side_bar_correction_x = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
            # side_bar_correction_y = - kiss_height * screen_size[1] / 2
            # return left_line_intersection_point[0] + side_bar_correction_x, left_line_intersection_point[
            #     1] + side_bar_correction_y
            return left_line_intersection_point
        else:  # upper line intersection
            return find_line_intersection_fast(
                line_slope, line_intercept, screen_size, 'up'
            )
    # Check down and left
    else:
        left_line_intersection_point = find_line_intersection_fast(
            line_slope, line_intercept, screen_size, 'left', side_bar_width, kiss_width
        )
        if left_line_intersection_point[1] >= 0:
            # side_bar_correction = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
            # return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
            return left_line_intersection_point
        else:  # lower line intersection
            lower_line_intersection_point = find_line_intersection_fast(
                line_slope, line_intercept, screen_size, 'down'
            )
            return lower_line_intersection_point[0], lower_line_intersection_point[1] - kiss_height * screen_size[1]


# def find_kiss_endpoint(character_image_center, touch_point, screen_size, kiss_width, kiss_height, side_bar_width):
#     # Check direction of shooting to decide which screen boundaries to assign
#     # Check up and right
#     if touch_point[0] > character_image_center[0] and touch_point[1] > character_image_center[1]:
#         right_line_intersection_point = find_line_intersection(
#             (character_image_center, touch_point),
#             ((screen_size[0], 0), (screen_size[0], screen_size[1]))
#         )
#         if right_line_intersection_point[1] <= screen_size[1]:
#             return right_line_intersection_point
#         else:  # upper line intersection
#             return find_line_intersection(
#                 (character_image_center, touch_point),
#                 ((0, screen_size[1]), (screen_size[0], screen_size[1]))
#             )
#     # Check down and right
#     elif touch_point[0] > character_image_center[0] and touch_point[1] < character_image_center[1]:
#         right_line_intersection_point = find_line_intersection(
#             (character_image_center, touch_point),
#             ((screen_size[0], 0), (screen_size[0], screen_size[1]))
#         )
#         if right_line_intersection_point[1] >= 0:
#             return right_line_intersection_point
#         else:  # lower line intersection
#             lower_line_intersection_point = find_line_intersection(
#                 (character_image_center, touch_point),
#                 ((0, 0), (screen_size[0], 0))
#             )
#             return lower_line_intersection_point[0], lower_line_intersection_point[1]-kiss_height*screen_size[1]
#     # Check up and left
#     elif touch_point[0] < character_image_center[0] and touch_point[1] > character_image_center[1]:
#         left_line_intersection_point = find_line_intersection(
#             (character_image_center, touch_point),
#             ((0, 0), (0, screen_size[1]))
#         )
#         if left_line_intersection_point[1] <= screen_size[1]:
#             side_bar_correction = side_bar_width*screen_size[0]-kiss_width*screen_size[0]/2
#             return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
#         else:  # upper line intersection
#             return find_line_intersection(
#                 (character_image_center, touch_point),
#                 ((0, screen_size[1]), (screen_size[0], screen_size[1]))
#             )
#     # Check down and left
#     else:
#         left_line_intersection_point = find_line_intersection(
#             (character_image_center, touch_point),
#             ((0, 0), (0, screen_size[1]))
#         )
#         if left_line_intersection_point[1] >= 0:
#             side_bar_correction = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
#             return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
#         else:  # lower line intersection
#             lower_line_intersection_point = find_line_intersection(
#                 (character_image_center, touch_point),
#                 ((0, 0), (screen_size[0], 0))
#             )
#             return lower_line_intersection_point[0], lower_line_intersection_point[1] - kiss_height * screen_size[1]


def adjust_character_life_bar(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    damage_percent = float(curr_screen.character_dict['damage_received']) / float(
        curr_screen.character_dict['hit_points'])
    remaining_life_percent_lvl_widget = curr_screen.ids['remaining_life_percent_lvl' + str(screen_num)]
    remaining_life_size_hint_y = remaining_life_percent_lvl_widget.remaining_life_size_hint_y
    remaining_life_percent_lvl_widget.size_hint = \
        (
            remaining_life_percent_lvl_widget.size_hint[0],
            remaining_life_size_hint_y - remaining_life_size_hint_y * damage_percent
        )


def calc_parabola_vertex(p1, p2, p3):
    '''
    Adapted and modifed to get the unknowns for defining a parabola:
    http://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
    '''
    x1, y1, x2, y2, x3, y3 = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
    denom = (x1 - x2) * (x1 - x3) * (x2 - x3);
    A = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom;
    B = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom;
    C = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom;

    return A, B, C


def get_direction_unit_vector(start_pos, finish_pos):
    # Check if we are getting a dictionary of pos_hints, and if that's the case,
    # convert them to lists
    if isinstance(start_pos, dict) and isinstance(finish_pos, dict):
        temp_start_pos, temp_finish_pos = [0, 0], [0, 0]
        temp_start_pos[0], temp_start_pos[1] = start_pos['x'], start_pos['y']
        temp_finish_pos[0], temp_finish_pos[1] = finish_pos['x'], finish_pos['y']
        start_pos, finish_pos = temp_start_pos, temp_finish_pos

    enemy_unit_vector_norm = sqrt(
        (finish_pos[0] - start_pos[0]) ** 2 + (finish_pos[1] - start_pos[1]) ** 2
    )
    return ((finish_pos[0] - start_pos[0]) / enemy_unit_vector_norm,
            (finish_pos[1] - start_pos[1]) / enemy_unit_vector_norm)


def read_game_info(platform):
    if platform == 'android':
        base_path = app_storage_path()  # Android
    elif platform in ('linux', 'win', 'macosx'):
        base_path = getcwd()  # PC
    file_path = join(base_path, 'levels.txt')

    if not path.exists(file_path):
        file = open(file_path, "w")
        file.write('1')
        file.close()
        return 1
    else:
        file = open(file_path, "r")
        next_level = int(file.read())
        file.close()
        return next_level


def write_level_passed(platform, screen_num):
    if platform == 'android':
        base_path = app_storage_path()  # Android
    elif platform in ('linux', 'win', 'macosx'):
        base_path = getcwd()  # PC
    file_path = join(base_path, 'levels.txt')
    with open(file_path, "r") as file:
        next_level_file = int(file.read())
    # Prevent regressing if level is already passed
    if next_level_file == screen_num:
        with open(file_path, "w") as file:
            file.write(str(screen_num + 1))

