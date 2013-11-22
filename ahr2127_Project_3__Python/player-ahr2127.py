#Adam Reis
#ahr2127
#jvoris' AI class

import sys
import time

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

from pdb import set_trace as debug

class GomokuGame:
    def __init__(self, board_dimension, winning_length, time_limit, player_1, player_2):
# temp 
        self.p1 = player_1(self, time_limit, 'X')
        self.p2 = player_2(self, time_limit, 'O')

        self.p1_turn = True
        self.winner = None

        self.board_dimension = board_dimension
        self.winning_length = winning_length
        self.time_limit = time_limit

        self.root = Tk()
        self.root.title("Gomoku!")
        self.root.focus_force()
        if self.p1.is_human:
            self.root.bind_all("<Escape>", self.p1.forfeit)
            self.root.bind_all("<Button-1>", self.p1.mouse_click)

        self.width=500

        self.canvas = Canvas(self.root, width=self.width, height=self.width)
        self.canvas.pack()

        self.x_eval, self.o_eval , x_instant, o_instant = make_eval_table(winning_length)
        self.state = GomokuState(board_dimension=board_dimension, win_length=winning_length, x_score_dict=self.x_eval, o_score_dict=self.o_eval, x_instant=x_instant, o_instant=o_instant)

        self._draw()

        self.p1.choose_move()
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
        self.root.title('{} wins!'.format(self.winner))
        self.root.focus_force()


    def move(self, player, coordinates):
        if (player == self.p1 and not self.p1_turn) or (player==self.p2 and self.p1_turn):
            print 'not your turn!'
            return

        if self.winner:
            print '{} wins!'.format(self.winner)
            return

        if coordinates == (-1,-1):
            if self.p1_turn:
                self.winner = 'Player 2'
            else:
                self.winner = 'Player 1'
            self._draw_winner()
            return

        if self.p1_turn:
            playa = "Player 1"
            symbol = 'X'
        else:
            playa = "Player 2"
            symbol = 'O'

        self.state = GomokuState(self.state, (symbol, coordinates))
        self.state.evaluate_score()

        self._draw()
        print '{}: {}.  Board score = {}'.format(playa, coordinates, self.state.score)


        if self.state.is_win_state:
            if self.p1_turn:
                self.winner = 'Player 1'
            else:
                self.winner = 'Player 2'
            print '{} wins!'.format(self.winner)     
            self._draw_winner()
            return

        if self.state.moves_on_board>=self.board_dimension**2:
            self.winner = "Draw"
            self._draw_winner()
            return

        self.p1_turn = not self.p1_turn
        if player == self.p1:
            self.p2.choose_move()
        elif player == self.p2:
            self.p1.choose_move()


#################################
import sys
from collections import defaultdict
import itertools
from math import floor, ceil

# l = [''.join(i) for i in list(itertools.product(['O','X','.'], repeat=8))]

def make_eval_table(win_length):
    if win_length<3:
        print 'are you serious?  that win length doesn\'t even make sense.'
        sys.exit(2)

    # orders of magnitude for various classes: normal: -1 to 1.  Win in 1 move: -100 to 100
    low_ord = 0.001
    norm_ord = 1
    one_ord = 1000
    win_ord = 1000000

    all_runs = [''.join(i) for i in list(itertools.product(['O','X','.'], repeat=(win_length+1)))]

    c = 'X'
    o = 'O'
    p = '.'

    x_table, x_instant_wins = tableify(all_runs, c, o, p, low_ord, norm_ord, one_ord, win_ord, win_length)

    c = 'O'
    o = 'X'
    o_table, o_instant_wins= tableify(all_runs, c, o, p, low_ord, norm_ord, one_ord, win_ord, win_length)

    return (x_table, o_table, x_instant_wins, o_instant_wins)
  

