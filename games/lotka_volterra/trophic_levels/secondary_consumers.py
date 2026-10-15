import random

class Predator:
    def __init__(self, row, col, p_init,
                 food_gain, food_wait, 
                 repro_th, repro_cost, move_cost, basal_cost):
        self.row = row
        self.col = col
        self.energy = p_init
        self.tile_type = "predator"
        self.wait = 0
        self.intended = (row, col)
        self.food_gain = food_gain
        self.food_wait = food_wait
        self.repro_th = repro_th      # energy threshold for reproduction
        self.repro_cost = repro_cost  # energy cost to reproduce
        self.move_cost = move_cost
        self.basal_cost = basal_cost

        self.max_energy = repro_th * 1.5
        self.speed = 2

    def decide_move(self, herb_positions, occupancy, world):
        # If no herbivores, try random move to empty neighbor
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(directions)

        # If there is prey, move toward nearest
        if herb_positions:
            target = min(
                herb_positions,
                key=lambda p: self.toroidal_dist(self.row, self.col, p[0], p[1],
                                            world.rows, world.cols)
            )

            dr = self.toroidal_step(self.row, target[0], world.rows)
            dc = self.toroidal_step(self.col, target[1], world.cols)

            nr, nc = self.row + dr, self.col + dc

        if (nr, nc) not in world.rocks:
            self.intended = (nr, nc)
            return

        # Random move if blocked or no prey
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if (0 <= nr < world.rows and 0 <= nc < world.cols 
                and (nr, nc) not in world.rocks 
                and occupancy[nr][nc] is None):
                self.intended = (nr, nc)
                return

        # Stay in place if all options blocked
        self.intended = (self.row, self.col)

    def toroidal_dist(self, r1, c1, r2, c2, rows, cols):
        dr = min(abs(r1 - r2), rows - abs(r1 - r2))
        dc = min(abs(c1 - c2), cols - abs(c1 - c2))
        return dr + dc

    def toroidal_step(self, a, b, size):
        if a == b:
            return 0
        forward = (b - a) % size
        backward = (a - b) % size
        return 1 if forward < backward else -1

    def move(self, occupancy, world):
        nr, nc = self.intended
        if (nr, nc) in world.rocks:
            # blocked, stay in place
            self.intended = (self.row, self.col)
            nr, nc = self.row, self.col

        old_row, old_col = self.row, self.col
        self.row, self.col = nr, nc

        occupancy[old_row][old_col] = None
        occupancy[self.row][self.col] = self


    def eat(self, world, occupancy):
        if self.energy >= self.max_energy:
            return

        pos = (self.row, self.col)



        for h in world.herbivores:
            if (h.row, h.col) == pos:
                world.herbivores.remove(h)   # kill prey
                occupancy[h.row][h.col] = None
                self.energy += self.food_gain
                self.wait = self.food_wait
                self.energy = min(self.energy, self.max_energy)
                return

    def update_energy(self):
        self.energy -= (self.basal_cost + self.move_cost)
        return self.energy > 0

