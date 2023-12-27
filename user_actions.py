def on_touch_down(self, touch):
    if self.is_desktop():
        return
    if touch.x < self.width / 2:
        self.curret_speed_x = self.SPEED_X
    else:
        self.curret_speed_x = -self.SPEED_X


def on_touch_up(self, touch):
    if not self.is_desktop():
        return
    self.curret_speed_x = 0


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    # print(keyboard, keycode, text, modifiers)
    if keycode[1] in ('w', 'up'):
        print(keycode[1])
    elif keycode[1] in ('s', 'down'):
        print(keycode[1])
    elif keycode[1] in ('a', 'left'):
        self.curret_speed_x = self.SPEED_X
    elif keycode[1] in ('d', 'right'):
        self.curret_speed_x = -self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    if keycode[1] in ('a', 'left'):
        self.curret_speed_x = 0
    elif keycode[1] in ('d', 'right'):
        self.curret_speed_x = 0