def tableify(all_runs, c, o, p, low_ord, norm_ord, one_ord, win_ord, win_length):
# TODO: _XX_XX | XX_XX_ | XX_XX | XX_XXO 
# Zero for XXX_XX or XX_XXX
# For even, would be XXX_XXX,

# XXX_X
    table = defaultdict(float)
    instant_wins = defaultdict(bool)
    for run in all_runs:

        for i in range(win_length):
            sent = ''.join([c*i, p, c*(win_length-i-1)])
            if sent in run:
                table[run]+=one_ord
                instant_wins[run]=True


        # basic number of stones
        for char in run:
            if char==c:
                table[run]+=low_ord

        # # win state _XXXXX or XXXXX_
        # if (c*win_length in run) and (c*(win_length+1) not in run):
        #     table[run]+=win_ord 

        # inevitable win state _XXXX_
        if run == ''.join([p, c*(win_length-1),p]):
            table[run]+=win_ord
            instant_wins[run]=True

        # one step away XXXX_

        # # one step away XXX_X
        # if ''.join([c*(win_length-2),p,c]) in run or ''.join([c,p,c*(win_length-2)]) in run:
        #     table[run]+=one_ord

        # # one side blocked _XXXXO or OXXXX_ 
        if (run in [''.join([p, c*(win_length-1), o]), ''.join([o, c*(win_length-1), p])]):
            table[run]+=one_ord
            instant_wins[run]=True

        # three in a row, unobstructed __XXX_ or _XXX__ || also XX_XX
        if run in [''.join([p, p, c*(win_length-2), p]), ''.join([p, c*(win_length-2), p, p])]:
            table[run]+=one_ord
            instant_wins[run]=True

        # half on each side, separated XX_XX
        if win_length%2: # odd
            if ''.join([c*((win_length-1)/2), p, c*((win_length-1)/2)]) in run:
                table[run]+=one_ord

        # X_XXO

        # _XXX_
        if ''.join([p,c*(win_length-2),p]) in run:
            table[run]+=(6*norm_ord)

        # OXXX_ or _XXXO
        if (''.join([o,c*(win_length-2),p]) in run) or (''.join([p,c*(win_length-2),o]) in run):
            table[run]+=(3*norm_ord)

        if win_length>3: 

            # half on each side, separated XX_X (only makes sense for length 4+) XX_X, X_XX, XXX_XX...
            if not win_length%2: # even
                l = int(floor((win_length-1)/2))
                u = int(ceil((win_length-1)/2))
                if (''.join([c*l,p,c*u]) in run) or (''.join([c*u,p,c*l]) in run):
                    table[run]+=one_ord


            # _X_XX_ or _XX_X_
            for i in range(1,win_length-2):
                if run == ''.join([p, c*i, p, c*(win_length-2-i), p]):
                    table[run]+=win_ord
                    instant_wins[run]=True


            # __XX__
            if run == ''.join([p,p,c*(win_length-3),p,p]):
                table[run]+=(4*norm_ord)

            # O_XX__ __XX_O
            if run in [''.join([o,p,c*(win_length-3),p,p]), ''.join([p,p,c*(win_length-3),p,o])]:
                table[run]+=(3*norm_ord)

            # OXX_ _XXO
            if ((''.join([o,c*(win_length-3),p]) in run) or (''.join([p,c*(win_length-3),o]) in run)) and run.count(o)<2:
                table[run]+=(2*norm_ord)


        if run[0]==o and run[-1]==o:
            table[run]=0

    return table, instant_wins


####################################
import copy
from pdb import set_trace as debug

