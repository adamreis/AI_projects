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

from gomoku_state import GomokuState
from make_evaluation_table import make_eval_table
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
            print "Draw!"
            self.winner = "No one"
            self._draw_winner()
            return

        self.p1_turn = not self.p1_turn
        if player == self.p1:
            self.p2.choose_move()
        elif player == self.p2:
            self.p1.choose_move()