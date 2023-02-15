import random


def get_enemy_start_end_positions(side_bar_width, enemy_width, enemy_height):
    # Choose starting side randomly: 0:left, 1:up, 2:right, 3:down
    r1_start = random.randint(0, 3)
    r2_start = random.random()
    r_finish = random.random()
    
    if r1_start == 0:  # left
        spawn_pos = {'x': side_bar_width - enemy_width, 'y': r2_start*(1-enemy_height)}
        finish_pos = {'x': 1.0, 'y': r_finish}
    elif r1_start == 1:  # up
        spawn_pos = {'x': r2_start, 'y': 1.0}
        finish_pos = {'x': r_finish, 'y': 0.0 - enemy_height}
    elif r1_start == 2:  # right
        spawn_pos = {'x': 1.0, 'y': r2_start*(1-enemy_height)}
        finish_pos = {'x': side_bar_width - enemy_width, 'y': r_finish}
    else:  # down
        spawn_pos = {'x': r2_start, 'y': 0.0 - enemy_height}
        finish_pos = {'x': r_finish, 'y': 1.0}
    return spawn_pos, finish_pos


def find_line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def find_kiss_endpoint(character_image_center, touch_point, screen_size, kiss_width, kiss_height, side_bar_width):
    # TODO might be possible to optimize the calculation of endpoints by adding a padding tolerance so that it
    #  might be not necessary to calculate a new endpoint if only a small amount of pixels above or
    #  below a threshold
    # Check direction of shooting to decide which screen boundaries to assign
    # Check up and right
    if touch_point[0] > character_image_center[0] and touch_point[1] > character_image_center[1]:
        right_line_intersection_point = find_line_intersection(
            (character_image_center, touch_point),
            ((screen_size[0], 0), (screen_size[0], screen_size[1]))
        )
        if right_line_intersection_point[1] <= screen_size[1]:
            return right_line_intersection_point
        else:  # upper line intersection
            return find_line_intersection(
                (character_image_center, touch_point),
                ((0, screen_size[1]), (screen_size[0], screen_size[1]))
            )
    # Check down and right
    elif touch_point[0] > character_image_center[0] and touch_point[1] < character_image_center[1]:
        right_line_intersection_point = find_line_intersection(
            (character_image_center, touch_point),
            ((screen_size[0], 0), (screen_size[0], screen_size[1]))
        )
        if right_line_intersection_point[1] >= 0:
            return right_line_intersection_point
        else:  # lower line intersection
            lower_line_intersection_point = find_line_intersection(
                (character_image_center, touch_point),
                ((0, 0), (screen_size[0], 0))
            )
            return lower_line_intersection_point[0], lower_line_intersection_point[1]-kiss_height*screen_size[1]
    # Check up and left
    elif touch_point[0] < character_image_center[0] and touch_point[1] > character_image_center[1]:
        left_line_intersection_point = find_line_intersection(
            (character_image_center, touch_point),
            ((0, 0), (0, screen_size[1]))
        )
        if left_line_intersection_point[1] <= screen_size[1]:
            side_bar_correction = side_bar_width*screen_size[0]-kiss_width*screen_size[0]/2
            return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
        else:  # upper line intersection
            return find_line_intersection(
                (character_image_center, touch_point),
                ((0, screen_size[1]), (screen_size[0], screen_size[1]))
            )
    # Check down and left
    else:
        left_line_intersection_point = find_line_intersection(
            (character_image_center, touch_point),
            ((0, 0), (0, screen_size[1]))
        )
        if left_line_intersection_point[1] >= 0:
            side_bar_correction = side_bar_width * screen_size[0] - kiss_width * screen_size[0] / 2
            return left_line_intersection_point[0] + side_bar_correction, left_line_intersection_point[1]
        else:  # lower line intersection
            lower_line_intersection_point = find_line_intersection(
                (character_image_center, touch_point),
                ((0, 0), (screen_size[0], 0))
            )
            return lower_line_intersection_point[0], lower_line_intersection_point[1] - kiss_height * screen_size[1]