Adam Reis
ahr2127
Artificial Intelligence Fall 2013
Assignment 2 -- Sokoban Solver

- Python Version: 2.7
- Development Environment: Text editing in Sublime Text 2 and running scripts in
						   the command line.

- How to run:

The following input will run both BFS and A* (with my first heuristic) on 
test_1.lvl and test_2.lvl and print answers for each, without stats.
----------------------------
python sokoban_runner.py
Please type in the map files you'd like to test, separated by spaces: test_1.lvl test_2.lvl
Please type in the algorithms you would like to use on these maps, separeted by spaces (BFS, DFS, UCS, GBFS, A*): BFS A*
Would you like to display stats on each of these algorithms (y/n)? n
Would you like to use heuristic 1 (sum of Manhattan distances from each box to the goal closest to it) or heuristic 2 (Manhattan distance from player to closest box) for your informed searches? (1/2) 1
----------------------------

* Note -- I assumed that I should implement graph search versions of all of these
algorithms (rather than tree search versions) to avoid infinite looping and
unneccessarily long runtimes.

** EXTRA COOLNESS:
If you want to test that my algorithm's output to a given puzzle is correct,
you can run sokoban_checker.pyw  with the string of the solution as a 
command line argument, and it will launch a GUI where you can choose a level on 
which to perform the moves (.lvl files only).  It will show you an animation of 
the puzzle being solved at 10 moves per second (you can change that by editing 
line 262 of sokoban_checker.pyw).  Sample input could be something like:

python sokoban_checker.pyw 'd, r, r, r, u, u, l, d, l, d, l, u, u, u, l, u, r, r, l, d, d, d, r, r, r, d, l, l, d, l, u, u, u, u, r, u, l, d, d, d, r, r, r, u, u, u, l'

If you then chose test_1.lvl from the GUI file chooser, you'll see it solved.

Cool, right?
I got most of the code from https://github.com/nightmarebadger/Sokoban-Tkinter,
but I made some significant modifications.

*You might need to install XQuartz or some similar X11 tool to launch the GUI





-Sample input/output for every algorithm on each of 3 maps:
------------------------------
python sokoban_runner.py
Please type in the map files you'd like to test, separated by spaces: test_1.lvl test_2.lvl test_3.lvl
Please type in the algorithms you would like to use on these maps, separeted by spaces (BFS, DFS, UCS, GBFS, A*): BFS DFS UCS GBFS A*
Would you like to display stats on each of these algorithms (y/n)? y
Would you like to use heuristic 1 (sum of Manhattan distances from each box to the goal closest to it) or heuristic 2 (Manhattan distance from player to closest box) for your informed searches? (1/2) 1

-----------------------------
test_1.lvl:

BFS:
Found a winning solution:
d, r, r, r, u, u, l, d, l, d, l, u, u, u, l, u, r, r, l, d, d, d, r, r, r, d, l, l, d, l, u, u, u, u, r, u, l, d, d, d, r, r, r, u, u, u, l
Number of nodes generated: 165200
Number of nodes containing states that were generated previously: 65156
Number of nodes on the fringe: 285
Number of nodes on explored list when termination occurs: 6830
Actual runtime of the algorithm: 15.27487 seconds

DFS:
Found a winning solution:
d, d, r, u, r, r, u, u, l, d, u, r, d, d, l, u, u, r, u, u, l, l, d, l, d, d, d, r, d, l, u, u, r, d, d, l, u, u, u, u, u, u, r, d, r, r, d, d, d, d, l, l, d, l, u, d, r, u, r, r, u, u, u, u, l, l, d, l, d, d, u, u, u, u, r, d, r, r, d, d, d, l, d, l, d, l, u, u, u, d, r, d, d, l, u, u, u, u, d, d, d, d, r, u, r, r, u, u, u, u, l, l, u, l, d, d, u, u, r, d, r, r, d, d, l, d, u, r, d, d, l, u, l, l, d, r, d, l, u, u, u, d, d, d, r, u, u, r, u, r, d, d, l, u, l, l, u, u, d, d, d, d, r, u, d, l, u, u, u, u, r, u, u, l, l, d, r, d, d, d, d, d, r, u, r, u, l, d, d, l, u, u, d, d, r, u, u, r, d, r, u, u, u, u, l, l, d, l, d, d, u, u, r, u, u, l, l, d, r, r, d, l, d, d, r, d, d, l, u, u, u, u, r, u, l, d, d, d, d, d, r, u, u, r, d, r, u, u, u, u, l
Number of nodes generated: 33196
Number of nodes containing states that were generated previously: 13900
Number of nodes on the fringe: 142
Number of nodes on explored list when termination occurs: 6453
Actual runtime of the algorithm: 2.991768 seconds

