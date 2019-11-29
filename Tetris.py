from tkinter import *
from time import sleep
from random import randrange as rand
import pygame, sys


color = ['red', 'orange', 'yellow', 'purple', 'blue', 'green', 'pink']
shape = [
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

colors = [
    (0,   0,   0),
    (255, 85,  85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50,  120, 52),
    (146, 202, 73),
    (150, 161, 218),
    (35,  35,  35)
]
cellSize = 18
cols = 10
rows = 22
maxfps = 30


def rotateClockwise(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


def checkCollision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def removeRow(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board


def joinMatrix(mat1, mat2, mat2Off):
    offX, offY = mat2Off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + offY-1][cx + offX] += val
    return mat1


def newBoard():
    board = [[0 for x in range(cols)]
             for y in range(rows)]
    board += [[1 for x in range(cols)]]
    return board


class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = cellSize*(cols + 6)
        self.height = cellSize*rows
        self.rlim = cellSize*cols
        self.bgroundGrid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]
        self.defaultFont = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.nextStone = shape[rand(len(shape))]
        self.init_game()

    def newStone(self):
        self.stone = self.nextStone[:]
        self.nextStone = shape[rand(len(shape))]
        self.stoneX = int(cols / 2 - len(self.stone[0])/2)
        self.stoneY = 0

        if checkCollision(self.board, self.stone, (self.stoneX, self.stoneY)):
            self.gameOver = True

        self.score += 1

    def init_game(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 400)
        self.board = newBoard()
        self.level = 1
        self.score = 0
        self.lines = 0

        self.gameOver = False
        self.paused = False
        self.newStone()

    def dispMesg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.defaultFont.render(line, False, (255, 255, 255), (0, 0, 0)), (x, y))
            y += 14

    def centerMesg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.defaultFont.render(line, False, (255, 255, 255), (0, 0, 0))
            msgCenterX, msgCenterY = msg_image.get_size()
            msgCenterX //= 2
            msgCenterY //= 2

            self.screen.blit(msg_image, (self.width // 2-msgCenterX, self.height // 2-msgCenterY + i*22))

    def drawMatrix(self, matrix, offset):
        offX, offY = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colors[val], pygame.Rect((offX + x)*cellSize,
                                                                           (offY + y)*cellSize,
                                                                           cellSize,
                                                                           cellSize), 0)

    def addClLines(self, n):
        scores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += scores[n]

    def move(self, deltaX):
        if not self.gameOver and not self.paused:
            newX = self.stoneX + deltaX
            if newX < 0:
                newX = 0
            if newX > cols - len(self.stone[0]):
                newX = cols - len(self.stone[0])
            if not checkCollision(self.board, self.stone, (newX, self.stoneY)):
                self.stoneX = newX

    def quit(self):
        self.centerMesg("Exit")
        pygame.display.update()
        sys.exit()

    def drop(self, manual):
        if not self.gameOver and not self.paused:
            self.stoneY += 1
            if checkCollision(self.board, self.stone, (self.stoneX, self.stoneY)):
                self.board = joinMatrix(self.board, self.stone, (self.stoneX, self.stoneY))
                clearedRows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = removeRow(self.board, i)
                            clearedRows += 1
                            break
                    else:
                        break
                self.addClLines(clearedRows)
                self.newStone()
                return True
        return False

    def instantDrop(self):
        if not self.gameOver and not self.paused:
            while (not self.drop(True)):
                pass

    def rotateStone(self):
        if not self.gameOver and not self.paused:
            new_stone = rotateClockwise(self.stone)
            if not checkCollision(self.board, new_stone, (self.stoneX, self.stoneY)):
                self.stone = new_stone

    def togglePaused(self):
        self.paused = not self.paused

    def startGame(self):
        if self.gameOver:
            self.init_game()
            self.gameOver = False

    def run(self):
        keyActions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.drop(True),
            'UP': self.rotateStone,
            'p': self.togglePaused,
            'SPACE': self.startGame(),
            'RETURN': self.instantDrop()
        }

        self.gameOver = False
        self.paused = False

        deceleration = pygame.time.Clock()

        while 1:
            self.screen.fill((0, 0, 0))
            if self.gameOver:
                self.centerMesg("Game Over\nScore: %d\nPress Space to Continue" % self.score)
            else:
                pygame.draw.line(self.screen,
                                  (255, 255, 255),
                                  (self.rlim+1, 0),
                                  (self.rlim+1, self.height-1))
                self.dispMesg("Next:", (self.rlim+cellSize, 2))
                self.dispMesg("Score: %d\nLevel: %d\nLines: %d" % (self.score, self.level, self.lines),
                              (self.rlim+cellSize, cellSize*5))
                self.drawMatrix(self.bgroundGrid, (0, 0))
                self.drawMatrix(self.board, (0, 0))
                self.drawMatrix(self.stone, (self.stoneX, self.stoneY))
                self.drawMatrix(self.nextStone, (cols+1, 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.bestMoves()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in keyActions:
                        if event.key == eval("pygame.K_"+key):
                            keyActions[key]()

            deceleration.tick(maxfps)

    def bestMoves(self):
        self.instantDrop()

if __name__ == '__main__':
    App = TetrisApp()
    App.run()



