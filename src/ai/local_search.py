from math import exp
import random
from time import time

import copy

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Player

from typing import Tuple, List
from src.utility import placeOnBoard, is_out

#added utility
def getTopCoordinate(board: Board, col: int) -> Tuple[int,int]:
    y = 0
    while y < board.row:
        if board[y,col].shape == ShapeConstant.BLANK: return [y,col]
        y += 1
    return (-1, -1)

#added utility
def evaluateScore(pos_x: int, pos_y: int, board: Board, playershape: str, playercolor: str, shape: str) -> int:
    streak_way = [(1, 0), (0, 1), (-1, 1), (1, 1)]

    player_val = 1
    enemy_val = 0
    if (shape != playershape): enemy_val += 1

    for row_ax, col_ax in streak_way:

        skip1 = skip2 = skip3 = skip4 = skip5 = skip6 = False

        playerstreakShape = 0
        playerstreakColor = 1
        enemystreak = 0 # shape-based

        if shape == playershape: 
            playerstreakShape += 1
        else: 
            enemystreak += 1

        row_ = pos_y + row_ax
        row__ = pos_y - row_ax
        col_ = pos_x + col_ax
        col__ = pos_x - col_ax

        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
            if not is_out(board, row_, col_):
                if board[row_, col_].shape == shape and playershape == shape and not skip1:
                    player_val += 1
                    playerstreakShape += 1
                else: skip1 = True
                if board[row_, col_].color == playercolor and not skip2:
                    player_val += 1
                    playerstreakColor += 1
                else: skip2 = True
                if board[row_, col_].shape == shape and shape != playershape and not skip3:
                    enemy_val -= 1
                    enemystreak += 1
                else: skip2 = True
            if not is_out(board, row__, col__):
                if board[row__, col__].shape == shape and playershape == shape and not skip4:
                    player_val  += 1
                    playerstreakColor += 1
                else: skip4 = True
                if board[row__, col__].color == playercolor and not skip5:
                    player_val  += 1
                    playerstreakColor += 1
                else: skip5 = True
                if board[row_, col_].color == shape and shape != playershape and not skip6:
                    enemy_val -= 1
                    enemystreak += 1
                else: skip6 = True

            if playerstreakColor == GameConstant.N_COMPONENT_STREAK or playerstreakShape == GameConstant.N_COMPONENT_STREAK:
                return 9999
            elif enemystreak == GameConstant.N_COMPONENT_STREAK:
                return 999

            row_ += row_ax
            col_ += col_ax
            row__ -= row_ax
            col__ -= col_ax
    return player_val - enemy_val

#added utility
def check_value(board: Board, player: Player) -> int:
    score = -99999
    for col in range(board.col):
        pos_x, pos_y = getTopCoordinate(board,col)
        if (pos_x, pos_y == (-1, -1)):
            break
        for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
            score = max(evaluateScore(pos_x,pos_y,board,player.shape,player.color,shape),score)
    return score

class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        init_temp = 1
        timeLimit = thinking_time
        init_random_state = (random.randint(0, state.board.col-1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        current_move = objectiveFunction(state, n_player, init_random_state)
        best_movement = init_random_state

        while timeLimit>0:
            annealingTemp = init_temp / (3.01 - timeLimit)
            new_state = (random.randint(0, state.board.col-1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            new_neighbor_value = objectiveFunction(state, n_player, new_state)
            if (new_neighbor_value>current_move):
                best_movement = new_state
            else:
                try:
                    efunction = exp(new_neighbor_value-current_move/annealingTemp)
                except OverflowError:
                    efunction = float('inf')
                if random.random() < efunction:
                    best_movement = new_state
            timeLimit = self.thinking_time - time()
            # print("results: ", current_move, init_random_state)

        return best_movement

def objectiveFunction(state, n_player, decision):
    # print("HAHAHA", decision[0])
    testBoard = placeOnBoard(state, copy.deepcopy(state.board), n_player, decision[1], decision[0])

    if (testBoard != -1): 
        return check_value(testBoard, state.players[n_player])
    return -999