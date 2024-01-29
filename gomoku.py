"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

# Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

def is_empty(board):
    """
    Checks if the Gomoku board is empty.

    Parameters:
    - board: 2D list representing the Gomoku board.

    Returns:
    - True if the board is empty, False otherwise.
    """
    # Check if the given board is equal to the result of make_empty_board with the same size
    # This is a simple way to determine if the board is empty, as it compares with a newly created empty board
    if board == make_empty_board(len(board[1])):
        return True
    else:
        return False

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """
    Determines the bounding status of a sequence on the Gomoku board.

    Parameters:
    - board: 2D list representing the Gomoku board.
    - y_end: Ending y-coordinate of the sequence.
    - x_end: Ending x-coordinate of the sequence.
    - length: Length of the sequence being checked.
    - d_y: Direction of movement along the y-axis (1 for downward, -1 for upward, 0 for no movement).
    - d_x: Direction of movement along the x-axis (1 for right, -1 for left, 0 for no movement).

    Returns:
    - "OPEN" if the sequence is open (both ends are unblocked),
    - "SEMIOPEN" if the sequence is semi-open (one end is unblocked),
    - "CLOSED" if the sequence is closed (neither end is unblocked).
    """
    # Initialize a counter to track the number of unblocked ends
    count = 0

    # Check if the square on the next position in the sequence exists and is blank
    if 0 <= y_end + d_y < len(board) and 0 <= x_end + d_x < len(board[y_end + d_y]) and board[y_end + d_y][x_end + d_x] == ' ':
        # If the next square in the sequence exists and is blank, increment the counter
        count += 1

    # Check if the square on the previous position in the sequence exists and is blank
    if 0 <= y_end - length * d_y < len(board) and 0 <= x_end - length * d_x < len(board[y_end - length * d_y]) and board[y_end - length * d_y][x_end - length * d_x] == ' ':
        # If the previous square in the sequence exists and is blank, increment the counter
        count += 1

    # Based on the count, determine the bounding status of the sequence
    if count == 2:
        return "OPEN"
    elif count == 1:
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    y = y_start
    x = x_start
    sub_length = 0
    for i in range(len(board)):
        if board[y][x] == col:
            sub_length += 1
        if y + d_y >= len(board) or 0 > y + d_y or 0 > x + d_x or x + d_x >= len(board) or board[y+d_y][x+d_x] != col:
            
            if sub_length == length:
                result = is_bounded(board, y, x, length, d_y, d_x)
                
                if result == "OPEN":
                    open_seq_count += 1
                elif result == "SEMIOPEN":
                    semi_open_seq_count += 1
            sub_length = 0
        
        if y + d_y == len(board) or x + d_x == len(board):
            break
        y += d_y
        x += d_x
    return open_seq_count, semi_open_seq_count

    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    d = [[0,1],[1,0],[1,1],[1,-1]]
    for x in d:
        d_y, d_x = x
        # (int(not d)) basically switches 1 or -1 to 0 and 0 to 1
        for i in range(len(board)):
            if abs(d_y) != abs(d_x):
                open, semi = detect_row(board, col, i*(int(not abs(d_y))), i*(int(not abs(d_x))), length, d_y, d_x)
            # It's useless to try to find a row of a certain length on some diagonals that aren't long enough
            # abs(min(0, d_x*7)) + length*d_x < len(board)
            else:
                open, semi = detect_row(board, col, 0, i, length, d_y, d_x)
                if i != 0:
                    sol = detect_row(board, col, i, abs(min(0, d_x*(len(board)-1))), length, d_y, d_x)
                    open += sol[0]
                    semi += sol[1]
            open_seq_count += open
            semi_open_seq_count += semi

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    count = 0
    move_y, move_x = 0, 0

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == ' ':
                count += 1
                board[y][x] = "b"
                new_score = score(board)
                if count == 1 or new_score > prev_score:
                    prev_score = new_score
                    move_y, move_x = y, x
                board[y][x] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    dic = {"w": "White won", "b": "Black won", "draw": "Draw", "continue": "Continue playing"}
    players = ['b', 'w']
    addition = [' '] + [' ']*len(board) + [' ']

    for col in players:
        hyp_board = []
        for i in range(len(board)):
            hyp_board.append([' '] + board[i].copy() + [' '])
        hyp_board.insert(0,addition)
        hyp_board.append(addition)
        for row in range(len(hyp_board)):
            for column in range(len(hyp_board[row])):
                if hyp_board[row][column] != col:
                    hyp_board[row][column] = ' '
        win = detect_rows(hyp_board, col, 5)
        if win != (0,0):
            return dic[col]
    test_empty = 0
    for a in board:
        for b in a:
            if b == " ":
                test_empty += 1
    if test_empty == 0:
        return dic["draw"]
    else:
        return dic["continue"]


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0



if __name__ == '__main__':
    play_gomoku(8)
