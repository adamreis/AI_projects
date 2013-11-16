# Originally written by nightmarebadger (https://github.com/nightmarebadger/Sokoban-Tkinter)
# Modified & translated by Adam Reis

__date__ ="Nov 6, 2013"


try:
    from tkinter import *
except ImportError:
    from Tkinter import *
try:
    from tkinter.filedialog import askopenfilename
except ImportError:
    from tkFileDialog import askopenfilename
try:
    from tkinter.messagebox import *
except ImportError:
    from tkMessageBox import *

import sys
import time
import copy
import random
from pdb import set_trace as debug

"""
    . ... Empty Goal
    X ... Black 
    O ... White
    
"""

def usage():
    print """
    usage:

    python gomoku.py [mode] [board dimension] [winning chain length] [time limit]

    ex: python gomoku.py 1 12 5 60

    """
class GomokuState:
    def __init__(self, prev_state=None, new_move=None, board_dimension=None, win_length=None):
        self.is_win_state = False
        if prev_state:
            self.board_dimension = prev_state.board_dimension
            self.win_length = prev_state.win_length
            self.board = copy.deepcopy(prev_state.board)
            self.move(new_move)
            if prev_state.is_win_state:
                self.is_win_state = True

        else:
            self.board_dimension = board_dimension
            self.win_length = win_length
            self.reset()

    def move(self, new_move):
        # new move = ('X', (1,3))
        if not new_move:
            return -1

        row = new_move[1][0]
        column = new_move[1][1]
        symbol = new_move[0]

        self.board[row][column]=symbol

    # check up and down
        count = 1
        # up
        for r in range(row-1,-1,-1):
            if count>self.win_length:
                break
            if self.board[r][column]==symbol:
                count+=1
                continue
            else:
                break
        # down
        for r in range(row+1, self.board_dimension, 1):
            if count>self.win_length:
                break
            if self.board[r][column]==symbol:
                count+=1
                continue
            else:
                break

        if count==self.win_length:
            print "WINNNNNNN"
            self.is_win_state = True

    # check left and right
        count = 1
        # left
        for c in range(column-1,-1,-1):
            if count>self.win_length:
                break
            if self.board[row][c]==symbol:
                count+=1
                continue
            else:
                break

        # right
        for c in range(column+1, self.board_dimension, 1):
            if count>self.win_length:
                break
            if self.board[row][c]==symbol:
                count+=1
                continue
            else:
                break


        if count==self.win_length:
            print "WINNNNNNN"
            self.is_win_state = True



    # check NE and SW
        count = 1
        # NE
        r = row-1
        c = column+1
        # import pdb; pdb.set_trace()
        while r>=0 and c<self.board_dimension:
            if count>self.win_length:
                break
            if self.board[r][c]==symbol:
                count+=1
                r-=1
                c+=1
                continue
            else:
                break
        # SW
        r = row+1
        c = column-1
        while r<len(self.board) and c>=0:
            if count>self.win_length:
                break
            if self.board[r][c]==symbol:
                count+=1
                r+=1
                c-=1
                continue
            else:
                break

        if count==self.win_length:
            print "WINNNNNNN"
            self.is_win_state = True

    # check NW and SE
        count = 1
        # NW
        r = row-1
        c = column-1
        while r>=0 and c>=0:
            if count>self.win_length:
                break
            if self.board[r][c]==symbol:
                count+=1
                r-=1
                c-=1
                continue
            else:
                break
        # SE
        r = row+1
        c = column+1
        while r<self.board_dimension and c<self.board_dimension:
            if count>self.win_length:
                break
            if self.board[r][c]==symbol:
                count+=1
                r+=1
                c+=1
                continue
            else:
                break

        if count==self.win_length:
            print "WINNNNNNN"
            self.is_win_state = True



    def reset(self):
        self.board = []
        for _ in range(self.board_dimension):
            self.board.append(['.']*self.board_dimension)


class GomokuGame:
    def __init__(self, board_dimension, winning_length, time_limit, player_1, player_2):
