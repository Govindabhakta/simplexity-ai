import random
import copy
from time import time
# from functools import lru_cache

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Player, Piece
from src.utility import getPlayer, is_win, check_value, check_value2,  place

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        state2 = copy.deepcopy(state)
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        best_movement = self.minimax(state2, n_player, 5, -9999999, 9999999, -1, -1, True)
        # print(best_movement)
        return (best_movement[3], best_movement[1])

    def minimax(self, state: State, player: int, depth: int, alpha: int, beta: int, col: int, row: int, maximizing: bool) -> Tuple[int, str, int, int]:
        # if self.thinking_time - time() < 0.3:
        pos_infinite = 9999999
        neg_infinite = -9999999

        if depth == 0 or is_win(state.board) or self.thinking_time - time() < 0.1:
            if (player == 0): piece = Piece(GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR)
            else: piece = Piece(GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR)
            win_c = is_win(copy.deepcopy(state.board))
            if win_c != None:
                if maximizing:
                    if win_c[1] == state.players[player].color:
                        return [9999, state.board[row, col].shape, row, col]
                    else: return [-9999, state.board[row, col].shape, row, col]
                else:
                    if win_c[1] == state.players[player].color:
                        return [-9999, state.board[row, col].shape, row, col]
                    else: return [9999, state.board[row, col].shape, row, col]
            
            # al = check_value(state.board, row, col, piece)
            al = check_value2(state.board, player)
            if not maximizing:
                al = al * -1
            return [al, state.board[row, col].shape, row, col]
            
        if maximizing == True:
            max_val = neg_infinite
            max_val_piece = max_val_row = max_val_col = None
            enemy = 1 - player
            for col_ in range(state.board.col * 2):
                piece = None
                if col_ % 2 == 0:
                    if (state.players[player].quota[ShapeConstant.CROSS]) > 0:
                        piece = ShapeConstant.CROSS
                    else: continue
                else:
                    if (state.players[player].quota[ShapeConstant.CIRCLE]) > 0:
                        piece = ShapeConstant.CIRCLE
                    else: continue
                col__ = col_ // 2
                check = place(state, player, piece, col__)
                val = self.minimax(copy.deepcopy(state), enemy, depth - 1, alpha, beta, col__, check, False)
                if val[0] > max_val:
                    max_val, max_val_piece, max_val_row, max_val_col = val
                # if val[0] > alpha: alpha = val[0]
                alpha = max(alpha, val[0])
                # if beta <= alpha: break
                if val[0] >= beta: break
            return [max_val, max_val_piece, max_val_row, max_val_col]
        else:
            min_val = pos_infinite
            min_val_piece = min_val_row = min_val_col = None
            # enemy = 1 - player
            for col_ in range(state.board.col * 2):
                piece = None
                if col_ % 2 == 0:
                    if (state.players[player].quota[ShapeConstant.CROSS]) > 0:
                        piece = ShapeConstant.CROSS
                    else: continue
                else:
                    if (state.players[player].quota[ShapeConstant.CIRCLE]) > 0:
                        piece = ShapeConstant.CIRCLE
                    else: continue
                col__ = col_ // 2
                check = place(state, player, piece, col__)
                val = self.minimax(copy.deepcopy(state), player, depth - 1, alpha, beta, col__, check, True)
                val[0] = (-1 * val[0])
                if val[0] < min_val:
                    min_val, min_val_piece, min_val_row, min_val_col = val
                # if val[0] < beta: beta = val[0]
                beta = min(beta, val[0])
                # if beta <= alpha: break
                if val[0] <= alpha: break
            return [min_val, min_val_piece, min_val_row, min_val_col]