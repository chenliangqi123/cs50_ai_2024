"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counts = 0
    o_counts = 0
    for row in board:
        for element in row:
            if element == "X":
                x_counts += 1
            elif element == "O":
                o_counts += 1
    if x_counts == o_counts:
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j]:
        raise Exception("already had elements on (i, j)")
    elif i > 2 or i < 0 or j > 2 or j < 0:
        raise Exception("out-of-bounds move")
    else:
        deep_copied_board = copy.deepcopy(board)
        deep_copied_board[i][j] = player(deep_copied_board)
    return deep_copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if all(cell == "X" for cell in row):
            return X
        elif all(cell == "O" for cell in row):
            return O

    for j in range(3):
        if all(board[i][j] == "X" for i in range(3)):
            return X
        elif all(board[i][j] == "O" for i in range(3)):
            return O

    if all(board[i][i] == "X" for i in range(3)):
        return X
    elif all(board[i][i] == "O" for i in range(3)):
        return O

    if all(board[i][2-i] == "X" for i in range(3)):
        return X
    elif all(board[i][2-i] == "O" for i in range(3)):
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for element in row:
            if not element:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if X == winner(board):
        return 1
    elif O == winner(board):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    x_action = None
    o_action = None

    def Max_Value(state):
        nonlocal x_action
        if terminal(state):
            return utility(state)

        v = -math.inf

        for action in actions(state):
            if Min_Value(result(state, action)) > v:
                v = Min_Value(result(state, action))
                x_action = action
                # v = max(v, Min_Value(result(state, action)))
        return v

    def Min_Value(state):
        nonlocal o_action
        if terminal(state):
            return utility(state)

        v = math.inf

        for action in actions(state):
            if Max_Value(result(state, action)) < v:
                v = Max_Value(result(state, action))
                o_action = action
            # v = max(v, Max_Value(result(state, action)))
        return v

    if player(board) == X:
        Max_Value(board)
        return x_action
    else:
        Min_Value(board)
        return o_action
