from math import exp
import random
from time import time

import copy

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
from src.utility import getPlayer, is_win, check_value, check_value2,  place, placeOnBoard

class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        init_temp = 1
        timeLimit = thinking_time
        init_random_state = (random.randint(0, state.board.col-1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        # def place(state: State, n_player: int, shape: str, col: str)
        
        current_move = objectiveFunction(state, n_player, init_random_state)

        # print("results: ", current_move, init_random_state)

        best_movement = init_random_state

        while timeLimit>0:
            annealingTemp = init_temp / (timeLimit)
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
        return check_value2(testBoard, state.players[n_player])
    return -999