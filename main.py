# import math
import pyglet

"""
class game:
    def __init__(self):
        self.tick = 0
        self.tickspeed = 60

        self.global_speed_increase = 1
        self.ticks_of_boost = 1
        self.gain_for_all = 1
        self.exp_gain = 1
        self.progress_bars_limit = 3
        self.progress_bars_new_delay = 1.25 * self.tickspeed
        self.progress_bars_delay = 0

        self.progress_bars = []


class progress_bar:
    def __init__(self):
        self.ROW = len(game.progress_bars)

        self.progress = 0
        self.progress_rate = 0.05
        self.progress_multi_from_level = 1
        self.level = 1
        self.resources = 0
        self.resource_gain = game.gain_for_all
        self.experience = 0
        self.experience_limit = 1
        self.boost_ticks = 0

    def tick(self):

        self.progress += round((self.progress_rate * self.progress_multi_from_level) / game.tickspeed, 3) * (2 if self.boost_ticks else 1)

        self.progress = round(self.progress, 3)

        if self.progress >= 1:
            self.resources += self.resource_gain
            if self.resources >= 10 and self.ROW > 0:
                game.progress_bars[self.ROW - 1].resources += round(math.floor(self.resources / 10) / 10, 1)
                self.resources -= round(math.floor(self.resources / 10) / 10, 1)
            self.experience += game.exp_gain
            self.progress -= 1

        game.progress_bars[self.ROW - 1].resources = round(game.progress_bars[self.ROW - 1].resources, 1)
        self.resources = round(self.resources, 1)

        if self.experience >= self.experience_limit:
            self.level += 1
            self.progress_multi_from_level += round((self.level + 3) / 100, 2)
            self.progress_multi_from_level = round(self.progress_multi_from_level, 2)
            self.experience -= self.experience_limit
            self.experience_limit = math.floor(1.4 ** self.level)
            self.boost_ticks = 60 * game.ticks_of_boost

        if self.boost_ticks > 0:
            self.boost_ticks -= 1
"""


class pyglet_window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(pyglet_window, self).__init__(*args, **kwargs)
        pyglet_window.set_minimum_size(self, 480, 360)
        pyglet_window.set_maximum_size(self, 1280, 720)
        print(pyglet_window.get_location(self))


def main():
    window = pyglet_window(480, 360, "pyglet window", resizable=True)
    pyglet.gl.glClearColor(0xc1 / 0xff, 0xd7 / 0xff, 0xee / 0xff, 1)

    label = pyglet.text.Label(text="Hello World!",
                              color=(0x00, 0x00, 0x00, 0xFF),
                              font_name="Courier",
                              font_size=36,
                              x=window.width // 2, y=window.height // 2,
                              anchor_x="center", anchor_y="center")

    @window.event
    def on_draw():
        window.clear()
        label.draw()

    pyglet.app.run()


if __name__ == "__main__":
    main()
