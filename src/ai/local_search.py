from math import exp
import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        init_temp = 1
        timeLimit = thinking_time
        init_random_state = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        current_move = objectiveFunction(init_random_state)
        best_movement = init_random_state

        while timeLimit>0:
            annealingTemp = init_temp / (timeLimit)
            new_state = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            new_neighbor_value = objectiveFunction(new_state)
            if (new_neighbor_value>current_move):
                best_movement = new_state
            else:
                efunction = exp(new_neighbor_value-current_move/annealingTemp)
                if random.random() < efunction:
                    best_movement = new_state
            timeLimit = self.thinking_time - time()

        return best_movement
