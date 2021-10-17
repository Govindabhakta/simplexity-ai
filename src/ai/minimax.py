import random
import copy
from time import time
# from functools import lru_cache

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Player, Piece
from src.utility import getPlayer, is_win, check_value, check_value2, place, evaluate

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        state2 = copy.deepcopy(state)
        best_movement = self.minimax(state2, n_player, 3, -999999999999, 999999999999, -1, -1, True)
        # print(best_movement)
        return (best_movement[3], best_movement[1])
        
    def minimax(self, state: State, player: int, depth: int, alpha: int, beta: int, col: int, row: int, maximizing: bool) -> Tuple[int, str, int, int]:
        pos_infinite = 99999999999
        neg_infinite = -99999999999
        win_c = is_win(copy.deepcopy(state.board))
        if depth == 0 or win_c != None or self.thinking_time - time() < 0.1:
            if win_c != None:
                if win_c[1] == state.players[player].color:
                    return [9999999999, state.board[row, col].shape, row, col]
                else: return [-9999999999, state.board[row, col].shape, row, col]

            if maximizing: al = evaluate(state.board, player)
            else: al = evaluate(state.board, 1 - player)  * -1

            return [al, state.board[row, col].shape, row, col]

        if maximizing:
            max_val = neg_infinite
            max_val_piece = max_val_row = max_val_col = None
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
                board2 = copy.deepcopy(state)
                check = place(board2, player, piece, col__)
                val = self.minimax(board2, player, depth - 1, alpha, beta, col__, check, False)
                if val[0] > max_val:
                    max_val, max_val_piece, max_val_row, max_val_col = val
                alpha = max(alpha, val[0])
                if beta <= alpha: break
            return [max_val, max_val_piece, max_val_row, max_val_col]

        else:
            min_val = pos_infinite
            min_val_piece = min_val_row = min_val_col = None
            for col_ in range(state.board.col * 2):
                piece = None
                if col_ % 2 == 0:
                    if (state.players[1 - player].quota[ShapeConstant.CROSS]) > 0:
                        piece = ShapeConstant.CROSS
                    else: continue
                else:
                    if (state.players[1 - player].quota[ShapeConstant.CIRCLE]) > 0:
                        piece = ShapeConstant.CIRCLE
                    else: continue
                col__ = col_ // 2
                board2 = copy.deepcopy(state)
                check = place(board2, 1 - player, piece, col__)
                val = self.minimax(board2, player, depth - 1, alpha, beta, col__, check, True)
                if val[0] < min_val:
                    min_val, min_val_piece, min_val_row, min_val_col = val
                beta = min(beta, val[0])
                if beta <= alpha: break
            return [min_val, min_val_piece, min_val_row, min_val_col]