# temp 
        self.p1 = player_1(self)
        self.p2 = player_2(self)

        self.p1_turn = True

        self.board_dimension = board_dimension
        self.winning_length = winning_length
        self.time_limit = time_limit

        self.root = Tk()
        self.root.title("Gomoku!")
        self.root.focus_force()
        if self.p1.is_human:
            self.root.bind_all("<Button-1>", self.p1._mouse_click)

        self.width=500

        self.canvas = Canvas(self.root, width=self.width, height=self.width)
        self.canvas.pack()

        self.state = GomokuState(board_dimension=board_dimension, win_length=winning_length)

        self._draw()

        self.root.mainloop()

    def _draw(self):
        self.line_width = self.width/(self.board_dimension+1)

        self.canvas.delete("all")
        for i in range(self.line_width, self.width-self.line_width, self.line_width):
            self.canvas.create_line(i, 0, i, self.width)

        for i in range(self.line_width, self.width-self.line_width, self.line_width):
            self.canvas.create_line(0, i, self.width, i)

        for i in range(self.board_dimension):
            for j in range(self.board_dimension):
                if(self.state.board[i][j] == '.'):
                    pass
                elif(self.state.board[i][j] == 'X'):
                    self._circle((j+1)*self.line_width, (i+1)*self.line_width, "black")
                elif(self.state.board[i][j] == 'O'):
                    self._circle((j+1)*self.line_width, (i+1)*self.line_width, "white")
        self.root.update()

    def _circle(self, x, y, color):
        self.canvas.create_oval(x-self.line_width/2.3, y-self.line_width/2.3, x+self.line_width/2.3, y+self.line_width/2.3, fill=color)

    def _draw_winner(self):
        if self.p1_turn:
            text = 'Player 1 wins!'
        else:
            text = 'Player 2 wins!'
        # self.canvas.create_text(self.width/2, self.width/2, text=text)
        self.root.title(text)
        self.root.focus_force()


    def move(self, player, coordinates):
        if (player == self.p1 and not self.p1_turn) or (player==self.p2 and self.p1_turn):
            print 'not your turn!'
            return

        if self.state.is_win_state:
            print 'game over!'
            return

        if self.p1_turn:
            symbol = 'X'
        else:
            symbol = 'O'

        self.state = GomokuState(self.state, (symbol, coordinates))
        self._draw()

        # debug()
        if self.state.is_win_state:
            self._draw_winner()
            return

        self.p1_turn = not self.p1_turn
        if player == self.p1:
            self.p2.choose_move()
        elif player == self.p2:
            self.p1.choose_move()
        

class GomokuPlayer:
    def __init__(self, game):
        self.game = game

class HumanPlayer:
    def __init__(self, game):
        self.game = game
        self.is_human=True

    def _mouse_click(self, event):
        x_index = (event.y-self.game.line_width/2)/self.game.line_width
        y_index = (event.x-self.game.line_width/2)/self.game.line_width

        if not (y_index>=0 and x_index>=0 and y_index<self.game.board_dimension and x_index<self.game.board_dimension):
            return
        
        print "clicked at {}, {}".format(x_index, y_index)

        self.game.move(self, (x_index, y_index))

    def choose_move(self):
        pass

class RandomPlayer:
    def __init__(self, game):
        self.game = game
        self.is_human=False

    def choose_move(self):
        rand_x = random.randrange(self.game.board_dimension)
        rand_y = random.randrange(self.game.board_dimension)

        while self.game.state.board[rand_x][rand_y] != '.':
            rand_x = random.randrange(self.game.board_dimension)
            rand_y = random.randrange(self.game.board_dimension)

        self.game.move(self, (rand_x, rand_y))



if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        sys.exit(2)

    mode, board_dimension, winning_length, time_limit = \
                    [int(i) for index, i in enumerate(sys.argv) if index]

    gomo = GomokuGame(board_dimension, winning_length, time_limit, HumanPlayer, RandomPlayer)

