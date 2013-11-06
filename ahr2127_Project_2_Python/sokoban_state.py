__author__="Adam Reis <ahr2127@columbia.edu>"
__date__ ="$Oct 23, 2013"

import sys
from copy import deepcopy

"""
    @ ... Player on floor
    # ... wall
    $ ... Box on floor
    . ... Empty Goal
    + ... Player on Goal
    * ... Box on goal
    
"""

class SokoState(object):
	"""docstring for SokoState"""
	def __init__(self, astar=None, cost=None, heuristic=False, box_cost=1, map_file=None, map_array=None, player_x=None, player_y=None, prev_moves=None):
		self.p = []
		self.ply_x = []
		self.ply_y = []
		self.moves = ''
		self.cost = 0
		self.box_cost = box_cost
		self.heuristic_choice = heuristic
		self.h_cost = None
		self.astar = astar

		if map_file:
			self._make_level(map_file)
			self._find_player()
		elif map_array and player_x!=None and player_y!=None and cost!=None:
			self.p = map_array
			self.ply_x = player_x
			self.ply_y = player_y
			self.moves = prev_moves
			self.cost = cost
	   	else:
			print 'incorrect arguments for SokoState'
			sys.exit(1)

	def _make_level(self,map_file):
	    with open(map_file, 'r') as f:
	        for index, line in enumerate(f):
	            if index != 0:
	                self.p.append(list(line.rstrip()))

	def _find_player(self):
	    player_x = None
	    player_y = None
	    for i in range(len(self.p)):
	        for j in range(len(self.p[i])):
	            if(self.p[i][j] in ['@','+']):
	                if player_x or player_y:
	                    print 'more than one player on board?'
	                    sys.exit(1)
	                else:
	                    player_x = j
	                    player_y = i
	    self.ply_x = player_x
	    self.ply_y = player_y

	def _move_off(self, x, y):
	    if(self.p[y][x] == '@'):
	        self.p[y][x] = ' '
	    if(self.p[y][x] == '+'):
	        self.p[y][x] = '.'

	def _move_on(self, x, y):
	    if(self.p[y][x] == '.'):
	        self.p[y][x] = '+'
	    if(self.p[y][x] == ' '):
	        self.p[y][x] = '@'

	def _move_off_box(self, x, y):
	    if(self.p[y][x] == '$'):
	        self.p[y][x] = ' '
	    if(self.p[y][x] == '*'):
	        self.p[y][x] = '.'
	        
	def _move_on_box(self, x, y):
	    if(self.p[y][x] == ' '):
	        self.p[y][x] = '$'
	    if(self.p[y][x] == '.'):
	        self.p[y][x] = '*'

	def _move(self, x, y):

		unblocked_space = [' ', '.']
		blocked_space = ['$', '*']

		if(self.p[self.ply_y + y][self.ply_x + x] in unblocked_space):
			self.cost+=1
			self._move_off(self.ply_x, self.ply_y)
			self.ply_y += y
			self.ply_x += x
			self._move_on(self.ply_x, self.ply_y)

		elif(self.p[self.ply_y + y][self.ply_x + x] in blocked_space):
			if(self.p[self.ply_y + 2*y][self.ply_x + 2*x] in unblocked_space):
				self.cost+=self.box_cost
				self._move_off_box(self.ply_x + x, self.ply_y + y)
				self._move_on_box(self.ply_x + 2*x, self.ply_y + 2*y)
				self._move_off(self.ply_x, self.ply_y)
				self.ply_y += y
				self.ply_x += x
				self._move_on(self.ply_x, self.ply_y)

	def next_sokostate(self, n):
		new = SokoState(map_array=deepcopy(self.p), 
						player_x=deepcopy(self.ply_x), 
						player_y=deepcopy(self.ply_y), 
						prev_moves=deepcopy(self.moves),
						cost=deepcopy(self.cost),
						box_cost=deepcopy(self.box_cost),
						heuristic=self.heuristic_choice,
						astar=deepcopy(self.astar))
		if(n == 'u'):
			new.moves+='u, '
			new._move(0, -1)

		elif(n == 'd'):
			new.moves+='d, '
			new._move(0, 1)

		elif(n == 'l'):
			new.moves+='l, '
			new._move(-1, 0)

		elif(n == 'r'):
			new.moves+='r, '
			new._move(1, 0)

		return new


	def is_win_state(self):
	    for i in self.p:
	        for j in i:
	            if(j == '.'):
	                return False
	            elif(j == '+'):
	                return False
	    return True

	def box_distance_from_goals_heuristic(self):
		"""
		http://weetu.net/Timo-Virkkala-Solving-Sokoban-Masters-Thesis.pdf
		http://www.onlinespiele-sammlung.de/sokoban/sokobangames/corcoles/help.html
		"""

		boxes = []
		goals = []
		total = 0
		for i in range(len(self.p)):
			for j in range(len(self.p[i])):
				if(self.p[i][j] == '$'):
					boxes.append((i,j))
		
		for i in range(len(self.p)):
			for j in range(len(self.p[i])):
				if(self.p[i][j] == '.'):
					goals.append((i,j))

		for box in boxes:
			min_dist = float('inf')
			for goal in goals:
				dist = abs(box[0]-goal[0])+abs(box[1]-goal[1])
				min_dist = min(dist, min_dist)
			total+=min_dist
		self.h_cost = total

	def box_distance_from_player_heuristic(self):
		"""
		http://weetu.net/Timo-Virkkala-Solving-Sokoban-Masters-Thesis.pdf
		http://www.onlinespiele-sammlung.de/sokoban/sokobangames/corcoles/help.html
		Returns the shortest manhattan distance of any block to the player
		"""

		shortest = float('inf')
		for i in range(len(self.p)):
			for j in range(len(self.p[i])):
				if(self.p[i][j] == '$'):
					dist = abs(j-self.ply_x)+abs(i-self.ply_y)
					if dist<shortest:
						shortest = dist
		self.h_cost = shortest


	def __str__(self):
		string = ''
		for row in self.p:
			string+= '\n'+''.join(row)
		return string

	def __lt__(self, other):
		if self.astar:
			return (self.h_cost+self.cost)<(other.h_cost+other.cost)
		elif self.heuristic_choice:
			return self.h_cost<other.h_cost
		else:
			return self.cost<other.cost

	def __eq__(self,other):
		return self.__str__()==other.__str__()



