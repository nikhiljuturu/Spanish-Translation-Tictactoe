import random
board = list(range(9))
win_seq = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)]

def draw():
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])
    print '\n'
    
def isLegalMove():
    while True:
        a = random.randint(0,8)
        if a in board:
            return a
        else:
            print("\nCell "+ str(a) +" already filled, pick another cell")
            #Cells are indexed from 0 to 8
            
            
def active_game():
    for a, b, c in win_seq:
        if board[a] == board[b] == board[c]:
            print("Player {0} wins!\n".format(board[a]))
            return True
    if sum((pos == 'X' or pos == 'O') for pos in board) == 9:
        print("The game ends in a tie\n")
        return True

def run_game():
    for player in 'XO' * 5:
        draw()
        if active_game():
            break
        print("Player {0} pick your move".format(player))
        board[isLegalMove()] = player
        

run_game()