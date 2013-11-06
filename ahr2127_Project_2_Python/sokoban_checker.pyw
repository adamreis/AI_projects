# Originally written by nightmarebadger (https://github.com/nightmarebadger/Sokoban-Tkinter)
# Modified & translated by Adam Reis

__date__ ="$Oct 23, 2013"


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

def square(x, y, barva):
    canvas.create_rectangle(x, y, x+wid, y+hei, fill=barva)

def circle(x, y, barva):
    canvas.create_oval(x, y, x+wid, y+hei, fill=barva)

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


def askLevel():
    top = Tk()
    top.withdraw()
    level = askopenfilename(initialdir = ".", filetypes = [('Level files', '.lvl'), ('All files', '.*')], title = "Choose the level you want to play")
    top.destroy()

    try:
        return(makeLevel(level))
    except IOError:
        top = Tk()
        top.withdraw()
        if(askretrycancel("Error!", "There was an error trying to open your level. Do you want to try again?")):           
            try:
                return(askLevel())
            finally:
                top.destroy()
        else:
            top.destroy()
            return(False)
    
if __name__ == '__main__':
    p = askLevel()
    if(not p):
        pass
    else:
        w = 0
        for array in p:
            if len(array) > w:
                w = len(array)
        h = len(p)

        unblocked_space = [' ', '.']
        blocked_space = ['$', '*']

        max_width = 2000
        max_height = 2000

        wid = hei = 50

        if(wid*w > max_width or hei*h > max_height):
            wid = hei = min(max_width//w, max_height//h)
        width = wid * w
        height = hei * h


        try:
            ply_x, ply_y = findPlayer()
        except TypeError:
            print "Your map doesn't have exactly one player on it!"
            sys.exit()
        except IndexError:
            print "Your map doesn't seem to be formatted correctly."
            sys.exit()

        root = Tk()
        root.title("Simple Sokoban clone")
        root.focus_force()

        canvas = Canvas(root, width=width, height=height)
        canvas.pack()
        draw()

        root.bind_all("<Escape>", kill)
        root.bind_all("<Key>", keyHandler)

        global MOVES
        MOVES = ''

        if len(sys.argv) == 2:
            moves = sys.argv[1].split(', ')
            for char in moves:
                root.update()
                movement(char)
                time.sleep(.1)
                

        root.mainloop()
