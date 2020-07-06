import game


gameState = []
# 1,-1,0,1,0,1,0,1,-1
# 1,0,1,0,1,1,-1,-1,1
# 1,0,-1,0,-1,1,1,-1,1
initial_position = int(input("Enter the initial position of MAX : "))
miniScore = int(input("Enter the minimal score level : "))
maxMoves = int(input("Enter the maximum number of moves : "))
input_string = (input("Enter the initial game state as 1D matrix : "))
_list = input_string.split(",")
for i in range(0, 9):
    gameState.append(int(_list[i]))

g = game.Game(initial_position, miniScore, maxMoves, gameState)
g.startGame()

