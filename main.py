import math
import colour
import pyglet


invert_y = lambda y, window_height: window_height - y


def color_shift_math(initial_color_hue, level):
    hue = initial_color_hue - (level-1) * 9
    sat = 10 + (level**0.85) * 3
    sat = (100 if sat > 100 else sat)
    light = 50
    print(hue, sat, light, colour.Color(hsl=(hue/360, sat/100, light/100)))
    return colour.Color(hsl=(hue/360, sat/100, light/100))
    pass


class game:
    def __init__(self):
        self.tick = 0
        self.tickspeed = 60

        self.global_speed_increase = 1
        self.ticks_of_boost = 1
        self.gain_for_all = 1
        self.exp_gain = 1
        self.progress_bars_limit = 4
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

        self.initial_color_hue = 180

        self.color = color_shift_math(self.initial_color_hue, self.level)

        self.label = pyglet.text.Label(text="w",
                                       font_name="Courier",
                                       font_size=10,
                                       color=(0x00, 0x00, 0x00, 0xFF),
                                       x=0, y=invert_y(20*self.ROW, 720),
                                       anchor_x="left", anchor_y="top")

        self.graphics = [
            pyglet.text.Label(
                text=f"#{self.ROW+1}",
                font_name="Arial",
                font_size=12,
                color=(0x00, 0x00, 0x00, 0xFF),
                x=20, y=invert_y(20*(self.ROW+2), 720),
                anchor_x="left", anchor_y="bottom"
            ),
            pyglet.shapes.Rectangle(
                x=50, y=invert_y(20*(self.ROW+2), 720),
                width=720-50, height=20,
                color=(0x00, 0x00, 0x00)
            ),
            pyglet.shapes.Rectangle(
                x=50, y=invert_y(20*(self.ROW+2) - 4, 720),
                width=self.progress*(720-50), height=20-8,
                color=[int(x*255) for x in self.color.get_rgb()]
            )
        ]

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
            self.color = color_shift_math(self.initial_color_hue, self.level)
            self.graphics[2].color = [int(x*255) for x in self.color.get_rgb()]

        if self.boost_ticks > 0:
            self.boost_ticks -= 1


class pyglet_window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(pyglet_window, self).__init__(*args, **kwargs)
        pyglet_window.set_minimum_size(self, 1280, 720)
        pyglet_window.set_maximum_size(self, 1920, 1080)
        print(pyglet_window.get_location(self))


def main():
    # game init
    global game
    game = game()

    def tick(*_):
        if game.progress_bars_delay > 0:
            game.progress_bars_delay -= 1

        if len(game.progress_bars) < game.progress_bars_limit and not game.progress_bars_delay:
            game.progress_bars.append(progress_bar())
            game.progress_bars_delay += round(game.progress_bars_new_delay)

        for bar in game.progress_bars:
            bar.label.text = f"row: {bar.ROW}, {bar.progress}{'00' if len(str(bar.progress))<4 else '0' if len(str(bar.progress))<5 else ''}/1.000, resources: {bar.resources}, experience: {bar.experience}/{bar.experience_limit}, level: {bar.level}, boost: {bar.boost_ticks}, speed = {bar.progress_multi_from_level}"
            bar.tick()
            bar.graphics[2].width = bar.progress * (720-50)
            if bar.boost_ticks:
                bar.graphics[1].color = (0x79, 0x69, 0x14)
            else:
                bar.graphics[1].color = (0x00, 0x00, 0x00)

    pyglet.clock.schedule_interval(tick, 1/game.tickspeed)

    # graphics init
    window = pyglet_window(1280, 720, "pyglet window", resizable=True)
    pyglet.gl.glClearColor(0xc1 / 0xff, 0xd7 / 0xff, 0xee / 0xff, 1)

    @window.event
    def on_resize(_width, height):
        for bar in game.progress_bars:
            for index, item in enumerate(bar.graphics):
                item.y = invert_y(20*(bar.ROW+2), height)
                if index == 2:
                    item.y += 4

    @window.event
    def on_draw():
        # will add resize code here to make it more stable
        window.clear()
        for bar in game.progress_bars:
            for item in bar.graphics:
                item.draw()

    pyglet.app.run()


if __name__ == "__main__":
    main()
