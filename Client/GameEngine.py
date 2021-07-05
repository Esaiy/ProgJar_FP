DIMENSION = 8

class GameState():
    def __init__(self):
        self.board = [
            ['5v','3v','3v','2v','1v','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
        ]
        self.state = 'placeship'
        
        self.defenseBoard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]

        self.attackBoard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]

    
    def getFinalBoard(self):
        tempBoard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = self.board[r][c]
                if piece != '--':
                    w = int(piece[0])
                    if piece[1] == 'v':
                        for i in range(w):
                            tempBoard[i + r][c] = 1
                    elif piece[1] == 'h':
                        for i in range(w):
                            tempBoard[r][i + c] = 1
        return tempBoard


    def isCollide(self, board):
        tempBoard = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece != '--':
                    w = int(piece[0])
                    if piece[1] == 'v':
                        if w + r > DIMENSION:
                            return True
                        else:
                            for i in range(w):
                                if tempBoard[i + r][c] == 1:
                                    return True
                                tempBoard[i + r][c] = 1
                    elif piece[1] == 'h':
                        if w + c > DIMENSION:
                            return True
                        else:
                            for i in range(w):
                                if tempBoard[r][i + c] == 1:
                                    return True
                                tempBoard[r][i + c] = 1
        return False

    def makeMove(self, move):
        tempBoard = [i.copy() for i in self.board]
        tempBoard[move.startRow][move.startCol] = '--'
        tempBoard[move.endRow][move.endCol] = move.pieceMoved
        if not(self.isCollide(tempBoard)):
            self.board = tempBoard

class Move():
    revPiece = {'v' : 'h', 'h' : 'v'}

    def __init__(self, startSq, endSq, rotate, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceRotate(rotate, board)

    def pieceRotate(self, rotate, board):
        self.pieceMoved = board[self.startRow][self.startCol]
        if rotate:
            self.pieceMoved = self.pieceMoved[0] + self.revPiece[self.pieceMoved[1]]