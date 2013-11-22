# Adam Reis
# ahr2127

import random
from pdb import set_trace as debug
from time import time, sleep
from random import randrange

from gomoku_state import GomokuState

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


