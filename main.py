import sys
import math
import pygame
from pygame.locals import *


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


game = game()


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


pygame.init()

window_size = [480, 360]
window = pygame.display.set_mode(window_size)  # once to-do fixed in line 88 add RESIZABLE
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)


def update_fps(fps):
    text_color = "green" if fps > 30 else "yellow" if fps > 10 else "red"
    fps_text = font.render(str(fps), 1, pygame.Color(text_color))
    return fps_text

# print(pygame.display.get_wm_info())

while 1:
    events = pygame.event.get()
    current_fps = round(float(clock.get_fps()), 2)
    for event in events:
        if event.type == VIDEORESIZE:
            pass
        """
            window_size = event.size
            pygame.display.set_mode(window_size, RESIZABLE, 32)
            print(window_size)
        """
        # TODO: fix window having height incremented when resizing window
        # idea: get window position and cursor position to calculate size
        if event.type == QUIT:
            print("exit: QUIT event type")
            sys.exit(0)

    window.fill((0xc1, 0xd7, 0xee))

    if current_fps:
        # print(f"fps: {fps}")
        window.blit(update_fps(current_fps), (0, 0))

        if game.progress_bars_delay > 0:
            game.progress_bars_delay -= 1

        if len(game.progress_bars) < game.progress_bars_limit and not game.progress_bars_delay:
            game.progress_bars.append(progress_bar())
            game.progress_bars_delay += round(game.progress_bars_new_delay)

        for bar in game.progress_bars:
            bar.tick()
            # print(f"row: {bar.ROW}, {bar.progress}/1.000, resources: {bar.resources}, experience: {bar.experience}/{bar.experience_limit}, level: {bar.level}, boost: {bar.boost_ticks}, speed = {bar.progress_multi_from_level}")

    clock.tick(60)
    pygame.display.update()
