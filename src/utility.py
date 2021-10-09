import pickle
from typing import Tuple
import copy
from src.model import Piece, Board, State, Player
from src.constant import ShapeConstant, ColorConstant, GameConstant


def dump(obj, path):
    """
    [DESC]
        Function to dump Object
    [PARAMS]
        obj: Object -> objects you want dump 
    """
    pickle.dump(obj, open(path, "wb"))


def is_out(board: Board, row: int, col: int) -> bool:
    """
    [DESC]
        Function to see if the piece (row, col) is outside of the board
    [PARAMS]
        board: Board -> current board
        row: int -> row to be checked
        col: int -> column to be checked
    [RETURN]
        True if outside board
        False if inside board
    """
    return row < 0 or row >= board.row or col < 0 or col >= board.col


def is_full(board: Board) -> bool:
    """
    [DESC]
        Function to see if current board is full of pieces
    [PARAMS]
        board: Board -> current board
    [RETURN]
        True if board is full
        False if board is not full
    """
    for row in range(board.row):
        for col in range(board.col):
            if board[row, col].shape == ShapeConstant.BLANK:
                return False
    return True


# **added utility**
def check_value(board: Board, row: int, col: int, piece: Piece) -> int:
    """ 
        [DESC]
            Function for heuristic value of a node (move)
        [PARAMS]
            board: Board -> current board
            row: int -> row for Piece to be placed
            col: int -> column for Piece to be placed
            piece: Piece -> The piece to be placed
        [RETURN]
            Returns the heuristic value of the node in integer
    """
    if piece.shape == ShapeConstant.BLANK:
        return None

    streak_way = [(1, 0), (0, 1), (-1, 1), (1, 1)]

    max_val = -1
    for row_ax, col_ax in streak_way:
        skip1 = skip2 = skip3 = skip4 = False
        val = 0
        val_ = 0
        row_ = row + row_ax
        row__ = row - row_ax
        col_ = col + col_ax
        col__ = col - col_ax
        for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
            if not is_out(board, row_, col_):
                if board[row_, col_].shape == piece.shape and not skip1:
                    val += 1
                else: skip1 = True
                if board[row_, col_].color == piece.color and not skip2:
                    val_ += 1
                else: skip2 = True
            if not is_out(board, row__, col__):
                if board[row__, col__].shape == piece.shape and not skip3:
                    val += 1
                else: skip3 = True
                if board[row__, col__].color == piece.color and not skip4:
                    val_ += 1
                else: skip4 = True
            row_ += row_ax
            col_ += col_ax
            row__ -= row_ax
            col__ -= col_ax
        if max_val < val or max_val < val_:
            if val < val_: max_val = val_
            else: max_val = val
    return max_val

#added utility
def check_value2(board: Board, player: Player) -> int:
    score = -99999
    for col in range(board.col):
        pos_x, pos_y = getTopCoordinate(board,col)
        if (pos_x, pos_y == (-1, -1)):
            break
        for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
            score = max(evaluateScore(pos_x,pos_y,board,player.shape,player.color,shape),score)
    return score


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

def getPlayer(state: State):
    if state.round % 2 == 0: #maximizing
        return state.players[0]
    else: 
        return state.players[1]

#def isCloseToStreak(board: Board, row: int, col: int, shape: str, color: str)

def check_streak(board: Board, row: int, col: int) -> Tuple[str, str, str]:
    """
    [DESC]
        Function to check streak from row, col in current board
    [PARAMS]
        board: Board -> current board
        row: int -> row
        col: int -> column
    [RETURN]
        None if the row, col in a board isn't filled with piece
        Tuple[prior, shape, color] match with player set if streak found and cause of win
    """
    piece = board[row, col]
    if piece.shape == ShapeConstant.BLANK:
        return None

    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for prior in GameConstant.WIN_PRIOR:
        mark = 0
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, row_, col_):
                    mark = 0
                    break

                shape_condition = (
                    prior == GameConstant.SHAPE
                    and piece.shape != board[row_, col_].shape
                )
                color_condition = (
                    prior == GameConstant.COLOR
                    and piece.color != board[row_, col_].color
                )
                if shape_condition or color_condition:
                    mark = 0
                    break

                row_ += row_ax
                col_ += col_ax
                mark += 1

            if mark == GameConstant.N_COMPONENT_STREAK - 1:
                player_set = [
                    (GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR),
                    (GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR),
                ]
                for player in player_set:
                    if prior == GameConstant.SHAPE:
                        if piece.shape == player[0]:
                            return (prior, player)
                            
                    elif prior == GameConstant.COLOR:
                        if piece.color == player[1]:
                            return (prior, player)


def is_win(board: Board) -> Tuple[str, str]:
    """
    [DESC]
        Function to check if player won
    [PARAMS]
        board: Board -> current board
    [RETURN]
        None if there is no streak
        Tuple[shape, color] match with player set if there is a streak
    """
    temp_win = None
    for row in range(board.row):
        for col in range(board.col):
            checked = check_streak(board, row, col)
            if checked:
                if checked[0] == GameConstant.WIN_PRIOR[0]:
                    return checked[1]
                else:
                    temp_win = checked[1]
    return temp_win


def place(state: State, n_player: int, shape: str, col: str) -> int:
    """
    [DESC]
        Function to place piece in board
    [PARAMS]
        state = current state in the game
        n_player = which player (player 1 or 2)
        shape = shape
        col = which col
    [RETURN]
        -1 if placement is invalid
        int(row) if placement is valid 
    """
    if state.players[n_player].quota[shape] == 0:
        return -1

    for row in range(state.board.row - 1, -1, -1):
        if state.board[row, col].shape == ShapeConstant.BLANK:
            piece = Piece(shape, GameConstant.PLAYER_COLOR[n_player])
            state.board.set_piece(row, col, piece)
            state.players[n_player].quota[shape] -= 1
            return row

    return -1

def placeOnBoard(state: State, board: Board, n_player: int, shape: str, col: str):
    if state.players[n_player].quota[shape] == 0:
        return -1

    for row in range(state.board.row - 1, -1, -1):
        if state.board[row, col].shape == ShapeConstant.BLANK:
            piece = Piece(shape, GameConstant.PLAYER_COLOR[n_player])
            board.set_piece(row, col, piece)
            return board
    return -1
