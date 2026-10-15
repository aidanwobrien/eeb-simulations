import pygame as pg

class Individual:
    def __init__(self, phenotype, row, col):
        self.phenotype = phenotype
        self.row = row
        self.col = col
        self.score = 0