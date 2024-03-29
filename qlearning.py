from Tetris import TetrisApp
from state import *
import random as rand
import math

weights = [1, -1, -1, -1, -1]
Epsilon = 0.05
Alpha = 0.075
qVal = {}


class QLearning(object):
    def __init__(self, state):
        self.state = state
        self.board = state.board
        self.lineScore = state.score
        self.heights = self.getHeight()
        self.score = self.evaluate()

    def evaluate(self):
        f0 = self.getLinesCleaned()
        f1 = self.getTotalHeight()
        f2 = self.getMaxHeight()
        f3 = self.getHoles()
        f4 = self.bumpiness()

        score = -0.520162*f1 + 0.771727*f0 - 0.36483*f3 - 0.183434*f4
        # score = weights[0]*f0 - weights[1]*f1 - weights[3]*f3 - weights[4]*f4
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

    def getTotalHeight(self):
        return sum(self.heights)

    def getMaxHeight(self):
        return sum(self.heights)

    def getLinesCleaned(self):
        s = [0, 40, 100, 300, 1200]
        if self.lineScore in s:
            return ([0, 40, 100, 300, 1200]).index(self.lineScore)
        else:
            return 0

    def bumpiness(self):
        sum = 0
        for i, j in enumerate(self.heights):
            if i:
                sum += abs(self.heights[i] - self.heights[i-1])
        return sum

    def getHoles(self):
        res = 0
        for i in range(COLS):
            flag = False
            for j in range(ROWS):
                if self.board[j][i] != 0:
                    flag = True
                elif flag:
                    res += 1
        return res


class TetrisQL(TetrisApp):
    def bestMoves(self):
        bestScore, bestAction = float("-inf"), None
        iniState = State(self.board, self.score, self.stone, self.nextStone)

        if rand.random() < Epsilon:
            rotate = rand.randrange(4)
            if rotate & 1:
                maxX = COLS - len(iniState.block) + 1
            else:
                maxX = COLS - len(iniState.block[0]) + 1
            x = rand.randrange(maxX)
            action = (rotate, x)
            nextState = iniState.nextState(action)
            if len(nextState):
                nextState = nextState[0]
                for i, j in enumerate(weights):
                    weights[i] += Alpha * (nextState.score + QLearning(nextState).evaluate() - QLearning(iniState).evaluate())
        else:
            for rotate in range(4):
                for x in range(COLS):
                    action = (rotate, x)
                    nextState = iniState.nextState(action)
                    if len(nextState):
                        score = QLearning(nextState[0]).score
                        if score > bestScore:
                            bestScore, bestAction = score, action

            nextState = iniState.nextState(bestAction)
            if len(nextState):
                nextState = nextState[0]
                for i, j in enumerate(weights):
                    weights[i] += Alpha * (nextState.score + QLearning(nextState).evaluate() - QLearning(iniState).evaluate())

        for rotate in range(4):
            for x in range(COLS):
                action = (rotate, x)
                nextState = iniState.nextState(action)
                if len(nextState):
                    score = QLearning(nextState[0]).score
                    if score > bestScore:
                        bestScore, bestAction = score, action

        if not self.gameOver:
            for _ in range(bestAction[0]):
                self.rotateStone()
            self.move(bestAction[1] - self.stoneX)
            self.instantDrop()


if __name__ == '__main__':
    app = TetrisQL()
    app.run()