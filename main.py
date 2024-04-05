import pygame
from game import TetrisGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Tetris")

    TetrisGame.start_game(screen)

if __name__ == "__main__":
    main()