class GomokuState:
    def __init__(self, prev_state=None, new_move=None, board_dimension=None, win_length=None, x_score_dict=None, o_score_dict=None, x_instant=None, o_instant=None):
        self.is_win_state = False
        if prev_state:
            self.prev = prev_state
            self.x_instant=prev_state.x_instant
            self.o_instant=prev_state.o_instant
            self.win_length = prev_state.win_length
            self.board = copy.deepcopy(prev_state.board)
            self.moves_on_board = prev_state.moves_on_board+1
            self.new_move = new_move
            self.x_dict = prev_state.x_dict
            self.o_dict = prev_state.o_dict
            self.score = None
            self.board_dimension = prev_state.board_dimension

            self.is_win_state = prev_state.is_win_state
            self.move(new_move)
            if self.is_win_state:
                self.score = 100000000000
            if (self.moves_on_board>=self.board_dimension**2) and not self.is_win_state:
                self.score = 0
                self.is_stalemate = True
            else:
                self.is_stalemate = False
            # if prev_state.is_win_state:
            #     self.is_win_state = True

        else:
            self.board_dimension = board_dimension
            self.win_length = win_length
            self.moves_on_board = 0
            self.x_dict = x_score_dict
            self.o_dict = o_score_dict
            self.x_instant = x_instant
            self.o_instant = o_instant
            self.reset()

    def evaluate_score(self):

        if self.score != None:
            return self.score
        else:
            self.score = 0

        if self.new_move[0]=='X':
            eval_dict = self.x_dict
            other_dict = self.o_dict
            inst_dict = self.o_instant
        elif self.new_move[0]=='O':
            eval_dict = self.o_dict
            other_dict = self.x_dict
            inst_dict = self.x_instant


        # check all horizontal strings
        for column in range(len(self.board)-self.win_length):
            for row in range(len(self.board)):
                s = ''
                for i in range(self.win_length+1):
                    s+=self.board[row][column+i]
                self.score+=0.1*eval_dict[s]
                self.score-=other_dict[s]
                if inst_dict[s]:
                    self.score += -10000000000
                    return

        # check all vertical strings
        for row in range(len(self.board)-self.win_length):
            for column in range(len(self.board)):
                s = ''
                for i in range(self.win_length+1):
                    s+=self.board[row+i][column]
                self.score+=0.1*eval_dict[s]
                self.score-=other_dict[s]
                if inst_dict[s]:
                    self.score += -10000000000
                    return

        # check all diagonal strings len(8-5)
        for column in range(self.board_dimension-self.win_length):
            for up_row in range(self.board_dimension-self.win_length):
                low_row = up_row+5

                south_east = ''
                north_east = ''
                for i in range(self.win_length+1):
                    south_east+=self.board[up_row+i][column+i]
                    try:
                        north_east+=self.board[low_row-i][column+i]
                    except:
                        debug
                # if 'XXXX' in north_east:
                    # debug()
                self.score+=0.1*eval_dict[south_east]
                self.score-=other_dict[south_east]
                self.score+=0.1*eval_dict[north_east]
                self.score-=other_dict[north_east]
                if inst_dict[south_east] or inst_dict[north_east]:
                    self.score += -10000000000
                    return

        # check four remaining
        # top right corner
        r = 0
        c = self.board_dimension-self.win_length
        s='.'
        for i in range(self.win_length):
            s+=self.board[r+i][c+i]
        if not self.new_move[0] in s:
            self.score+=0.1*eval_dict[s]
            self.score-=other_dict[s]
            if inst_dict[s]:
                self.score += -10000000000
                return

        # top left corner
        r = self.win_length-1
        c = 0
        s='.'
        for i in range(self.win_length):
            s+=self.board[r-i][c+i]
        if not self.new_move[0] in s:
            self.score+=0.1*eval_dict[s]
            self.score-=other_dict[s]
            if inst_dict[s]:
                self.score += -10000000000
                return

        # bottom left corner
        r = self.board_dimension-self.win_length
        c = 0
        s='.'
        for i in range(self.win_length):
            s+=self.board[r+i][c+i]
        if not self.new_move[0] in s:
            self.score+=0.1*eval_dict[s]
            self.score-=other_dict[s]
            if inst_dict[s]:
                self.score += -10000000000
                return

        # bottom right corner
        r = self.board_dimension-1
        c = self.board_dimension-self.win_length
        s='.'
        for i in range(self.win_length):
            s+=self.board[r-i][c+i]
        if not self.new_move[0] in s:
            self.score+=0.1*eval_dict[s]
            self.score-=other_dict[s]
            if inst_dict[s]:
                self.score += -10000000000
                return


    def move(self, new_move):
        # new move = ('X', (1,3))

        symbol = new_move[0]
        row = new_move[1][0]
        column = new_move[1][1]

        self.board[row][column]=symbol
        self.check_win_state(row, column, symbol)

    def next_states(self):
        # one_away = set()
        two_away = set()

        for r in range(self.board_dimension):
            for c in range(self.board_dimension):
                if self.board[r][c]!='.':
                    for i in range(-1,2):
                        for j in range(-1,2):
                            r1 = r+i
                            c1 = c+j
                            if r1<0 or r1>(self.board_dimension-1):
                                continue
                            if c1<0 or c1>(self.board_dimension-1):
                                continue
                            if self.board[r1][c1]!='.':
                                continue
                            two_away.add((r1,c1))

        return two_away




    def check_win_state(self, row, column, symbol):
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
            self.is_win_state = True

    def __str__(self):
        # st = ''
        # for r in range(len(self.board)):
        #     for c in range(len(self.board)):
        #         st+=self.board[r][c]
        #     st+='\n'
        # return st
        return str(self.board)

    def reset(self):
        self.board = []
        for _ in range(self.board_dimension):
            self.board.append(['.']*self.board_dimension)


