import random
from games.lotka_volterra.trophic_levels.primary_producers import PrimaryProducer
from games.lotka_volterra.abiotic_features.rock_tile import RockTile

class Herbivore:
    def __init__(self, row, col, h_init, food_gain, food_wait, repro_th, repro_cost, move_cost, basal_cost):
        self.row = row
        self.col = col
        self.energy = h_init
        self.tile_type = "herbivore"
        self.wait = 0
        self.intended = (row, col)  # default to staying in place
        self.food_gain = food_gain
        self.food_wait = food_wait
        self.move_cost = move_cost
        self.basal_cost = basal_cost
        self.speed = 1

    def decide_move(self, world, occupancy):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(directions)

        for dr, dc in directions:
            # TOROIDAL WRAP using modulo
            nr = (self.row + dr) % world.rows
            nc = (self.col + dc) % world.cols

            if occupancy[nr][nc] is None and (nr, nc) not in world.rocks:
                self.intended = (nr, nc)
                return

        # no move possible, stay in place
        self.intended = (self.row, self.col)


    def move(self, occupancy):
        old_row, old_col = self.row, self.col
        self.row, self.col = self.intended
        occupancy[old_row][old_col] = None
        occupancy[self.row][self.col] = self

    def forage(self, world):
        tile = world.grid[self.row][self.col]

        if isinstance(tile, PrimaryProducer) and tile.energy > 0:
            # eat food
            tile.energy = 0
            tile.regrow_timer = world.food_regrow

            self.energy += self.food_gain
            self.wait = self.food_wait

            # remove food tile from world's list
            pos = (self.row, self.col)
            if pos in world.food_tiles:
                world.food_tiles.discard((self.row, self.col))

    def update_energy(self):
        if self.wait > 0:
            self.wait -= 1
            self.energy -= self.basal_cost
        else:
            self.energy -= self.move_cost
        return self.energy > 0
