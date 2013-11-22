__date__ ="Nov 6, 2013"


import sys
import time

from gomoku_state import GomokuState
from gomoku_game import GomokuGame
from gomoku_player import HumanPlayer, RandomPlayer, SmartPlayer



def usage():
    print """
    usage:

    python gomoku.py [mode] [board dimension] [winning chain length] [time limit]

    ex: python gomoku.py 1 10 5 60

    """

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        sys.exit(2)

    mode, board_dimension, winning_length, time_limit = \
                    [int(i) for index, i in enumerate(sys.argv) if index]

    gomo = GomokuGame(board_dimension, winning_length, time_limit, HumanPlayer, SmartPlayer)

