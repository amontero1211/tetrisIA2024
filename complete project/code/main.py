from settings import *
from sys import exit
from os.path import join

# components
from game import Game, Tetromino, Block
from score import Score
from preview import Preview

from random import choice
from agent import alpha_beta_search, generate_moves

class Main:
    def __init__(self):
        # general 
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        self.agent_game = Game(self.get_next_shape, self.update_score)  # Segundo objeto Game para el agente
        self.score = Score()
        self.preview = Preview()

        # audio 
        self.music = pygame.mixer.Sound(join('..', 'sound', 'music.wav'))
        self.music.set_volume(0.05)
        self.music.play(-1)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        
            # Agente tomando decisiones
            current_tetromino = self.agent_game.tetromino
            field_data = self.agent_game.field_data
            depth = 3  # Profundidad del árbol de búsqueda
            best_move = None
            best_score = -float('inf')

            if current_tetromino:
                possible_moves = generate_moves(current_tetromino, field_data)
                for move in possible_moves:
                    move_field_data, x, rotation, lines_cleared, level = move
                    score = alpha_beta_search(move_field_data, depth, -float('inf'), float('inf'), True, current_tetromino)
                    if score > best_score:
                        best_score = score
                        best_move = move

                # Aplicar el mejor movimiento
                if best_move:
                    move_field_data, x, rotation, lines_cleared, level = best_move
                    current_tetromino.pos.x = x
                    for _ in range(rotation):
                        current_tetromino.rotate()

            # display 
            self.display_surface.fill(GRAY)
            
            # components
            self.game.run()
            self.agent_game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            # updating the game
            pygame.display.update()
            self.clock.tick()

if __name__ == '__main__':
    main = Main()
    main.run()
