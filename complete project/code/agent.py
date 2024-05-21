from game import Tetromino, Block
from settings import *
from copy import deepcopy

def evaluate_position(field_data, lines_cleared, level, shape):
    Salt = sum([sum(row) for row in field_data])
    nlimp = lines_cleared
    nhue = sum([row.count(0) for row in field_data])
    nblog = sum([sum(row) for row in field_data])

    # Pesos de la función de evaluación
    W1 = -0.5
    W2 = 1.0
    W3 = -0.5
    W4 = -0.5

    return W1 * Salt + W2 * nlimp + W3 * nhue + W4 * nblog

def generate_moves(tetromino, field_data):
    moves = []
    original_x, original_y = tetromino.pos.x, tetromino.pos.y
    original_shape = deepcopy(tetromino.shape)

    for rotation in range(4):
        tetromino.shape = deepcopy(original_shape)
        for _ in range(rotation):
            tetromino.rotate()

        for x in range(COLUMNS - len(tetromino.shape[0]) + 1):
            tetromino.pos.x = x
            tetromino.pos.y = 0
            while not tetromino.next_move_vertical_collide(field_data, 1):
                tetromino.move_down()

            # Copia profunda del campo de juego para la simulación
            simulated_field_data = deepcopy(field_data)
            for block in tetromino.blocks:
                bx, by = int(block.rect.x / CELL_SIZE), int(block.rect.y / CELL_SIZE)
                if by >= 0 and 0 <= bx < COLUMNS:
                    simulated_field_data[by][bx] = 1

            lines_cleared = 0  # calcular las líneas limpiadas
            for y in range(ROWS):
                if all(simulated_field_data[y]):
                    lines_cleared += 1
                    for clear_y in range(y, 0, -1):
                        simulated_field_data[clear_y] = simulated_field_data[clear_y - 1]
                    simulated_field_data[0] = [0] * COLUMNS

            level = 1  

            moves.append((simulated_field_data, x, rotation, lines_cleared, level))

    # Restablecer la posición original del tetromino
    tetromino.pos.x, tetromino.pos.y = original_x, original_y
    tetromino.shape = deepcopy(original_shape)

    return moves

def alpha_beta_search(field_data, depth, alpha, beta, maximizing_player, tetromino):
    if depth == 0:
        return evaluate_position(field_data, 0, 1, None)

    if maximizing_player:
        max_eval = -float('inf')
        possible_moves = generate_moves(tetromino, field_data)
        for move in possible_moves:
            move_field_data, x, rotation, lines_cleared, level = move
            eval = alpha_beta_search(move_field_data, depth - 1, alpha, beta, False, tetromino)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        possible_moves = generate_moves(tetromino, field_data)
        for move in possible_moves:
            move_field_data, x, rotation, lines_cleared, level = move
            eval = alpha_beta_search(move_field_data, depth - 1, alpha, beta, True, tetromino)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
