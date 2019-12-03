from Tetris import TetrisApp

class TetrisMiniHeight(TetrisApp):
    def bestMoves(self):
        x, low = 0, 0
        for j in range(len(self.board[0])):
            i = 0
            while not self.board[i][j]:
                i += 1
            if i > low:
                x, low = j, i

        self.move(x - self.stoneX)
        self.instantDrop()

if __name__ == '__main__':
    app = TetrisMiniHeight()
    app.run()