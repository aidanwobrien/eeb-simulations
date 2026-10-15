import pygame as pg
import sys
from utils import draw_text
from world import World
from settings import (
    BLACK, RED, BLUE,
    WHITE, VALUE, COST, GAMES_PER_INDIVIDUAL, GRID_X, GRID_Y, 
    FRAMES_PER_GENERATION, TEXT_SIZE
                       )
from plot import Plot

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock() 
        self.width, self.height = self.screen.get_size()

        self.world = World(screen, self.width, self.height, GRID_X, GRID_Y)
        self.plot = Plot(self.world, GRID_X, GRID_Y)

        self.frame_counter = 0
        self.frames_per_generation = FRAMES_PER_GENERATION

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)

            events = pg.event.get()
            self.events(events)
            self.update(events)
            self.draw()

    def events(self, events):
        for event in events:

            # quit program
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # quit with esc key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self, events):
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_generation:
            self.world.update(GAMES_PER_INDIVIDUAL, VALUE, COST)
            self.plot.update()
            self.frame_counter = 0

    def draw(self):
        self.screen.fill(BLACK)

        self.world.draw(self.screen)

        draw_text(self.screen,
                  'hawks',
                  TEXT_SIZE,
                  RED,
                  (self.width*0.15, self.height * 0.1))
        
        draw_text(self.screen,
                  'doves',
                  TEXT_SIZE,
                  BLUE,
                  (self.width*0.15, self.height * 0.15))
        
        draw_text(self.screen,
                  f'generation={self.world.generation}',
                  TEXT_SIZE,
                  WHITE,
                  (self.width*0.15, self.height * 0.05))

        # draw FPS indicator after all other draw loops are run (to check performance)
        draw_text(self.screen,
                  'fps={}'.format(round(self.clock.get_fps())),
                  TEXT_SIZE,
                  WHITE,
                  (self.width*0.75, self.height * 0.95))

        pg.display.flip()