import pygame
import random


class TetrisGame:
    def __init__(self, screen):
        self.game_over_flag = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.cell_size = 30
        self.playable_area_width = 8
        self.playable_area_height = 20
        self.board_width = self.playable_area_width
        self.board_height = self.playable_area_height
        self.screen_width = self.board_width * self.cell_size
        self.screen_height = self.board_height * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")
        self.board = [[0] * self.board_width for _ in range(self.board_height)]
        self.current_piece = None
        self.current_piece_x = 3
        self.current_piece_y = 0
        self.score = 0
        self.new_piece()

    def new_piece(self):
        if not self.game_over_flag:
            self.current_piece = random.choice([
                [[1, 1, 1, 1]],  # I piece
                [[1, 1, 1], [0, 1, 0]],  # T piece
                [[1, 1, 1], [1, 0, 0]],  # L piece
                [[1, 1, 1], [0, 0, 1]],  # J piece
                [[0, 1, 1], [1, 1, 0]],  # S piece
                [[1, 1, 0], [0, 1, 1]],  # Z piece
                [[1, 1], [1, 1]]  # O piece
            ])
            self.current_piece_x = 3
            self.current_piece_y = 0

            # Check if the new piece overlaps with existing blocks
            if self.check_collision(0, 0):
                self.game_over()

    def game_over(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Load font file and render game over text
        font_path = pygame.font.match_font('arial')
        font = pygame.font.Font(font_path, 64)  # Load font with size 64
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

        # Display game over message
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        # Wait for a few seconds before quitting
        pygame.time.wait(3000)

        # Set a flag to indicate that the game is over
        self.game_over_flag = True

    def draw_board(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y][x] == 0:
                    pygame.draw.rect(self.screen, (128, 128, 128),
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        self.draw_piece()
        pygame.display.flip()

    def draw_piece(self):
        if self.current_piece:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, (255, 255, 255), (
                            (x + self.current_piece_x) * self.cell_size, (y + self.current_piece_y) * self.cell_size,
                            self.cell_size, self.cell_size))

    def move_piece_left(self):
        if not self.check_collision(-1, 0):
            self.current_piece_x -= 1

    def move_piece_right(self):
        if not self.check_collision(1, 0):
            self.current_piece_x += 1

    def move_piece_down(self):
        if not self.check_collision(0, 1):
            self.current_piece_y += 1
            return True
        return False

    def rotate_piece(self):
        rotated_piece = [list(row) for row in self.current_piece]
        rotated_piece = list(zip(*rotated_piece))
        rotated_piece = [list(reversed(row)) for row in rotated_piece]
        self.current_piece = rotated_piece

    def lock_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece_y + y][self.current_piece_x + x] = 1
        self.clear_rows()
        self.new_piece()

    def check_collision(self, offset_x, offset_y):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    # Check if the current piece is out of bounds
                    if (self.current_piece_x + x + offset_x < 0 or
                            self.current_piece_x + x + offset_x >= self.board_width or
                            self.current_piece_y + y + offset_y >= self.board_height or
                            self.board[self.current_piece_y + y + offset_y][self.current_piece_x + x + offset_x]):
                        return True
                    # Check if the current piece overlaps with existing blocks at the top of the board
                    if self.current_piece_y + y + offset_y < 0:
                        return True
        return False

    def clear_rows(self):
        completed_rows = []
        for y in range(self.board_height):
            if all(self.board[y]):
                completed_rows.append(y)

        # Remove completed rows and add new empty rows at the top
        for row in completed_rows:
            del self.board[row]
            self.board.insert(0, [0] * self.board_width)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_piece_right()
                elif event.key == pygame.K_DOWN:
                    self.move_piece_down()
                elif event.key == pygame.K_UP:
                    self.rotate_piece()

    def update_game_state(self):
        # Implement game state update logic here
        pass

    def run(self):
        running = True
        tick_rate = 500
        last_drop_time = pygame.time.get_ticks()

        while running:
            self.handle_input()

            # Update game state periodically based on tick rate
            current_time = pygame.time.get_ticks()
            if current_time - last_drop_time > tick_rate:
                if not self.move_piece_down():
                    self.lock_piece()
                    if not self.game_over_flag:
                        self.new_piece()
                last_drop_time = current_time

            # Update and draw game board
            self.update_game_state()
            self.draw_board()

            # Cap the frame rate
            self.clock.tick(30)

            if self.game_over_flag:
                break

    @classmethod
    def start_game(cls, screen):
        game = cls(screen)
        game.run()
