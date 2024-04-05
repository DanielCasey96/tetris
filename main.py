import pygame
from game import TetrisGame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Change the screen size here
    pygame.display.set_caption("Tetris")

    game = TetrisGame(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
