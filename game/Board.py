class Board:

    def __init__(self, startingIndex, maxMoves, maxScore, gameState):
        self.indexOfPlayer1 = startingIndex
        self.indexOfPlayer2 = startingIndex
        self.numOfMoves = 0

        self.maxMoves = maxMoves
        self.maxScore = maxScore
        self.current_state = gameState
        self.scoreOfPlayer1 = self.current_state[self.indexOfPlayer1]
        self.historyOfP1 = [self.indexOfPlayer1]
        self.historyOfP2 = []

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('\t{}\t|'.format(self.current_state[i * 3 + j]), end=" ")
            print()
        print()

    def getMaxCopy(self, newIndexOfP1):
        '''
        This function takes the new position that Max will move to.
        Then it returns a new board with new values to indicate the move of Max
        '''
        board = Board(self.indexOfPlayer1, self.maxMoves, self.maxScore, self.current_state.copy())
        board.indexOfPlayer1 = newIndexOfP1
        board.current_state = self.current_state.copy()
        board.numOfMoves = self.numOfMoves + 1
        board.scoreOfPlayer1 = self.scoreOfPlayer1 + board.current_state[board.indexOfPlayer1]
        board.current_state[board.indexOfPlayer1] = board.scoreOfPlayer1
        board.historyOfP1 = self.historyOfP1.copy()
        board.historyOfP1.append(newIndexOfP1)
        board.historyOfP2 = self.historyOfP2.copy()
        return board

    def getMinCopy(self, newValue):
        board = Board(self.indexOfPlayer1, self.maxMoves, self.maxScore, self.current_state.copy())
        board.indexOfPlayer2 = self.indexOfPlayer2
        board.current_state = self.current_state.copy()
        board.numOfMoves = self.numOfMoves
        board.scoreOfPlayer1 = self.scoreOfPlayer1
        board.current_state[board.indexOfPlayer2] = newValue
        board.historyOfP1 = self.historyOfP1.copy()
        board.historyOfP2 = self.historyOfP2.copy()
        board.historyOfP2.append(newValue)

        return board

    def printMyProperties(self):
        print("index of p1 = ", self.indexOfPlayer1, "..\tindex of p2 = ", self.indexOfPlayer2)
        print("Current score = ", self.scoreOfPlayer1, "..\tCurrent moves = ", self.numOfMoves)
        print("Current score at board = ", self.current_state[self.indexOfPlayer1])
        print(self.historyOfP1)
        print(self.historyOfP2)

    def getCopy(self):
        board = Board(self.indexOfPlayer1, self.maxMoves, self.maxScore, self.current_state.copy())
        board.numOfMoves = self.numOfMoves
        board.scoreOfPlayer1 = self.scoreOfPlayer1
        board.current_state[board.indexOfPlayer1] = board.scoreOfPlayer1
        board.historyOfP1 = self.historyOfP1.copy()
        board.historyOfP2 = self.historyOfP2.copy()
        return board
