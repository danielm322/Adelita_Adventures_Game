import random


def _get_enemy_start_end_positions(side_bar_width: float, enemy_width: float, enemy_height: float):
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
    spawn_pos = {'x': 1.0, 'y': r_start*(1-enemy_height)}
    finish_pos = {'x': side_bar_width - enemy_width, 'y': r_finish*(1-enemy_height)}
    return spawn_pos, finish_pos


def _get_red_enemy_start_end_positions(side_bar_width: float,
                                       red_enemy_spawn_point: float,
                                       red_enemy_end_point: float,
                                       red_enemy_trajectory_variance: float,
                                       enemy_width: float,
                                       enemy_height: float):
    """
    Enemies start always from the right, and finish always on the left, this function
    chooses randomly start and end points
    :param side_bar_width:
    :param enemy_width:
    :param enemy_height:
    :return:
    """
    r_start = random.gauss(red_enemy_spawn_point, red_enemy_trajectory_variance)
    r_finish = random.gauss(red_enemy_end_point, red_enemy_trajectory_variance)
    spawn_pos = {'x': 1.0, 'y': r_start*(1-enemy_height)}
    finish_pos = {'x': side_bar_width - enemy_width, 'y': r_finish*(1-enemy_height)}
    return spawn_pos, finish_pos


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


def find_line_intersection_fast(line_slope: float, line_intercept: float, screen_size: tuple, border: str):
    if line_slope == 0:
        line_slope = 1e-6
    if border == 'up':
        return (screen_size[1] - line_intercept) / line_slope, screen_size[1]
    elif border == 'down':
        return - line_intercept / line_slope, 0.0
    elif border == 'right':
        return screen_size[0], line_slope * screen_size[0] + line_intercept
    else:  # left
        return 0.0, line_intercept


def _find_kiss_endpoint_fast(character_image_center, touch_point, screen_size, kiss_width, kiss_height, side_bar_width):
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
            line_slope, line_intercept, screen_size, 'left'
        )
        if left_line_intersection_point[1] <= screen_size[1]:
            side_bar_correction_x = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
            side_bar_correction_y = - kiss_height * screen_size[1] / 2
            return left_line_intersection_point[0] + side_bar_correction_x, left_line_intersection_point[1] + side_bar_correction_y
        else:  # upper line intersection
            return find_line_intersection_fast(
                line_slope, line_intercept, screen_size, 'up'
            )
    # Check down and left
    else:
        left_line_intersection_point = find_line_intersection_fast(
            line_slope, line_intercept, screen_size, 'left'
        )
        if left_line_intersection_point[1] >= 0:
            side_bar_correction = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
            return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
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
