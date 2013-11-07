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

"""
    @ ... Player on floor
    # ... wall
    $ ... Box on floor
    . ... Empty Goal
    + ... Player on Goal
    * ... Box on goal
    
"""

def makeLevel(string):
    p = []
    with open(string, 'r') as f:
        for index, line in enumerate(f):
            if index != 0:
                p.append(list(line.rstrip()))
    return p

def findPlayer():
    player_x = None
    player_y = None
    for i in range(len(p)):
        for j in range(len(p[i])):
            if(p[i][j] in ['@','+']):
                if player_x or player_y:
                    return
                else:
                    player_x = j
                    player_y = i

    return(player_x,player_y)

def square(x, y, color):
    canvas.create_rectangle(x, y, x+wid, y+hei, fill=color)

def circle(x, y, color):
    canvas.create_oval(x, y, x+wid, y+hei, fill=color)

def draw():
    canvas.delete("all")
    for i in range(wid, width, wid):
        canvas.create_line(i, 0, i, height)

    for i in range(hei, height, hei):
        canvas.create_line(0, i, width, i)

    for i in range(len(p)):
        for j in range(len(p[i])):
            if(p[i][j] == '#'):
                square(j*wid, i*hei, "#252525")
            if(p[i][j] == '@'):
                circle(j*wid, i*hei, "red")
            if(p[i][j] == '$'):
                square(j*wid, i*hei, "blue")
            if(p[i][j] == '.'):
                square(j*wid, i*hei, "yellow")
            if(p[i][j] == '+'):
                square(j*wid, i*hei, "yellow")
                circle(j*wid, i*hei, "red")
            if(p[i][j] == '*'):
                square(j*wid, i*hei, "green")
            
            
def kill(event):
    root.destroy()

def move_off(x, y):
    # print 'move_off'
    #global ply_y, ply_x
    if(p[y][x] == '@'):
        p[y][x] = ' '
    if(p[y][x] == '+'):
        p[y][x] = '.'

def move_on(x, y):
    # print 'move_on'
    if(p[y][x] == '.'):
        p[y][x] = '+'
    if(p[y][x] == ' '):
        p[y][x] = '@'

def move_off_box(x, y):
    # print 'move_off_box'
    if(p[y][x] == '$'):
        p[y][x] = ' '
    if(p[y][x] == '*'):
        p[y][x] = '.'
        
def move_on_box(x, y):
    # print 'move_on_box'
    if(p[y][x] == ' '):
        p[y][x] = '$'
    if(p[y][x] == '.'):
        p[y][x] = '*'


def move(x, y):
#    print("Hej")
    global ply_y, ply_x
    if(p[ply_y + y][ply_x + x] in unblocked_space):
        move_off(ply_x, ply_y)
        ply_y += y
        ply_x += x
        move_on(ply_x, ply_y)

    elif(p[ply_y + y][ply_x + x] in blocked_space):
        if(p[ply_y + 2*y][ply_x + 2*x] in unblocked_space):
            move_off_box(ply_x + x, ply_y + y)
            move_on_box(ply_x + 2*x, ply_y + 2*y)
            move_off(ply_x, ply_y)
            ply_y += y
            ply_x += x
            move_on(ply_x, ply_y)
            

def has_won():
    for i in p:
        for j in i:
            if(j == '.'):
                return False
            elif(j == '+'):
                return False
    return True

def movement(n):
    global MOVES

    if(n == 'u'):
        MOVES+='u, '
        move(0, -1)

    elif(n == 'd'):
        MOVES+='d, '
        move(0, 1)

    elif(n == 'l'):
        MOVES+='l, '
        move(-1, 0)

    elif(n == 'r'):
        MOVES+='r, '
        move(1, 0)

    draw()
    if(has_won()):
        showinfo("You won!", "Congratulations, you won!")
        print 'You won! Moves: '+MOVES[:-2]
        root.destroy()
    
    

def restart():
    global p
    global ply_x, ply_y
    p = makeLevel(level)
    ply_x, ply_y = findPlayer()
    draw()
    
    
def keyHandler(event):
    foo = event.keysym[0].lower()
    movement(foo)
    if(event.char == 'r'):
        restart()

def mouse_click(event):
    print "clicked at {}, {}".format(event.x, event.y)


def usage():
    print """
    usage:

    python gomoku.py [mode] [board dimension] [winning chain length] [time limit]

    ex: python gomoku.py 1 12 5 60

    """
class GomokuState:
    def __init__(self, board=None):
        if board:
            self.board = board
        else:
            self.reset()

    def reset(self):
        self.board = []


class GomokuPlayer:
    def __init__(self, board_dimension, winning_length, time_limit):
# temp 
        self.player_turn = True

        self.board_dimension = board_dimension
        self.winning_length = winning_length
        self.time_limit = time_limit

        self.root = Tk()
        self.root.title("Gomoku!")
        self.root.focus_force()
        self.root.bind_all("<Button-1>", self._mouse_click)

        self.width=500

        self.canvas = Canvas(self.root, width=self.width, height=self.width)
        self.canvas.pack()

        self.state = []
        for i in range(board_dimension):
            self.state.append(['.']*board_dimension)
        # self.state[2][3]='X'

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
                if(self.state[i][j] == '.'):
                    pass
                elif(self.state[i][j] == 'X'):
                    self._circle((j+1)*self.line_width, (i+1)*self.line_width, "black")
                elif(self.state[i][j] == 'O'):
                    self._circle((j+1)*self.line_width, (i+1)*self.line_width, "white")

    def _circle(self, x, y, color):
        self.canvas.create_oval(x-self.line_width/2.3, y-self.line_width/2.3, x+self.line_width/2.3, y+self.line_width/2.3, fill=color)

    def _mouse_click(self, event):
        y_index = (event.y-self.line_width/2)/self.line_width
        x_index = (event.x-self.line_width/2)/self.line_width

        if not (x_index>=0 and y_index>=0 and x_index<self.board_dimension and y_index<self.board_dimension):
            return
        
        print "clicked at {}, {}".format(y_index, x_index)

        if self.player_turn:
            symbol = 'O'
        else:
            symbol = 'X'
        self.player_turn = not self.player_turn

        self.state[y_index][x_index]=symbol
        self._draw()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        sys.exit(2)

    mode, board_dimension, winning_length, time_limit = \
                    [int(i) for index, i in enumerate(sys.argv) if index]

    gomo = GomokuPlayer(board_dimension, winning_length, time_limit)

