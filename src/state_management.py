from kivy.graphics import Color, Quad


def on_special_button_state(self, widget, screen_num):
    curr_screen = self.root.screens[screen_num]
    if widget.state == "normal":
        curr_screen.characters_dict['character']['shoot_special_state'] = False
        curr_screen.canvas.remove_group(u"special_radius")
    else:
        if curr_screen.ids['kiss_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"
        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS and curr_screen.ids[
            'move_aux_char_1_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state = "normal"
        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_2_ENTERS and curr_screen.ids[
            'move_aux_char_2_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state = "normal"

        curr_screen.characters_dict['character']['shoot_special_state'] = True
        # Draw rectangle with the minimum distance to fire special
        quad_coords = self.get_special_quad_coords(screen_num)
        with curr_screen.canvas:
            Color(0, 0, 0, 0.2)
            self.special_attack_properties['quad'] = Quad(points=quad_coords, group=u"special_radius")


def on_special_triangle_button_state(self, widget, screen_num):
    curr_screen = self.root.screens[screen_num]
    if widget.state == "normal":
        curr_screen.special_triangle_state = False
        curr_screen.canvas.remove_group(u"special_triangle_shape")
    # Activate special fire triangle, which is compatible with all the other toggle button states
    else:
        curr_screen.special_triangle_state = True
        self.activate_special_fire_triangle(screen_num, widget)


def on_toggle_button_state(self, widget, screen_num):
    curr_screen = self.root.screens[screen_num]
    if widget.state == "normal":
        # widget.source = "graphics/entities/kiss1_bw.png"
        curr_screen.characters_dict['character']['shoot_state'] = False
    else:
        if screen_num > 1 and curr_screen.ids['special_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"
        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS \
                and curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state = "normal"
        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_2_ENTERS \
                and curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state = "normal"
        # widget.source = "graphics/entities/kiss1.png"
        curr_screen.characters_dict['character']['shoot_state'] = True


def on_move_aux_char_1_button(self, widget, screen_num):
    curr_screen = self.root.screens[screen_num]
    if widget.state == "normal":
        curr_screen.move_aux_char_1_state = False
        curr_screen.canvas.remove_group(u"aux_char_1_quad")
    else:
        if curr_screen.ids['special_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"

        if curr_screen.ids['kiss_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"

        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_2_ENTERS \
                and curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_2_lvl' + str(screen_num)].state = "normal"

        curr_screen.move_aux_char_1_state = True
        quad_coords = self.get_aux_char_1_quad_coords(screen_num)
        with curr_screen.canvas:
            Color(0, 0, 0, 0.2)
            self.aux_char_1_quad = Quad(points=quad_coords, group=u"aux_char_1_quad")


def on_move_aux_char_2_button(self, widget, screen_num):
    curr_screen = self.root.screens[screen_num]
    if widget.state == "normal":
        curr_screen.move_aux_char_2_state = False
    else:
        if curr_screen.ids['special_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['special_button_lvl' + str(screen_num)].state = "normal"

        if curr_screen.ids['kiss_button_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['kiss_button_lvl' + str(screen_num)].state = "normal"

        if screen_num >= self.LEVEL_WHEN_AUX_CHAR_1_ENTERS \
                and curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state == "down":
            curr_screen.ids['move_aux_char_1_lvl' + str(screen_num)].state = "normal"

        curr_screen.move_aux_char_2_state = True
