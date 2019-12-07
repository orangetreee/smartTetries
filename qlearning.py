from Tetris import TetrisApp
from state import *
import random as rand

weights = [1, -1, -1, -1, -1]

class QLearning(object):
    def __init__(self, state):
        self.state = state
        self.board = state.board
        self.lineScore = state.score
        self.height = self.getHeight()

    def evaluate(self):
        f0 = self.getLinesCleaned()
        f1 = self.getTotalHeight()
        f2 = self.getMaxHeight()
        f3 = self.getHoles()
        f4 = self.getDeltas()

        score = weights[0]*f0 - weights[1]*f1 - weights[2]*f2 - weights[3]*f3 - weights[4]*f4
        return score

    def getHeight(self):
        height = []
        for x in range(COLS):
            height.append(0)
            for y in range(ROWS):
                if self.board[y][x]:
                    height[x] = ROWS - y
                    break
        return height
    