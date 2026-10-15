import pygame as pg
import matplotlib.pyplot as plt
from utils import draw_text
from settings import GREY, WHITE, RED, BLUE, PERLIN_SCALE, TEXT_SIZE
import random
import noise
from backend.hawk_dove import hawk_dove_payoff
from individual import Individual

class World:
    def __init__(self, screen, width, height, rows, cols):
        self.screen = screen
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.world_size = rows * cols
        self.cell_width = self.width / self.cols

        self.generation = 0

        self.world = self.create_world()
        self.occupancy = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        self.individuals = []
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.world[row][col]
                if tile["tile_type"] == "rock":
                    continue  # skip rocks
                ind = Individual(tile["phenotype"], row, col)
                self.individuals.append(ind)
                self.occupancy[row][col] = ind


    def get_neighbors(self, row, col):
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    ind = self.occupancy[nr][nc]
                    if ind is not None:
                        neighbors.append(ind)
        return neighbors


    def create_world(self):
        world = []
        iso_coords = []

        for row in range(self.rows):
            world.append([])
            for col in range(self.cols):
                rect = [
                    (row * self.cell_width, col * self.cell_width),
                    (row * self.cell_width + self.cell_width, col * self.cell_width),
                    (row * self.cell_width + self.cell_width, col * self.cell_width + self.cell_width),
                    (row * self.cell_width, col * self.cell_width + self.cell_width)
                ]
                iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
                iso_coords.extend(iso_poly)

                world_tile = self.grid_to_world(row, col, self.cell_width)
                world[row].append(world_tile)

        # Find global bounds
        minx = min(x for x, y in iso_coords)
        maxx = max(x for x, y in iso_coords)
        miny = min(y for x, y in iso_coords)
        maxy = max(y for x, y in iso_coords)

        # Compute scaling factor to fit screen
        scale_x = self.screen.get_width() / (maxx - minx)
        scale_y = self.screen.get_height() / (maxy - miny)
        scale = min(scale_x, scale_y) * 0.9  # leave a small margin

        # Compute offset to center
        offset_x = self.screen.get_width()/2 - (minx + maxx)/2 * scale
        offset_y = self.screen.get_height()/2 - (miny + maxy)/2 * scale

        # Create surface
        self.world_tiles = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA)

        # Apply scaling + offset
        for row in range(self.rows):
            for col in range(self.cols):
                tile = world[row][col]
                tile["iso_poly"] = [((x*scale + offset_x), (y*scale + offset_y)) for x, y in tile["iso_poly"]]
                tile["render_pos"] = [tile["render_pos"][0]*scale + offset_x, tile["render_pos"][1]*scale + offset_y]
                tile["iso_centroid"] = self.poly_center(tile["iso_poly"])

                pg.draw.polygon(self.world_tiles, WHITE, tile["iso_poly"], 1)

        self.cell_width = self.cell_width * scale
        return world

    def grid_to_world(self, row, col, cell_width):
        rect = [
            (row * cell_width, col * cell_width),
            (row * cell_width + cell_width, col * cell_width),
            (row * cell_width + cell_width, col * cell_width + cell_width),
            (row * cell_width, col * cell_width + cell_width)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        perlin = 100 * noise.pnoise2(row/10, col/10)
        tile_type = "rock" if perlin >= PERLIN_SCALE or perlin <= -PERLIN_SCALE else "food"

        cart_x = float(row * cell_width)
        cart_y = float(col * cell_width)
        rect = pg.Rect(cart_x, cart_y, cell_width, cell_width)
    
        if random.randint(0, self.world_size) < 890:
            phenotype = "dove"
        else:
            phenotype = "hawk"

        return {
            "tile_type": tile_type,
            "phenotype": phenotype,
            "grid_xy": (row, col),
            "cart_xy": (cart_x, cart_y),
            "iso_poly": iso_poly,
            "iso_centroid": None,
            "render_pos": [min(x for x, y in iso_poly), min(y for x, y in iso_poly)],
            "rect": rect
        }
    
    def cart_to_iso(self, x, y):
        "cartesian to isometric formula"
        iso_x = x-y
        iso_y = (x+y)/2
        return iso_x, iso_y
    
    def poly_center(self, iso_poly):
        cx = sum(x for x, y in iso_poly) / len(iso_poly)
        cy = sum(y for x, y in iso_poly) / len(iso_poly)
        return cx, cy


    def move_individuals(self):
        moves = {}

        for ind in self.individuals:
            directions = [(0,1),(1,0),(0,-1),(-1,0)]
            random.shuffle(directions)

            for dr, dc in directions:
                nr, nc = ind.row + dr, ind.col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    # only move if target is empty and not a rock
                    if self.occupancy[nr][nc] is None and self.world[nr][nc]["tile_type"] != "rock":
                        moves[ind] = (nr, nc)
                        break

        # apply moves
        for ind, (nr, nc) in moves.items():
            self.occupancy[ind.row][ind.col] = None
            ind.row, ind.col = nr, nc
            self.occupancy[nr][nc] = ind




    def play_games(self, games_per_individual, value, cost):
        # reset scores
        for ind in self.individuals:
            ind.score = 0

        for ind in self.individuals:
            # skip if individual is on rock
            if self.world[ind.row][ind.col]["tile_type"] == "rock":
                continue

            neighbors = self.get_neighbors(ind.row, ind.col)
            # filter out neighbors on rocks
            neighbors = [n for n in neighbors if self.world[n.row][n.col]["tile_type"] != "rock"]

            for _ in range(games_per_individual):
                if neighbors:
                    opponent = random.choice(neighbors)
                    ind.score += hawk_dove_payoff(ind.phenotype, opponent.phenotype, value, cost)


    def next_generation(self):
        new_occupancy = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        new_individuals = []

        for ind in self.individuals:
            # candidates: self + neighbors
            candidates = [ind] + self.get_neighbors(ind.row, ind.col)

            scores = [c.score for c in candidates]
            min_score = min(scores)
            fitness = [s - min_score + 1e-6 for s in scores]

            parent = random.choices(candidates, weights=fitness, k=1)[0]

            offspring_row, offspring_col = ind.row, ind.col
            # if the tile is a rock, pick a random neighbor that's not a rock
            if self.world[offspring_row][offspring_col]["tile_type"] == "rock":
                neighbors = [(ind.row+dr, ind.col+dc) for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]]
                neighbors = [(r,c) for r,c in neighbors if 0<=r<self.rows and 0<=c<self.cols and self.world[r][c]["tile_type"]!="rock"]
                if neighbors:
                    offspring_row, offspring_col = random.choice(neighbors)

            offspring = Individual(parent.phenotype, offspring_row, offspring_col)
            # add offspring to lists
            new_individuals.append(offspring)
            new_occupancy[offspring_row][offspring_col] = offspring

        self.individuals = new_individuals
        self.occupancy = new_occupancy

        self.generation += 1


    
    def update(self, games_per_individual, value, cost):
        self.move_individuals()
        self.play_games(games_per_individual, value, cost)
        self.next_generation()


    def draw(self, screen):
        screen.blit(self.world_tiles, (0, 0))

        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.world[row][col]
                if tile["tile_type"] == "rock":
                    cx, cy = tile["iso_centroid"]
                    pg.draw.circle(screen, GREY, (int(cx), int(cy)), 5)

        for ind in self.individuals:
            color = RED if ind.phenotype=="hawk" else BLUE
            tile = self.world[ind.row][ind.col]
            cx, cy = tile["iso_centroid"]
            pg.draw.circle(screen, color, (int(cx), int(cy)), 3)


