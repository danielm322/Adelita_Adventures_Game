from functools import partial
from kivy.clock import Clock
from kivy.graphics import Color, Triangle, Line

from src.helper_fns import get_triangle_borders_coords

# In seconds
SPECIAL_TRIANGLE_DURATION = 7.0
SPECIAL_TRIANGLE_RELOAD_TIME = 10.0


def activate_special_fire_triangle(self, screen_num, widget):
    curr_screen = self.root.screens[screen_num]
    sp_triangle_coords = self.get_special_triangle_coords(screen_num)
    with curr_screen.canvas:
        # Color(0.9, 0.4, 0, 0.7)  # Orange
        Color(0.3, 0.4, 0, 0.7)  # Dark green
        self.special_triangle_shape = Triangle(points=sp_triangle_coords,
                                               group=u"special_triangle_shape",
                                               # source="graphics/entities/fire-texture.jpg"
                                               )
        Color(0.5, 1, 0, 0.8)  # Flashy green
        # Color(1, 0, 0, 0.8)  # Red
        borders = get_triangle_borders_coords(sp_triangle_coords)
        self.special_triangle_border = Line(points=borders,
                                            group=u"special_triangle_shape",
                                            width=2)
    widget.disabled = True
    self.sound_thunder.play()
    # Set a counter for special triangle duration
    Clock.schedule_once(partial(self.finish_special_triangle, screen_num), SPECIAL_TRIANGLE_DURATION)


def get_special_triangle_coords(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_centers = []
    for character in curr_screen.characters_dict.values():
        character_centers.extend(curr_screen.ids[character['name'] + str(screen_num)].center)
    return tuple(character_centers)


def finish_special_triangle(self, screen_num, dt=0.0):
    # Control special triangle state for current screen here
    self.root.screens[screen_num].special_triangle_state = False
    self.root.screens[screen_num].ids['special_triangle_button_lvl' + str(screen_num)].state = 'normal'
    Clock.schedule_once(partial(self.enable_special_triangle, screen_num), SPECIAL_TRIANGLE_RELOAD_TIME)
    self.special_triangle_shape = None


def enable_special_triangle(self, screen_num, dt=0.0):
    curr_screen = self.root.screens[screen_num]
    # Do not enable if at least one character is dead
    for character in curr_screen.characters_dict.values():
        if character['is_killed']:
            return
    curr_screen.ids['special_triangle_button_lvl' + str(screen_num)].disabled = False
