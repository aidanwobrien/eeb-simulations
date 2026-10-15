import pygame as pg
from game import Game
# from game.menu import StartMenu

def main():
    running = True

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((800, 600))    
    pg.display.set_caption("Hawk-Dove Simulation") 
    clock = pg.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0
        game = Game(screen)
        game.run()

if __name__ == "__main__":
    main()