UCS:
Found a winning solution:
d, r, r, r, u, u, l, d, l, d, l, u, u, u, l, u, r, r, l, d, d, d, r, r, r, d, l, l, d, l, u, u, u, u, r, u, l, d, d, d, r, r, u, r, u, u, l
Total cost (2 for moving blocks, 1 otherwise): 62
Number of nodes generated: 172804
Number of nodes containing states that were generated previously: 68362
Number of nodes on the fringe: 85
Number of nodes on explored list when termination occurs: 6849
Actual runtime of the algorithm: 16.567964 seconds

GBFS:
Found a winning solution:
d, r, r, r, u, u, l, d, r, d, l, l, d, l, u, u, u, u, d, d, d, r, r, u, l, d, l, u, u, d, r, r, u, r, u, u, l, l, u, l, l, d, r, r, l, d, d, d, r, d, d, l, u, u, u, u, l, u, u, r, r, d, l, d, d, d, r, r, r, u, u, u, l
Number of nodes generated: 6823
Number of nodes containing states that were generated previously: 9681
Number of nodes on the fringe: 615
Number of nodes on explored list when termination occurs: 73
Actual runtime of the algorithm: 2.876406 seconds

A*:
Found a winning solution:
d, r, r, r, u, u, l, d, l, d, l, u, u, u, l, u, r, r, l, d, d, d, r, r, r, d, l, l, d, l, u, u, u, u, r, u, l, d, d, d, r, r, r, u, u, u, l
Number of nodes generated: 25872
Number of nodes containing states that were generated previously: 18978
Number of nodes on the fringe: 426
Number of nodes on explored list when termination occurs: 6468
Actual runtime of the algorithm: 3.772261 seconds

-----------------------------
test_2.lvl:

BFS:
Found a winning solution:
r, u, u, l, l, l, u, l, d, r, r, r, r, d, d, l, u, r, u, l, l, l, d, d, l, l, l, u, u, r, r, d, r, d, l, u, u, u, r, d, d
Number of nodes generated: 26552
Number of nodes containing states that were generated previously: 8942
Number of nodes on the fringe: 466
Number of nodes on explored list when termination occurs: 1929
Actual runtime of the algorithm: 2.161508 seconds

DFS:
Found a winning solution:
r, u, u, l, l, l, d, d, l, l, l, u, u, r, r, u, r, d, r, r, r, d, d, l, u, d, r, u, u, l, l, l, u, l, d, l, l, d, d, r, r, r, u, d, l, l, l, u, u, r, r, d, r, d, l, u, u, u, r, d, d
Number of nodes generated: 5988
Number of nodes containing states that were generated previously: 2123
Number of nodes on the fringe: 21
Number of nodes on explored list when termination occurs: 1269
Actual runtime of the algorithm: 0.487129 seconds

UCS:
Found a winning solution:
r, u, u, l, l, l, u, l, d, r, r, r, r, d, d, l, u, r, u, l, l, l, d, d, l, l, l, u, u, r, r, d, r, d, l, u, u, u, r, d, d
Total cost (2 for moving blocks, 1 otherwise): 54
Number of nodes generated: 22800
Number of nodes containing states that were generated previously: 7754
Number of nodes on the fringe: 270
Number of nodes on explored list when termination occurs: 1928
Actual runtime of the algorithm: 1.938821 seconds

GBFS:
Found a winning solution:
r, u, u, l, l, l, u, l, d, r, r, r, r, d, d, l, u, r, u, l, l, l, d, d, l, l, l, u, u, r, r, d, r, d, l, u, u, u, r, d, d
Number of nodes generated: 1647
Number of nodes containing states that were generated previously: 2070
Number of nodes on the fringe: 137
Number of nodes on explored list when termination occurs: 41
Actual runtime of the algorithm: 0.609833 seconds

A*:
Found a winning solution:
r, u, u, l, l, l, u, l, d, r, r, r, r, d, d, l, u, r, u, l, l, l, d, d, l, l, l, u, u, r, r, d, r, d, l, u, u, u, r, d, d
Number of nodes generated: 5668
Number of nodes containing states that were generated previously: 4037
Number of nodes on the fringe: 214
Number of nodes on explored list when termination occurs: 1417
Actual runtime of the algorithm: 0.734866 seconds

-----------------------------
test_3.lvl:

BFS:
Found a winning solution:
l, u, u, u, l, u, r, d, d, d, d, l, d, l, u, u, u, u, l, u, r
Number of nodes generated: 125196
Number of nodes containing states that were generated previously: 51782
Number of nodes on the fringe: 4544
Number of nodes on explored list when termination occurs: 8559
Actual runtime of the algorithm: 11.505786 seconds

