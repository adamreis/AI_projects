Adam Reis
Ahr2127
Artificial Intelligence Assignment 3 -  Gomoku Agent

How to run:

    python player-ahr2127.py [mode] [board dimension] [winning chain length] [time limit]

    where mode==1 is human vs intelligent opponent
          mode==2 is human vs random opponent
          mode==3 is intelligent player vs intelligent player

    ex: python player-ahr2127.py 1 8 5 15

    See the beautiful GUI!?  No command-line interface here (Voris said I could). You shouldn't have any problem running it on the CLIC machines -- I was able to do it over ssh.  If you have any issues with that, please email me: ahr2127@columbia.edu

My evaluation function:
    The way I structured my evaluation function is pretty sweet.  First, I create a list of every possible (win_length+1) character long permutation of the characters 'X', 'O', and '.'.  Then I loop through all those strings, checking to see whether they satisfy certain valuable attributes (you can see some of them in my comments).  If they do, then I save the string in a dictionary, where the value is the value of that string (higher values for strings that will inevitably lead to wins like .XXXX., lower values for strings like X..XOX).  To evaluate a particular board, I simply loop through every single (win_length+1) character long string on the board and add its corresponding value in the dictionary.  Note that the dictionary is very sparse, so most strings will have no value associated with them.  I also take this chance to see if the opponent will inevitably win given this state, in which case I make the score verrrrry low (-1000000000).

    This approach wouldn't have been too hard if the win length was always 5, but it was extremely difficult to generalize to any win length -- looking back, I wish I had taken a more general approach.

    One thing I hoped to have time to do, to make my code more efficient, was to only update the score for strings surrounding a newly placed stone.  This would cut my evaluation time approximately in half (assuming normal board sizes), but it was far too difficult to implement.  In general my evaluation function isn't perfect (I didn't have time to iron out all of the kinks), but it can beat me most of the time.

My challenges:
    Mode 1:
    My player can beat me almost every time.  I think it's mostly because the player does not think at all like a human (partially because of my very synthetic evaluation function), so I generally don't understand what it's trying to do until it lures me into a trap.  

    Mode 2:
    This isn't too interesting -- the random opponent isn't much of a challenge (although it's quick!)  The random opponent just keeps picking random points until it finds one that's unoccupied.  I'm not sure that this is the most efficient implementation, but it's plenty fast for these purposes.

    Mode 3:
    Mode 3 was particularly useful for debugging.  Because my agent picks a random move at first, this mode will rarely repeat a game, and it often exposed bugs in my evaluation function.  If I play on a small enough board, player 1 always wins.  On larger boards the players often tie, although if it runs into one of the edge cases of my evaluation function, it might end otherwise.  

