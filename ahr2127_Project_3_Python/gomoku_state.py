import copy
from pdb import set_trace as debug

class GomokuState:
    def __init__(self, prev_state=None, new_move=None, board_dimension=None, win_length=None, x_score_dict=None, o_score_dict=None, x_instant=None, o_instant=None):
        self.is_win_state = False
        self.instant_lose = []
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
                    self.instant_lose.append(s)
                    self.score += -10000000000
                    # return

        # check all vertical strings
        for row in range(len(self.board)-self.win_length):
            for column in range(len(self.board)):
                s = ''
                for i in range(self.win_length+1):
                    s+=self.board[row+i][column]
                self.score+=0.1*eval_dict[s]
                self.score-=other_dict[s]
                if inst_dict[s]:
                    self.instant_lose.append(s)
                    self.score += -10000000000
                    # return

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
                        debug()
                # if 'XXXX' in north_east:
                    # debug()
                self.score+=0.1*eval_dict[south_east]
                self.score-=other_dict[south_east]
                self.score+=0.1*eval_dict[north_east]
                self.score-=other_dict[north_east]
                if inst_dict[south_east]:
                    self.instant_lose.append(south_east)
                    self.score += -10000000000
                    # return
                if inst_dict[north_east]:
                    self.instant_lose.append(north_east)
                    self.score += -10000000000

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
                self.instant_lose.append(s)
                self.score += -10000000000
                # return

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
                self.instant_lose.append(s)
                self.score += -10000000000
                # return

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
                self.instant_lose.append(s)
                self.score += -10000000000
                # return

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
                self.instant_lose.append(s)
                # self.score += -10000000000
                # return


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