##############################

import random
from time import time, sleep
from random import randrange

class HumanPlayer:
    def __init__(self, game, time_limit, symbol):
        self.game = game
        self.is_human=True

    def mouse_click(self, event):
        x_index = (event.y-self.game.line_width/2)/self.game.line_width
        y_index = (event.x-self.game.line_width/2)/self.game.line_width

        if not (y_index>=0 and x_index>=0 and y_index<self.game.board_dimension and x_index<self.game.board_dimension):
            return
        
        # print "clicked at {}, {}".format(x_index, y_index)

        self.game.move(self, (x_index, y_index))

    def forfeit(self, event):
        self.game.move(self, (-1,-1))

    def choose_move(self):
        pass

class RandomPlayer:
    def __init__(self, game, time_limit, symbol):
        self.game = game
        self.is_human=False
        self.time_limit = time_limit
        self.symbol=symbol

    def choose_move(self):
        if self.game.state.moves_on_board < self.game.board_dimension**2:
            x = random.randrange(self.game.board_dimension)
            y = random.randrange(self.game.board_dimension)

            while self.game.state.board[x][y] != '.':
                x = random.randrange(self.game.board_dimension)
                y = random.randrange(self.game.board_dimension)
        else:
            x = -1
            y = -1

        self.game.move(self, (x,y))

