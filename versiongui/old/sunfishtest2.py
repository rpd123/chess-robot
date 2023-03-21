print ("hi")
import sunfish
print ("ho")
# Initialize the chess board
board = sunfish.Board()

# Define a function to print the board state
def print_board(board):
    print("\n".join(board.pretty().split("\n")[::-1]))

# Play a simple game of chess
while not board.is_game_over():
    print_board(board)

    # Get the player's move
    move = input("Enter your move (e.g. e2e4): ")
    
    # Make the move
    if move:
        board.push(sunfish.parse(move))

    # Get the computer's move
    if not board.is_game_over():
        move = sunfish.search(board, depth=4)
        board.push(move)

# Print the final board state and result
print_board(board)
print("Result:", board.result())