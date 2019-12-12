import copy


def newBoard():
    board = [[0 for _ in range(COLS)]
             for __ in range(ROWS)]
    board += [[1 for _ in range(COLS)]]
    return board


class State(object):
    def __init__(self, board, score, block, nextBlock):
        self.board = board
        self.score = score
        self.block = block
        self.nextBlock = nextBlock
        self.newScore = score

    def checkCollision(self, block, offset):
        board = self.board
        x, y = offset
        for blockY, row in enumerate(block):
            for blockX, pixel in enumerate(row):
                try:
                    if pixel and board[blockY + y][blockX + x]:
                        return True
                except IndexError:
                    return True
        return False

    def rotate(self, block, N):
        for _ in range(N):
            block = [[block[y][x]
                      for y in range(len(block))]
                     for x in range(len(block[0]) -1, -1, -1)]
        return block

    def removeRow(self, board):
        clearedRows = 0
        for i, row in enumerate(board[:-1]):
            if 0 not in row:
                del board[i]
                board = [[0 for i in range(COLS)]] + board
                clearedRows += 1
        self.addScore(clearedRows)
        return board

    def drop(self, block, x):
        y = 0
        while not self.checkCollision(block, (x, y)):
            y += 1
        return self.removeRow(self.addBlock(block, (x, y-1)))

    def addBlock(self, block, offset):
        board = copy.deepcopy(self.board)
        x, y = offset
        for blockY, row in enumerate(block):
            for blockX, pixel in enumerate(row):
                board[blockY + y][blockX + x] += pixel
        return board

    def addScore(self, n):
        lineScores = [0, 40, 100, 300, 1200]
        self.newScore = lineScores[n]

    def nextState(self, action):
        rotate, x = action
        newStates = []
        block = self.rotate(self.block, rotate)
        if not self.checkCollision(block, (x, 0)):
            newBoard = self.drop(block, x)
            newScore = self.newScore
            newBlock = self.nextBlock
            for newNextBlock in blocks:
                newState = State(newBoard, newScore, newBlock, newNextBlock)
                newStates.append(newState)
        return newStates


COLS = 10
ROWS = 22

blocks = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

if __name__ == '__main__':
    testBoard = \
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    testState = State(testBoard, 0, blocks[0], blocks[1])
    print(testState.nextState((1, 2))[0].board)
    print(testState.board)
    print(testState.nextState((1, 2))[0].score)
    print(testState.nextState((1, 2))[0].block)

