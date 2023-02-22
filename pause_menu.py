from kivy.uix.floatlayout import FloatLayout


class PauseMenuWidget(FloatLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(FloatLayout, self).on_touch_down(touch)