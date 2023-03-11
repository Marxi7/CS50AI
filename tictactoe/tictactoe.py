"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    xCount = 0
    oCount = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                xCount += 1
            elif board[row][col] == O:
                oCount += 1
    
    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Checking if the action is possible is possible
    if action not in actions(board):
        raise Exception('This action is not possible!')
    
    row, col = action
    current_board_copy = copy.deepcopy(board)

    # This action belongs to the current player
    current_board_copy[row][col] = player(board)

    return current_board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking every row of the board
    if all(row == board[0][0] for row in board[0]):
        return board[0][0]
    elif all(row == board[1][0] for row in board[1]):
        return board[1][0]
    elif all(row == board[2][0] for row in board[2]):
        return board[2][0]

    # Checking columns
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]

    # Checking diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[2][0]
    else:
        return None        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checking if there is a winner, if not, we check if all the positions are taken to make sure the game is over
    if winner(board) is not None or winner(board) is None and noEmptyPosition(board) is True:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Also check if the game just began. If True, the AI will choose a random position. 
    This add more randomness to the game and avoid unecessary calculation for the first move.
    """
    # Making sure the game isn't over yet
    if terminal(board):
        return None

    if player(board) == X:
        if isBeginningOfGame(board):
            return random.choice(tuple(actions(board)))   
              
        else:
            v = -math.inf
            for action in actions(board):
                highest_in_min = minValue(result(board, action), -1, 1)
                if highest_in_min > v:
                    v = highest_in_min
                    best_move = action
            return best_move

    elif player(board) == O:
        v = math.inf
        for action in actions(board):
            smallest_in_max = maxValue(result(board, action), -1, 1)
            if smallest_in_max < v:
                v = smallest_in_max
                best_move = action
        return best_move


def maxValue(board, alpha, beta):
    """
    Returns the action that produces the highest value of Min-Value
    """
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action), alpha, beta))
        if v >= beta:
            return v
        if v > alpha:
            alpha = v
    return v


def minValue(board, alpha, beta):
    """
    Returns the action that produces the lowest value of Max-Value
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action), alpha, beta))
        if v <= alpha:
            return v
        if v < beta:
            beta = v
    return v
    

def noEmptyPosition(board):
    """
    Check if every position is taken or not. 
    Return True if not a single position is empty & False Otherwise
    """
    if not any(EMPTY in row for row in board):
        return True
    else:
        return False


def isBeginningOfGame(board):
    """
    This returns True if the game is beginning
    If the number of possibilties is 9, that means that the board is empty and the game just began.
    """
    if len(actions(board)) == 9:
        return True
    else:
        return False