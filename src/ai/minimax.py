import random
import copy
from time import time
# from functools import lru_cache

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Piece
from src.utility import is_win, place, evaluate, is_out

from typing import Tuple, List

def check(board: Board, row: int, col: int, piece: Piece, player_piece: Piece) -> int:
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    score = 0
    for row_ax, col_ax in streak_way:
        row_ = row + row_ax
        col_ = col + col_ax
        score_s = 1
        score_c = 1
        if not is_out(board, row - row_ax, col - col_ax) and \
            board[row - row_ax, col - col_ax].shape == ShapeConstant.BLANK:
                left_blank = True
        else: left_blank = False
        encounter_blank = False
        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
            if is_out(board, row_, col_):
                break
            pos = board[row_, col_]
            if pos.shape == ShapeConstant.BLANK:
                encounter_blank = True
                continue
            if pos.shape == piece.shape:
                if score_s == 2 and encounter_blank:
                    if piece.shape != player_piece.shape: score_s += 99
                    else: score_s += 10
                elif score_s == 2 and not encounter_blank:
                    if left_blank:
                        if piece.shape != player_piece.shape: score_s += 99
                        else: score_s += 10
                    elif board[row + row_ax, col + col_ax].shape != player_piece.shape:
                        score_s += 2
                    elif not is_out(board, row + (2 * row_ax), col + (2 * col_ax)) and \
                        board[row + (2 * row_ax), col + (2 * col_ax)].shape != player_piece.shape:
                            score_s += 2
                    else: score_s += 2
                else: score_s += 1
            if pos.color == piece.color:
                if score_c == 2 and encounter_blank:
                    if piece.color != player_piece.color: score_c += 95
                    else: score_c += 9
                elif score_c == 2 and not encounter_blank:
                    if left_blank:
                        if piece.color != player_piece.color: score_c += 95
                        else: score_c += 9
                    elif board[row + row_ax, col + col_ax].color != player_piece.color:
                        score_c += 2
                    elif not is_out(board, row + (2 * row_ax), col + (2 * col_ax)) and \
                        board[row + (2 * row_ax), col + (2 * col_ax)].shape != player_piece.shape:
                            score_c += 2
                    else: score_c += 2
                else: score_c += 1
        if piece.shape == player_piece.shape: score += score_s
        else: score -= score_s
        if piece.color == player_piece.shape: score += score_c
        else: score -= score_c
    return score

#added utility evaluate
def evaluate(board: Board, player: int) -> int:
    # values = []
    # piece = []
    if player == 0:
        piece_s = GameConstant.PLAYER1_SHAPE
        piece_c = GameConstant.PLAYER1_COLOR
    else:
        piece_s = GameConstant.PLAYER2_SHAPE
        piece_c = GameConstant.PLAYER2_COLOR
    score = 0
    piece_p = Piece(piece_s, piece_c)
    for col in range(board.col):
        for row in range(board.row - 1, -1, -1):
            if board[row, col].shape == ShapeConstant.BLANK: break
            # score = check_value(board, row, col, board[row, col])
            score += check(board, row, col, board[row, col], piece_p)
    return score

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