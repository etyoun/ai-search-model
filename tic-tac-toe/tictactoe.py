"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None
INFINITY = 1e3


class InvalidAction(Exception):
    "Raised when the action is not available"
    pass


def initial_state():
    """
    Return starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Return player who has the next turn on a board.

    X starts the game.
    """
    # Initialize counters
    X_counter = 0
    O_counter = 0

    for each_row in board:
        # Row-wise count of each X and O's
        X_counter += each_row.count(X)
        O_counter += each_row.count(O)

    # O plays if and only if it has less turns on board
    if O_counter < X_counter:
        return O

    return X


def actions(board):
    """
    Return set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for row_index, row in enumerate(board):
        for col_index, value in enumerate(row):
            if value not in (X, O):
                action_set.add((row_index, col_index))

    return action_set


def result(board, action):
    """
    Return the board that results from making move (i, j) on the board.
    """
    # Check if action is a valid action
    if action not in actions(board):
        raise InvalidAction("You have took an invalid action.")

    # Check who is is playing now
    current_player = player(board)

    # Create a deep copy of the board
    new_board = copy.deepcopy(board)

    row_index, col_index = action
    new_board[row_index][col_index] = current_player

    return new_board


def winner(board):
    """
    Return the winner of the game, if there is one.
    """
    BOARD_SIZE = len(board)

    # Check horizontal
    for each_row in board:
        if each_row.count(X) == BOARD_SIZE:
            return X
        if each_row.count(O) == BOARD_SIZE:
            return O

    # Check vertical
    for col_index in range(BOARD_SIZE):
        column = [row[col_index] for row in board]
        if column.count(X) == BOARD_SIZE:
            return X
        if column.count(O) == BOARD_SIZE:
            return O

    # Check diagonal
    # from top-left to bottom-right
    diagonal_1 = [board[i][i] for i in range(BOARD_SIZE)]
    # from bottom-left to top-right
    diagonal_2 = [board[BOARD_SIZE-1-i][i] for i in range(BOARD_SIZE)]

    diagonal_2 = [board[BOARD_SIZE-1-i][i] for i in range(BOARD_SIZE)]
    if diagonal_1.count(X) == BOARD_SIZE \
        or diagonal_2.count(X) == BOARD_SIZE:
        return X
    if diagonal_1.count(O) == BOARD_SIZE \
        or diagonal_2.count(O) == BOARD_SIZE:
        return O

    return None


def terminal(board):
    """
    Return TRUE if game is over, False otherwise.
    """
    # The game is over when X or O is the winner
    if winner(board) in (X, O):
        return True

    # or when the board is full but no winner.
    if not any(map(lambda x: EMPTY in x, board)):
        return True

    return False


def utility(board):
    """
    Return
    1 if X has won the game,
    -1 if O has won,
    0 otherwise.
    """
    WIN = 1
    LOSE = -1
    DRAW = 0

    if winner(board) == X:
        return WIN
    elif winner(board) == O:
        return LOSE

    return DRAW


def minimax(board):
    """
    Return the optimal action for the current player on the board.

    X is the maximizing player.
    O is the minimizing player.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        # Now, the player is X.
        candidate_outcome = -INFINITY
        for action in actions(board):
            possible_board = result(board, action)
            # O is trying to minimize the X's action
            opponents_utility = min_value(possible_board)
            # Store action and utility info from the maximum value
            # that O has given to X
            if opponents_utility > candidate_outcome:
                candidate_outcome = opponents_utility
                candidate_action = action

    elif current_player == O:
        # Now is O's turn.
        candidate_outcome = INFINITY
        for action in actions(board):
            possible_board = result(board, action)
            # O is tring to maximize the action of X
            opponents_utility = max_value(possible_board)
            # Store action and utility info from the minimum value
            # that X has given to O
            if opponents_utility < candidate_outcome:
                # Store this result
                candidate_outcome = opponents_utility
                candidate_action = action

    return candidate_action


def max_value(board):
    """
    The maximizing player picks action a in set of actions that
    produces the highest value of min_value(result(state, action)).
    """
    val = -INFINITY
    if terminal(board):
        return utility(board)

    for action in actions(board):
        # Get the resulting board for a given action
        resulting_board = result(board, action)
        # Check the best option for the next player
        val = max(val, min_value(resulting_board))

    return val


def min_value(board):
    """
    The minimizing player picks action a in set of actions that
    produces the lowest value of max_value(result(state, action)).
    """
    val = INFINITY
    if terminal(board):
        return utility(board)

    for action in actions(board):
        # Get the resulting board for a given action
        resulting_board = result(board, action)
        # Check the best option for the next player
        val = min(val, max_value(resulting_board))

    return val