DFS:
Found a winning solution:
d, r, u, u, u, u, u, l, l, d, l, u, l, d, d, d, d, d, r, u, u, r, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, r, u, u, u, u, l, l, d, d, d, l, l, d, d, r, u, d, r, u, u, u, u, u, r, r, d, d, d, l, d, d, r, u, u, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, u, r, u, u, u, l, l, d, d, d, l, r, d, d, r, u, u, r, u, u, u, l, l, d, l, u, l, d, d, d, u, u, u, r, d, r, d, d, d, d, l, u, d, r, u, u, u, u, u, l, d, l, d, d, r, d, d, r, u, u, d, d, r, u, u, r, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, l, l, u, r, d, r, u, d, r, u, u, u, u, u, l, l, d, d, d, d, d, l, l, u, d, r, u, u, r, d, d, r, u, r, u, l, d, d, r, u, u, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, l, u, d, l, u, l, u, d, d, r, u, u, r, d, d, r, u, r, u, l, d, d, r, u, u, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, u, r, u, u, u, l, l, d, d, d, l, l, d, d, r, u, d, r, u, u, u, u, u, l, d, l, d, u, u, r, d, r, d, d, d, d, l, u, l, u, u, d, d, d, r, u, r, d, r, u, u, r, u, u, u, l, l, d, d, d, l, d, d, r, u, u, u, u, u, l, l, l, d, r, d, d, u, u, u, r, r, d, d, d, d, d, l, l, u, u, d, d, r, u, u, r, d, d, r, u, u, r, u, u, u, l, l, d, l, u, l, l, d, r, r, u, r, d, u, r, r, d, d, d, d, d, l, u, u, l, d, d, l, u, u, l, u, d, d, d, r, u, u, r, d, d, r, u, u, r, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, u, r, u, u, u, l, l, d, d, d, l, l, d, r, d, r, u, d, r, u, u, r, u, u, u, l, l, d, l, u, l, l, d, r, d, d, d, d, r, u, u, r, d, d, r, u, r, u, u, u, u, l, l, d, l, u, r, d, d, d, d, d, l, u, u, l, u, u, d, d, d, d, r, u, u, r, d, d, r, u, r, u, l, d, d, r, u, u, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, u, r, u, u, u, l, l, d, d, d, l, l, d, d, r, u, d, r, u, u, u, u, u, l, d, l, d, d, r, d, d, r, u, u, d, d, r, u, u, r, u, u, u, l, l, d, l, l, l, u, r, d, d, d, d, d, r, u, u, r, d, d, r, u, u, r, u, u, u, l, l, d, d, d, u, u, u, r, r, d, d, d, d, d, l, u, l, d, r, u, u, r, u, u, u, l, l, d, d, d, l, l, d, d, r, u, d, r, u, u, u, u, l, l, d, d, r, d, d, r, u, r, d, r, u, u, u, u, u, l, l, d, l, l, u, r, d, r, d, d, u, u, l, u, r, d, d, d, r, d, d, r, u, u, u, u, u, l, r, d, d, d, d, d, l, u, l, d, r, u, u, l, u, u, l, u, r, d, d, d, d, d, l, u, d, r, u, u, u, u, u, l, d, l, d, d, r, d, d, r, u, u, d, d, r, u, u, r, u, u, u, l, r, d, d, d, d, d, l, u, u, l, u, d, d, d, r, u, u, r, u, u, u, l, l, l, d, l, d, d, d, d, r, u, u, r, u, u, d, d, d, d, l, u, u, l, u, u, r, u, r, d, d, d, d, d, l, u, u, l, u, u, l, u, r
Number of nodes generated: 44720
Number of nodes containing states that were generated previously: 19894
Number of nodes on the fringe: 536
Number of nodes on explored list when termination occurs: 8541
Actual runtime of the algorithm: 4.049321 seconds

UCS:
Found a winning solution:
l, u, u, u, l, u, r, d, d, d, d, l, d, l, u, u, u, u, l, u, r
Total cost (2 for moving blocks, 1 otherwise): 32
Number of nodes generated: 161932
Number of nodes containing states that were generated previously: 68207
Number of nodes on the fringe: 3011
Number of nodes on explored list when termination occurs: 9567
Actual runtime of the algorithm: 15.815458 seconds

GBFS:
Found a winning solution:
l, u, u, u, d, d, l, l, d, d, r, u, l, u, r, r, d, r, r, u, l, d, d, l, u, u, u, d, l, l, u, u, r, u, r, d, d, u, l, l, d, d, r, d, r, r, u, l, l, d, l, u, u, u, l, u, r
Number of nodes generated: 1303
Number of nodes containing states that were generated previously: 2081
Number of nodes on the fringe: 129
Number of nodes on explored list when termination occurs: 57
Actual runtime of the algorithm: 0.543567 seconds

A*:
Found a winning solution:
l, u, u, u, l, u, r, d, d, d, d, l, d, l, u, u, u, u, l, u, r
Number of nodes generated: 14264
Number of nodes containing states that were generated previously: 8551
Number of nodes on the fringe: 2147
Number of nodes on explored list when termination occurs: 3566
Actual runtime of the algorithm: 2.037993 seconds