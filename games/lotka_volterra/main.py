import pygame as pg
from game import Game

def main():
    running = True

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((900, 900))    
    pg.display.set_caption("Lottka-Volterra Simulation") 
    clock = pg.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0
        game = Game(screen)
        game.run()

if __name__ == "__main__":
    main()