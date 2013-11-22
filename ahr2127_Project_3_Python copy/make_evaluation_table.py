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