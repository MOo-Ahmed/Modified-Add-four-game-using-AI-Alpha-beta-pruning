import math
import random

import Board


class Game:

    def __init__(self, startingIndex, maxScore, maxMoves, gameState):
        self.numOfMoves = 0
        self.maxDepth = 7
        self.maxMoves = maxMoves
        self.maxScore = maxScore
        self.board = Board.Board(startingIndex, maxScore, maxMoves, gameState)

    def getValidMoves(self, current):
        '''
        This function returns the indexes to which the player can move
        :param current: the current position of player Max
        :return: a list of valid indexes
        '''
        moves = [1, 3, -1, -3]
        result = []
        for i in range(0, 4):
            if self.is_valid(current.indexOfPlayer1, current.indexOfPlayer1 + moves[i]) == True:
                result.append(moves[i] + current.indexOfPlayer1)
        moves2 = []
        for i in range(0, len(result)):
            if current.current_state[result[i]] == 1:
                moves2.append(result[i])

        for i in range(0, len(result)):
            try:
                idx = moves2.index(result[i])
            except:
                moves2.append(result[i])
        return moves2

    def getMaxChildren(self, current):
        moves = self.getValidMoves(current)
        children = []
        for i in range(0, len(moves)):
            board = current.getMaxCopy(moves[i])
            children.append(board)
        return children

    def is_valid(self, current, new):
        if new < 0 or new > 8:
            return False
        elif current % 3 == 0 and new == current - 1:  # first column
            return False
        elif (current + 1) % 3 == 0 and new == current + 1:  # last column
            return False
        elif current < 3 and new == current - 3:  # first row
            return False
        elif current > 5 and new == current + 3:  # last row
            return False
        else:
            return True

    def is_end(self, Board):
        if Board.numOfMoves == self.maxMoves:
            score = Board.scoreOfPlayer1
            moves = Board.numOfMoves
            if score >= self.maxScore:
                return 'Max', score, moves
            else:
                return 'Min', score, moves
        else:
            return 'No', 0, 0

    def getDirection(self, current, newIdx):
        if newIdx == current + 1:
            return 'RIGHT'
        elif newIdx == current + 3:
            return 'DOWN'
        elif newIdx == current - 1:
            return 'LEFT'
        elif newIdx == current - 3:
            return 'UP'

    def play(self, node, depth, alpha, beta, Player):
        H1 = [node.indexOfPlayer1]
        H2 = []
        while True:

            isTerminal, score, moves = self.is_end(node)
            if isTerminal != 'No':
                return node.scoreOfPlayer1, node.numOfMoves, H1, H2

            if Player == 'Max':
                oldScore = node.scoreOfPlayer1
                oldIdx1 = node.indexOfPlayer1
                oldMoves = node.numOfMoves
                oldState = node.current_state.copy()

                res, moves, history1, history2, choice = self.Max(node, depth, alpha, beta)
                H1.append(choice)

                node.indexOfPlayer2 = oldIdx1
                node.indexOfPlayer1 = choice
                node.current_state = oldState
                node.scoreOfPlayer1 = oldScore
                node.numOfMoves = oldMoves

                node.current_state[choice] += node.scoreOfPlayer1
                node.scoreOfPlayer1 = node.current_state[choice]
                node.numOfMoves += 1
                Player = 'Min'
            else:
                oldScore = node.scoreOfPlayer1
                oldIdx1 = node.indexOfPlayer1
                oldIdx2 = node.indexOfPlayer2
                oldMoves = node.numOfMoves
                oldState = node.current_state.copy()

                res, moves, history1, history2, choice = self.Min(node, depth, alpha, beta)
                node.indexOfPlayer1 = oldIdx1
                node.indexOfPlayer2 = oldIdx2
                node.current_state = oldState.copy()
                node.scoreOfPlayer1 = oldScore
                node.numOfMoves = oldMoves
                node.current_state[node.indexOfPlayer2] = choice
                H2.append(choice)
                Player = 'Max'

    def Max(self, node, depth, alpha, beta):
        isTerminal, score, moves = self.is_end(node)
        if depth == self.maxDepth or isTerminal != 'No':
            return score, moves, node.historyOfP1, node.historyOfP2, 0

        H1 = []
        H2 = []
        bestMoves = -1
        value = - math.inf
        possiblePositions = self.getValidMoves(node)
        index = possiblePositions[0]
        children = self.getMaxChildren(node)
        for i in range(0, len(children)):
            child = children[i]
            res, moves, history1, history2, choice = self.Min(child, depth + 1, alpha, beta)
            if value < res:
                bestMoves = moves
                H1 = history1.copy()
                H2 = history2.copy()
                index = possiblePositions[i]

            elif value == res and moves > bestMoves:
                bestMoves = moves
                H1 = history1.copy()
                H2 = history2.copy()
                index = possiblePositions[i]
            value = max(value, res)
            alpha = max(alpha, value)
            if alpha >= beta:
                # Beta cut off
                break
        return value, bestMoves, H1, H2, index

    def Min(self, node, depth, alpha, beta):
        H1 = []
        H2 = []
        bestMoves = -1
        value = math.inf
        values = [1, -1, 0]
        rand = random.randint(0, 2)
        choice = values[rand]
        child = node.getMinCopy(choice)
        res, moves, history1, history2, idx = self.Max(child, depth, alpha, beta)
        if value > res:
            bestMoves = moves
            H1 = history1.copy()
            H2 = history2.copy()
        elif value == res and moves < bestMoves:
            bestMoves = moves
            H1 = history1.copy()
            H2 = history2.copy()

        value = min(value, res)
        beta = min(beta, value)

        return value, bestMoves, H1, H2, choice

    def startGame(self):
        b = self.board.getCopy()
        value, moves, h1, h2 = self.play(self.board, 0, -math.inf, math.inf, 'Max')
        self.displayHistory(h1, h2, b, value, moves)

    def displayHistory(self, h1, h2, board, score, moves):
        h1 = h1.copy()
        h2 = h2.copy()
        print("\t\tThis is the initial state of our board:")
        print("Player 1 is initially at position ", h1[0])
        board.draw_board()
        print()
        start = h1[0]
        current = h1[1]
        score2 = board.current_state[start]
        del h1[0]
        for i in range(0, len(h1)):
            if i != 0:
                start = h1[i - 1]
                current = h1[i]
            direction = self.getDirection(start, current)
            print("At the turn of MAX, he moved ", direction, "  .. to index ", current)
            board.current_state[current] += score2
            score2 = board.current_state[current]
            print("The board becomes : ")
            board.draw_board()
            if i != len(h1) - 1:
                print("At the turn of MIN, he chose the value ", h2[i])
                board.current_state[start] = h2[i]
                print("The board becomes : ")
                board.draw_board()
        print("\nPlayer 1 scored ", score2, " points within ", len(h1), " moves")
        if score2 >= self.maxScore:
            print("Player1 wins ...")
        else:
            print("Player1 loses ...")
            
    def getMinChildren(self, current):
        values = [0, -1, 1]
        children = []
        for i in range(0, 3):
            child = current.getMinCopy(values[i])
            children.append(child)
        return children

    
