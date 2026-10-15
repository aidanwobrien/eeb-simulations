import pygame as pg
import sys
from games.lotka_volterra.utils import draw_text
from games.lotka_volterra.world import World
from games.lotka_volterra.settings import (
    BLACK, RED, BLUE, GREEN,
    WHITE, GRID_X, GRID_Y, 
    FRAMES_PER_GENERATION, TEXT_SIZE,
                       )
from mvc.lotka_volterra.plot_tab import PlotTab
from mvc.lotka_volterra.phase_plot_tab import PhasePlotTab
# from games.lotka_volterra.plots.plot import Plot
# from games.lotka_volterra.plots.phase_plot import PhasePlot

class Game:

    def __init__(self, screen, params):
        self.screen = screen
        self.clock = pg.time.Clock() 
        self.width, self.height = self.screen.get_size()
        self.unpack_params(params)

        self.world = World(screen, 
                           self.width, 
                           self.height, 
                           self.grid_x, 
                           self.grid_y,
                           self.initial_food_pop_rate,
                           self.food_regrow,
                           self.h_init,
                           self.h_move_cost,
                           self.h_basal_cost,
                           self.h_food_gain,
                           self.h_food_wait,
                           self.h_repro_th,
                           self.h_repro_cost,
                           self.p_init,
                           self.p_move_cost,
                           self.p_basal_cost,
                           self.p_food_gain,
                           self.p_food_wait,
                           self.p_repro_th,
                           self.p_repro_cost,
                           self.prey_birth_rate,
                           self.predation_rate,
                           self.predator_mortality_rate,
                           self.predator_fitness_gain_rate,
                           self.initial_prey_pop,
                           self.initial_predator_pop,
                           self.time_step,
                           self.frames_per_generation,
                           self.perlin_scale,
                           self.perlin_noise_scale,
                           )

        self.time_series_tab = PlotTab(self.world, self.grid_x, self.grid_y)
        self.phase_plot_tab = PhasePlotTab(self.world, self.grid_x, self.grid_y)

        # self.plot = Plot(self.world, GRID_X, GRID_Y)
        # self.phase_plot = PhasePlot(self.world)

        self.frame_counter = 0

    def unpack_params(self, params):

        self.initial_food_pop_rate = params["INITIAL_FOOD_POP_RATE"]
        self.food_regrow = params["FOOD_REGROW"]
        self.grid_x = params["GRID_X"]
        self.grid_y = params["GRID_Y"]
        self.h_init = params["H_INIT"]
        self.h_move_cost = params["H_MOVE_COST"]
        self.h_basal_cost = params["H_BASAL_COST"]
        self.h_food_gain = params["H_FOOD_GAIN"]
        self.h_food_wait = params["H_FOOD_WAIT"]
        self.h_repro_th = params["H_REPRO_TH"]
        self.h_repro_cost = params["H_REPRO_COST"]
        self.p_init = params["P_INIT"]
        self.p_move_cost = params["P_MOVE_COST"]
        self.p_basal_cost = params["P_BASAL_COST"]
        self.p_food_gain = params["P_FOOD_GAIN"]
        self.p_food_wait = params["P_FOOD_WAIT"]
        self.p_repro_th = params["P_REPRO_TH"]
        self.p_repro_cost = params["P_REPRO_COST"]
        self.prey_birth_rate = params["PREY_BIRTH_RATE"]
        self.predation_rate = params["PREDATION_RATE"]
        self.predator_mortality_rate = params["PREDATOR_MORTALITY_RATE"]
        self.predator_fitness_gain_rate = params["PREDATOR_FITNESS_GAIN_RATE"]
        self.initial_prey_pop = params["INITIAL_PREY_POP"]
        self.initial_predator_pop = params["INITIAL_PREDATOR_POP"]
        self.time_step = params["TIME_STEP"]
        self.frames_per_generation = params["FRAMES_PER_GENERATION"]
        self.perlin_scale = params["PERLIN_SCALE"]
        self.perlin_noise_scale = params["PERLIN_NOISE_SCALE"]

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
            pass

            # # quit program
            # if event.type == pg.QUIT:
            #     pg.quit()
            #     sys.exit()

            # # quit with esc key
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_ESCAPE:
            #         pg.quit()
            #         sys.exit()

    def update(self, events):
        self.frame_counter += 1
        if self.frame_counter >= self.frames_per_generation:
            self.world.update()
            # self.time_series_tab.update()
            # self.phase_plot_tab.update()
            self.frame_counter = 0

    def draw(self):
        self.screen.fill(BLACK)

        self.world.draw(self.screen)

        draw_text(self.screen,
                  f'Plants = {len(self.world.food_tiles)}',
                  TEXT_SIZE,
                  GREEN,
                  (self.width*0.05, self.height * 0.1))
        
        draw_text(self.screen,
                  f'Herbivores = {len(self.world.herbivores)}',
                  TEXT_SIZE,
                  BLUE,
                  (self.width*0.05, self.height * 0.15))
        
        draw_text(self.screen,
                  f'Carnivores = {len(self.world.predators)}',
                  TEXT_SIZE,
                  RED,
                  (self.width*0.05, self.height * 0.20))
        
        draw_text(self.screen,
                  f'Time = {(self.world.generation)}',
                  TEXT_SIZE,
                  WHITE,
                  (self.width*0.05, self.height * 0.05))

        # # draw FPS indicator after all other draw loops are run (to check performance)
        # draw_text(self.screen,
        #           'fps={}'.format(round(self.clock.get_fps())),
        #           TEXT_SIZE,
        #           WHITE,
        #           (self.width*0.75, self.height * 0.95))

        pg.display.flip()