import pygame as pg
import random
import noise
import matplotlib.pyplot as plt
from collections import deque
from games.lotka_volterra.settings import *
from games.lotka_volterra.trophic_levels.primary_producers import PrimaryProducer
from games.lotka_volterra.trophic_levels.primary_consumers import Herbivore
from games.lotka_volterra.trophic_levels.secondary_consumers import Predator
from games.lotka_volterra.abiotic_features.rock_tile import RockTile

# ---------- FOOD GRID / PRIMARY PRODUCER TILES ----------
class PrimaryProducerTile(PrimaryProducer):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.energy = 1           # 1 = edible, 0 = eaten
        self.regrow_timer = 0     # turns until it regrows

    def update(self, regrow_time):
        if self.energy == 0:
            self.regrow_timer -= 1
            if self.regrow_timer <= 0:
                self.energy = 1

# ---------- WORLD ----------
class World:
    def __init__(
            self,
            screen, 
            width, 
            height,
            rows, 
            cols,
            initial_food_pop_rate,
            food_regrow,
            h_init,
            h_move_cost,
            h_basal_cost,
            h_food_gain,
            h_food_wait,
            h_repro_th,
            h_repro_cost,
            p_init,
            p_move_cost,
            p_basal_cost,
            p_food_gain,
            p_food_wait,
            p_repro_th,
            p_repro_cost,
            prey_birth_rate,
            predation_rate,
            predator_mortality_rate,
            predator_fitness_gain_rate,
            initial_prey_pop,
            initial_predator_pop,
            time_step,
            frames_per_generation,
            perlin_scale,
            perlin_noise_scale,
                 ):
        self.screen = screen
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cell_width = width/cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.occupancy = [[None for _ in range(cols)] for _ in range(rows)]

        self.food_regrow = food_regrow

        self.initial_food_pop_rate = initial_food_pop_rate
        self.grid_x = rows
        self.grid_y = cols
        self.h_init = h_init
        self.h_move_cost = h_move_cost
        self.h_basal_cost = h_basal_cost
        self.h_food_gain = h_food_gain
        self.h_food_wait = h_food_wait
        self.h_repro_th = h_repro_th
        self.h_repro_cost = h_repro_cost
        self.p_init = p_init
        self.p_move_cost = p_move_cost
        self.p_basal_cost = p_basal_cost
        self.p_food_gain = p_food_gain
        self.p_food_wait = p_food_wait
        self.p_repro_th = p_repro_th
        self.p_repro_cost = p_repro_cost
        self.prey_birth_rate = prey_birth_rate
        self.predation_rate = predation_rate
        self.predator_mortality_rate = predator_mortality_rate
        self.predator_fitness_gain_rate = predator_fitness_gain_rate
        self.time_step = time_step
        self.frames_per_generation = frames_per_generation
        self.perlin_scale = perlin_scale
        self.perlin_noise_scale = perlin_noise_scale

        self.food_tiles = set()
        self.herbivores = []
        self.predators = []

        self.generation = 0

        self.initial_prey_pop = initial_prey_pop
        self.initial_predator_pop = initial_predator_pop

        self.food_history = deque(maxlen=1000)
        self.prey_history = deque(maxlen=1000)
        self.predator_history = deque(maxlen=1000)

        self.create_world()
        self.spawn_agents()

    # ---------- CREATE GRID ----------
    def create_world(self):
        self.world_tiles = pg.Surface((self.width, self.height), pg.SRCALPHA)
        iso_coords = []

        self.rocks = set()  # track rock positions

        for row in range(self.rows):
            for col in range(self.cols):
                perlin = noise.pnoise2(row/self.perlin_noise_scale, col/self.perlin_noise_scale)*100
                if perlin > self.perlin_scale or perlin < -self.perlin_scale:
                    tile = RockTile(row, col)
                    self.rocks.add((row, col))
                    self.occupancy[row][col] = "rock" 
                else:
                    tile = PrimaryProducerTile(row, col)

                # Compute isometric polygon
                x = row * self.cell_width
                y = col * self.cell_width
                rect = [
                    (x, y),
                    (x + self.cell_width, y),
                    (x + self.cell_width, y + self.cell_width),
                    (x, y + self.cell_width)
                ]
                tile.iso_poly = [self.cart_to_iso(px, py) for px, py in rect]
                tile.iso_centroid = self.poly_center(tile.iso_poly)
                iso_coords.extend(tile.iso_poly)

                self.grid[row][col] = tile

        # Find global bounds
        minx = min(x for x, y in iso_coords)
        maxx = max(x for x, y in iso_coords)
        miny = min(y for x, y in iso_coords)
        maxy = max(y for x, y in iso_coords)

        scale_x = self.width / (maxx - minx)
        scale_y = self.height / (maxy - miny)
        scale = min(scale_x, scale_y) * 0.9
        offset_x = self.width / 2 - (minx + maxx) / 2 * scale
        offset_y = self.height / 2 - (miny + maxy) / 2 * scale

        # Apply scale/offset
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                tile.iso_poly = [(x*scale + offset_x, y*scale + offset_y) for x, y in tile.iso_poly]
                tile.iso_centroid = self.poly_center(tile.iso_poly)

    # ---------- SPAWN AGENTS ----------
    def spawn_agents(self):
        # All candidate food tiles (non-rock)
        candidate_tiles = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if isinstance(self.grid[r][c], PrimaryProducer)
        ]
        random.shuffle(candidate_tiles)

        # Determine max agents allowed
        max_agents = len(candidate_tiles)
        total_requested = self.initial_prey_pop + self.initial_predator_pop
        if total_requested > max_agents:
            return
        else:
            prey_to_spawn = self.initial_prey_pop
            predator_to_spawn = self.initial_predator_pop

        # Spawn prey
        self.herbivores = []
        self.predators = []
        self.food_tiles = set(candidate_tiles)
        empty_tiles = candidate_tiles.copy()

        for _ in range(prey_to_spawn):
            if not empty_tiles:
                break
            r, c = empty_tiles.pop()
            h = Herbivore(r, c, self.h_init, self.h_food_gain, self.h_food_wait,
                        self.h_repro_th, self.h_repro_cost, self.h_move_cost, self.h_basal_cost)
            self.herbivores.append(h)
            self.occupancy[r][c] = h

        # Spawn predators
        for _ in range(predator_to_spawn):
            if not empty_tiles:
                break
            r, c = empty_tiles.pop()
            p = Predator(r, c, self.p_init, self.p_food_gain, self.p_food_wait,
                        self.p_repro_th, self.p_repro_cost, self.p_move_cost, self.p_basal_cost)
            self.predators.append(p)
            self.occupancy[r][c] = p

    def step(self):
        # ---------------- HERBIVORE ACTIONS ----------------
        # 1) Decide moves
        for h in self.herbivores:
            h.decide_move(self, self.occupancy)

        # 2) Move & forage
        for h in self.herbivores:
            old_pos = (h.row, h.col)
            new_row = self.wrap(h.intended[0], self.rows)
            new_col = self.wrap(h.intended[1], self.cols)
            if self.occupancy[new_row][new_col] is None:
                self.occupancy[h.row][h.col] = None
                h.row, h.col = new_row, new_col
                self.occupancy[new_row][new_col] = h
                h.forage(self)


        # 3) Reproduce
        new_herbivores = []
        max_herbivores = self.rows * self.cols - len(self.rocks)
        for h in self.herbivores:
            if h.energy >= self.h_repro_th and len(self.herbivores) + len(new_herbivores) < max_herbivores:
                directions = [(0,1),(1,0),(0,-1),(-1,0)]
                random.shuffle(directions)
                for dr, dc in directions:
                    nr = self.wrap(h.row + dr, self.rows)
                    nc = self.wrap(h.col + dc, self.cols)
                    if self.occupancy[nr][nc] is None and (nr, nc) not in self.rocks:
                        h.energy -= self.h_repro_cost
                        child = Herbivore(nr, nc, self.h_init, self.h_food_gain, self.h_food_wait, self.h_repro_th, self.h_repro_th, self.h_move_cost, self.h_basal_cost)
                        new_herbivores.append(child)
                        self.occupancy[nr][nc] = child
                        break
        self.herbivores.extend(new_herbivores)

        # 4) Remove dead herbivores
        for h in self.herbivores[:]:
            if not h.update_energy():
                self.occupancy[h.row][h.col] = None
                self.herbivores.remove(h)

        # ---------------- PREDATOR ACTIONS ----------------
        herb_positions = {(h.row, h.col): h for h in self.herbivores}
        for p in self.predators:
            for _ in range(p.speed):  # move one tile at a time
                # Decide move
                if herb_positions:
                    # move toward nearest prey
                    nearest = min(
                        herb_positions.keys(),
                        key=lambda pos: abs(pos[0]-p.row) + abs(pos[1]-p.col)
                    )
                    dr = 1 if nearest[0] > p.row else -1 if nearest[0] < p.row else 0
                    dc = 1 if nearest[1] > p.col else -1 if nearest[1] < p.col else 0
                else:
                    # random move if no herbivores
                    dr, dc = random.choice([(0,1),(1,0),(0,-1),(-1,0)])

                # Calculate intended tile with toroidal wrap
                nr = self.wrap(p.row + dr, self.rows)
                nc = self.wrap(p.col + dc, self.cols)

                # Check rocks and occupancy (cannot pass through rocks)
                if (nr, nc) in self.rocks or (self.occupancy[nr][nc] not in (None, Herbivore)):
                    # try a random neighbor instead
                    directions = [(0,1),(1,0),(0,-1),(-1,0)]
                    random.shuffle(directions)
                    moved = False
                    for dr2, dc2 in directions:
                        tmp_r = self.wrap(p.row + dr2, self.rows)
                        tmp_c = self.wrap(p.col + dc2, self.cols)
                        if (tmp_r, tmp_c) not in self.rocks and (self.occupancy[tmp_r][tmp_c] is None or isinstance(self.occupancy[tmp_r][tmp_c], Herbivore)):
                            nr, nc = tmp_r, tmp_c
                            moved = True
                            break
                    if not moved:
                        nr, nc = p.row, p.col  # blocked, stay

                # Eat herbivore if present before moving
                if (nr, nc) in herb_positions:
                    prey = herb_positions[(nr, nc)]
                    if prey in self.herbivores:
                        self.herbivores.remove(prey)
                        p.energy += p.food_gain
                        p.energy = min(p.energy, p.max_energy)
                        herb_positions.pop((nr, nc))

                # Move predator
                old_pos = (p.row, p.col)
                self.occupancy[old_pos[0]][old_pos[1]] = None
                p.row, p.col = nr, nc
                self.occupancy[p.row][p.col] = p

                # Eat herbivore if present
                if (p.row, p.col) in herb_positions:
                    prey = herb_positions[(p.row, p.col)]
                    if prey in self.herbivores:
                        self.herbivores.remove(prey)
                        p.energy += p.food_gain
                        p.energy = min(p.energy, p.max_energy)
                        self.occupancy[p.row][p.col] = p
                        herb_positions.pop((p.row, p.col))

        # 5) Predator reproduction
        new_predators = []
        max_predators = self.rows * self.cols - len(self.rocks)
        for p in self.predators:
            if p.energy >= self.p_repro_th and len(self.predators) + len(new_predators) < max_predators:
                directions = [(0,1),(1,0),(0,-1),(-1,0)]
                random.shuffle(directions)
                for dr, dc in directions:
                    nr = self.wrap(p.row + dr, self.rows)
                    nc = self.wrap(p.col + dc, self.cols)
                    if self.occupancy[nr][nc] is None and (nr, nc) not in self.rocks:
                        p.energy -= self.p_repro_cost
                        child = Predator(nr, nc, self.p_init, self.p_food_gain, self.p_food_wait, self.p_repro_th, self.p_repro_cost, self.p_move_cost, self.p_basal_cost)
                        new_predators.append(child)
                        self.occupancy[nr][nc] = child
                        break
        self.predators.extend(new_predators)

        # 6) Remove dead predators
        for p in self.predators[:]:
            if not p.update_energy():
                self.occupancy[p.row][p.col] = None
                self.predators.remove(p)

        # ---------------- TILE UPDATES ----------------
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.grid[r][c]
                if isinstance(tile, PrimaryProducer):
                    was_empty = tile.energy == 0
                    tile.update(self.food_regrow)
                    if was_empty and tile.energy > 0:
                        self.food_tiles.add((r, c))

        # ---------------- RECORD HISTORY ----------------
        self.food_history.append(len(self.food_tiles))
        self.prey_history.append(len(self.herbivores))
        self.predator_history.append(len(self.predators))
        self.generation += 1


    # ---------- DRAW ----------
    def draw(self, screen):
        screen.fill((0,0,0))
        for row in self.grid:
            for tile in row:
                if isinstance(tile, RockTile):
                    color = ROCK_COLOR
                elif isinstance(tile, PrimaryProducerTile):
                    color = FOOD_FULL if tile.energy > 0 else FOOD_EMPTY
                else:
                    color = (120, 120, 120)

                pg.draw.polygon(screen, color, tile.iso_poly)
                pg.draw.polygon(screen, BLACK, tile.iso_poly, 1)

        for h in self.herbivores:
            cx, cy = self.grid[h.row][h.col].iso_centroid
            pg.draw.circle(screen, BLUE, (int(cx), int(cy)), 3)

        for p in self.predators:
            cx, cy = self.grid[p.row][p.col].iso_centroid
            pg.draw.circle(screen, RED, (int(cx), int(cy)), 3)

    # ---------- UTILITIES ----------
    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def poly_center(self, poly):
        x_coords = [p[0] for p in poly]
        y_coords = [p[1] for p in poly]
        return sum(x_coords)/len(poly), sum(y_coords)/len(poly)


    def update(self):
        """Advance the world by one time step"""
        self.step()

    def wrap(self, value, max_val):
        """Wrap a coordinate around the grid edges."""
        return value % max_val

    # def configure(self, params: dict):
    #     for key, value in params.items():
    #         setattr(self, key, value)

    #     self.reset()


    # def reset(self):
    #     self.generation = 0
    #     self.food_history.clear()
    #     self.prey_history.clear()
    #     self.predator_history.clear()

    #     self.food_tiles.clear()
    #     self.herbivores.clear()
    #     self.predators.clear()

    #     self.populate()