class SmartPlayer:
    def __init__(self, game, time_limit, symbol):
        self.game = game
        self.is_human=False
        self.time_limit = time_limit
        self.symbol=symbol
        self.timer = 0
        self.max_count = self.min_count = 0

        self.node_count = 0

    def print_debug(self, note=''):
        # print note+' max: {}, min: {}'.format(self.max_count, self.min_count)
        print note

    def choose_move(self):
        # empty board
        sleep(0.4)
        if self.game.state.moves_on_board==0:
            rand1 = randrange(self.game.board_dimension)
            rand2 = randrange(self.game.board_dimension)
            self.game.move(self, (rand1, rand2))
            return

        self.timer = time()
        next_states = list(self.game.state.next_states())
        num_states = len(next_states)
        # scores = [0]*len(next_states)
        
        max_score = (-float('inf'), None) # (score, coords)
        all_max = []

        stop_interval = .03*(self.time_limit/num_states)
        
        # debug()
        for index, state in enumerate(next_states):
            new_state = GomokuState(self.game.state, (self.symbol, state))
            self.node_count+=1
            # if time()<(self.timer+self.time_limit):
            #     s = 'not beyond stop time in choose #{}/{}'.format(index+1, len(next_states))
            #     print s
            #     self.print_debug(s)

            s = 'branch #{}/{}'.format(index+1, len(next_states))
            # self.print_debug(s)

            # scores[index]=self.max_value(new_state, stop_time)
            # if new_state.is_win_state:
            #     self.game.move(self, state)
            #     return

            my_max = self.min_value(new_state, time()+stop_interval, -float('inf'), float('inf'), 1)
            # print 'score: {}'.format(my_max)
            all_max.append(my_max)
            if my_max>max_score[0]:
                max_score = (my_max, state)

        all_hugely_negative = True
        for thing in all_max:
            if thing>-10000000000:
                all_hugely_negative = False
        if all_hugely_negative:
            pass
            # debug()
            # self.game.move(self, (-1,-1))
            # return
        self.game.move(self,max_score[1])

    def min_value(self, state, stop_time, alpha, beta, level):
        self.min_count+=1
        if time()>(self.timer+self.time_limit):
            self.print_debug('forced return')
            state.evaluate_score()
            return state.score


        if state.is_win_state or time()>stop_time or state.is_stalemate:
            state.evaluate_score()
            # self.print_debug('current time: {}, stop_time: {}, actual limit: {}'.format(time()%1000, stop_time%1000, (self.timer+self.time_limit)%1000))
            # if level<6:
                # self.print_debug('return on level {}'.format(level))
            return state.score   

        v = float('inf')
        if self.symbol == 'X':
            sym = 'O'
        else:
            sym = 'X'

        next_states = state.next_states()
# might be an issue
        new_interval = (stop_time - time())/len(next_states)

        for coords in next_states:
            new_state = GomokuState(state, (sym, coords))
            self.node_count+=1

            if time()<stop_time:
                s = 'not beyond stop time min_value'
                # self.print_debug(s)

            v = min(v, self.max_value(new_state, time()+new_interval, alpha, beta, level+1))
            if v<=alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, state, stop_time, alpha, beta, level):
        self.max_count+=1
        if time()>(self.timer+self.time_limit):
            self.print_debug('forced return')
            state.evaluate_score()
            return state.score
        if state.is_win_state or time()>stop_time or state.is_stalemate:
            state.evaluate_score()
            # self.print_debug('current time: {}, stop_time: {}, actual limit: {}'.format(time()%1000, stop_time%1000, (self.timer+self.time_limit)%1000))
            # if level<6:
                # self.print_debug('return on level {}'.format(level))
            return state.score

        v = -float('inf')

        next_states = state.next_states()
# is this right?
        new_interval = (stop_time - time())/len(next_states)

        for coords in next_states:
            new_state = GomokuState(state, (self.symbol, coords))
            self.node_count+=1

            if time()<stop_time:
                s = 'not beyond stop time max_value'
                # self.print_debug(s)


            v = max(v, self.min_value(new_state, time()+new_interval, alpha, beta, level+1))
            if v>=beta:
                return v
            alpha = max(alpha, v)
        return v

















def usage():
    print """
    usage:

    python player-ahr2127.py [mode] [board dimension] [winning chain length] [time limit]

    ex: python player-ahr2127.py 1 8 5 15

    """

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        sys.exit(2)

    mode, board_dimension, winning_length, time_limit = \
                    [int(i) for index, i in enumerate(sys.argv) if index]

    if mode==1:
        gomo = GomokuGame(board_dimension, winning_length, time_limit, HumanPlayer, SmartPlayer)
    elif mode==2:
        gomo = GomokuGame(board_dimension, winning_length, time_limit, HumanPlayer, RandomPlayer)
    elif mode==3:
        gomo = GomokuGame(board_dimension, winning_length, time_limit, SmartPlayer, SmartPlayer)

