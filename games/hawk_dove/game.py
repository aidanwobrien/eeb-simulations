import pygame as pg
import sys
from games.hawk_dove.utils import draw_text
from games.hawk_dove.world import World
from games.hawk_dove.settings import (
    BLACK, RED, BLUE,
    WHITE, VALUE, COST, GAMES_PER_INDIVIDUAL, GRID_X, GRID_Y,
    FRAMES_PER_GENERATION, TEXT_SIZE, PERLIN_SCALE, SELECTION_TEMP, INITIAL_HAWK_POP, INITIAL_DOVE_POP
)


def default_params():
    """Fallbacks for standalone runs or any key the caller leaves out."""
    return {
        "TIME_STEP": 0.1,
        "GRID_X": GRID_X,
        "GRID_Y": GRID_Y,
        "GAMES_PER_INDIVIDUAL": GAMES_PER_INDIVIDUAL,
        "VALUE": VALUE,
        "COSTS": COST,
        "FRAMES_PER_GENERATION": FRAMES_PER_GENERATION,
        "PERLIN_SCALE": PERLIN_SCALE,
        "INITIAL_HAWK_POP": INITIAL_HAWK_POP,
        "INITIAL_DOVE_POP": INITIAL_DOVE_POP,
        "SELECTION_TEMP": SELECTION_TEMP,
    }


class Game:

    def __init__(self, screen, params=None, world=None):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.width, self.height = self.screen.get_size()
        self.unpack_params({**default_params(), **(params or {})})

        self.manage_world = world is None

        if world is None:
            world = World(screen,
                          self.width,
                          self.height,
                          self.grid_x,
                          self.grid_y,
                          self.games_per_individual,
                          self.value,
                          self.costs,
                          self.time_step,
                          self.frames_per_generation,
                          self.perlin_scale,
                          self.initial_hawk_pop,
                          self.initial_dove_pop,
                          )
        self.world = world

        self.frame_counter = 0

    def unpack_params(self, params):

        self.time_step = params["TIME_STEP"]
        self.grid_x = params["GRID_X"]
        self.grid_y = params["GRID_Y"]
        self.games_per_individual = params["GAMES_PER_INDIVIDUAL"]
        self.value = params["VALUE"]
        self.costs = params["COSTS"]
        self.frames_per_generation = params["FRAMES_PER_GENERATION"]
        self.perlin_scale = params["PERLIN_SCALE"]
        self.initial_hawk_pop = params["INITIAL_HAWK_POP"]
        self.initial_dove_pop = params["INITIAL_DOVE_POP"]
        self.selection_temp = params["SELECTION_TEMP"]

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)

            events = pg.event.get()
            self.events(events)
            self.update(events)
            self.draw()

    def events(self, events):
        # Embedded in Qt, the view owns quitting; only handle it when standalone.
        if not self.manage_world:
            return

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
        # When embedded, the view advances the world on its own timer.
        if not self.manage_world:
            return

        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_generation:
            self.world.update()
            self.frame_counter = 0

    def draw(self):
        self.screen.fill(BLACK)

        self.world.draw(self.screen)

        hawks, doves = self.world.count_phenotypes()

        draw_text(self.screen,
                  f'Generation = {self.world.generation}',
                  TEXT_SIZE,
                  WHITE,
                  (self.width * 0.05, self.height * 0.05))

        draw_text(self.screen,
                  f'Hawks = {hawks}',
                  TEXT_SIZE,
                  RED,
                  (self.width * 0.05, self.height * 0.10))

        draw_text(self.screen,
                  f'Doves = {doves}',
                  TEXT_SIZE,
                  BLUE,
                  (self.width * 0.05, self.height * 0.15))

        # # FPS only means something when this Game runs its own 60 FPS loop
        # if self.manage_world:
        #     draw_text(self.screen,
        #               'fps={}'.format(round(self.clock.get_fps())),
        #               TEXT_SIZE,
        #               WHITE,
        #               (self.width * 0.75, self.height * 0.95))

        pg.display.flip()