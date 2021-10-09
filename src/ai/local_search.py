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
        timeLimit = thinking_time

        while timeLimit>0:

            #tobe algorithm
            timeLimit = self.thinking_time - time()

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) 
        return best_movement