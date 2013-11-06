__author__="Adam Reis <ahr2127@columbia.edu>"
__date__ ="$Oct 23, 2013"

from sokoban_state import SokoState
from collections import defaultdict, deque
import Queue
import time
from heapq import heappush, heappop, heapify
import sys
import json

class DFS:

	def __init__(self, map_file):
		self.num_generated = 0
		self.num_previously_seen = 0
		self.num_on_fringe = 0
		self.num_explored_nodes = None
		self.runtime = 0


		state = SokoState(map_file=map_file)

		start = time.clock()
		try:
			winner = self._dfs_helper(state)
		except RuntimeError:
			print 'This algorithm exceeded the maximum recursion depth (expected).'
			winner = None

		self.runtime = (time.clock()-start)

		if winner:
			print 'Found a winning solution:'
			moves =  winner.moves[:-2]
			print moves
		else:
			print 'Did not find a winning solution.'


	def _dfs_helper(self, state):
		seen = defaultdict(lambda: None)

		q = []
		q.append(state)

		while len(q):
			# print len(q)
			
			cur_state = q.pop()
			seen[cur_state.__str__()] = True
			if cur_state.is_win_state():
				self.num_explored_nodes = len(seen)
				self.num_on_fringe = len(q)
				return cur_state
			for move in ['l','r','u','d']:
				if move == 'd':
					pass
				new_state = cur_state.next_sokostate(move)
				self.num_generated+=1
				if new_state.p != cur_state.p: # This should take care of wall situations
					if seen[new_state.__str__()]:
						self.num_previously_seen+=1
						continue 		# Uncomment this to prevent it from re-visiting nodes
					q.append(new_state)

		return None


	def print_statistics(self):
		print 'Number of nodes generated: {}'.format(self.num_generated)
		print 'Number of nodes containing states that were generated previously: {}'.format(self.num_previously_seen)
		print 'Number of nodes on the fringe: {}'.format(self.num_on_fringe)
		print 'Number of nodes on explored list when termination occurs: {}'.format(self.num_explored_nodes)
		print 'Actual runtime of the algorithm: {} seconds'.format(self.runtime)


class BFS:

	def __init__(self, map_file):
		self.num_generated = 0
		self.num_previously_seen = 0
		self.num_on_fringe = 0
		self.num_explored_nodes = None
		self.runtime = 0

		state = SokoState(map_file=map_file)

		start = time.clock()
		winner = self._bfs_helper(state)
		self.runtime = (time.clock()-start)

		if winner:
			print 'Found a winning solution:'
			moves =  winner.moves[:-2]
			print moves
		else:
			print 'Did not find a winning solution.'


	def _bfs_helper(self, state):
		seen = defaultdict(lambda: None)

		q = deque()
		q.append(state)

		while len(q):
			cur_state = q.popleft()
			seen[cur_state.__str__()] = True
			if cur_state.is_win_state():
				self.num_explored_nodes = len(seen)
				self.num_on_fringe = len(q)
				return cur_state
			for move in ['l','r','u','d']:
				new_state = cur_state.next_sokostate(move)
				self.num_generated+=1
				if new_state.p != cur_state.p: # This should take care of wall situations
					if seen[new_state.__str__()]:
						self.num_previously_seen+=1
						continue 		# Uncomment this to prevent it from re-visiting nodes
					q.append(new_state)

		return None


	def print_statistics(self):
		print 'Number of nodes generated: {}'.format(self.num_generated)
		print 'Number of nodes containing states that were generated previously: {}'.format(self.num_previously_seen)
		print 'Number of nodes on the fringe: {}'.format(self.num_on_fringe)
		print 'Number of nodes on explored list when termination occurs: {}'.format(self.num_explored_nodes)
		print 'Actual runtime of the algorithm: {} seconds'.format(self.runtime)

class UCS:

	def __init__(self, map_file):
		self.num_generated = 0
		self.num_previously_seen = 0
		self.num_on_fringe = 0
		self.num_explored_nodes = None
		self.runtime = 0


		state = SokoState(map_file=map_file,box_cost=2)

		start = time.clock()
		winner = self._ucs_helper(state)
		self.runtime = (time.clock()-start)

		if winner:
			print 'Found a winning solution:'
			moves =  winner.moves[:-2]
			print moves
			print 'Total cost (2 for moving blocks, 1 otherwise): {}'.format(winner.cost)
		else:
			print 'Did not find a winning solution.'


	def _ucs_helper(self, state):
		seen = defaultdict(lambda: None)

		q = Queue.PriorityQueue()
		q.put(state)

		while not q.empty():
			cur_state = q.get()
			seen[cur_state.__str__()] = True
			if cur_state.is_win_state():
				self.num_on_fringe = q.qsize()
				self.num_explored_nodes = len(seen)
				return cur_state
			for move in ['l','r','u','d']:
				self.num_generated+=1
				new_state = cur_state.next_sokostate(move)
				
				if new_state.p != cur_state.p: # This should take care of wall situations
					if seen[new_state.__str__()]:
						self.num_previously_seen+=1
						continue 		# Uncomment this to prevent it from re-visiting nodes
					q.put(new_state)

		return None


	def print_statistics(self):
		print 'Number of nodes generated: {}'.format(self.num_generated)
		print 'Number of nodes containing states that were generated previously: {}'.format(self.num_previously_seen)
		print 'Number of nodes on the fringe: {}'.format(self.num_on_fringe)
		print 'Number of nodes on explored list when termination occurs: {}'.format(self.num_explored_nodes)
		print 'Actual runtime of the algorithm: {} seconds'.format(self.runtime)



class GBFS:

	def __init__(self, map_file, heuristic_choice):
		self.num_generated = 0
		self.num_previously_seen = 0
		self.num_on_fringe = 0
		self.num_explored_nodes = None
		self.runtime = 0
		self.heuristic = heuristic_choice

		state = SokoState(map_file=map_file,heuristic=True)

		start = time.clock()
		try:
			winner = self._gbfs_helper(state)
		except RuntimeError:
			print 'This algorithm exceeded the maximum recursion depth.'
			winner = None

		self.runtime = (time.clock()-start)

		if winner:
			print 'Found a winning solution:'
			moves =  winner.moves[:-2]
			print moves
			self.num_explored_nodes = len(moves.split(', '))
		else:
			print 'Did not find a winning solution.'


	def _update(self,sokostate):
		if self.heuristic == 1:
			sokostate.box_distance_from_goals_heuristic()
		elif self.heuristic == 2:
			sokostate.box_distance_from_player_heuristic()


	def _gbfs_helper(self, state):
		seen = defaultdict(lambda: None)
		
		q = Queue.PriorityQueue()
		q.put(state)

		while not q.empty():
			cur_state = q.get()
			seen[cur_state.__str__()] = True
			if cur_state.is_win_state():
				self.num_explored_nodes = len(seen)
				self.num_on_fringe = q.qsize()
				return cur_state
			for move in ['l','r','u','d']:
				new_state = cur_state.next_sokostate(move)
				
				if new_state.p != cur_state.p: # This should take care of wall situations
					if seen[new_state.__str__()]:
						self.num_previously_seen+=1
						continue 		# Uncomment this to prevent it from re-visiting nodes
					self.num_generated+=1
					self._update(cur_state)
					self._update(new_state)

					if new_state<cur_state:
						new_state.h_cost = 0
						cur_state.h_cost = 1
						q.put(cur_state)
						q.put(new_state)
						break

					q.put(new_state)
		return None


	def print_statistics(self):
		print 'Number of nodes generated: {}'.format(self.num_generated)
		print 'Number of nodes containing states that were generated previously: {}'.format(self.num_previously_seen)
		print 'Number of nodes on the fringe: {}'.format(self.num_on_fringe)
		print 'Number of nodes on explored list when termination occurs: {}'.format(self.num_explored_nodes)
		print 'Actual runtime of the algorithm: {} seconds'.format(self.runtime)

class ASTAR:

	def __init__(self, map_file, heuristic_choice):
		self.num_generated = 0
		self.num_previously_seen = 0
		self.num_on_fringe = 0
		self.num_explored_nodes = None
		self.runtime = 0
		self.heuristic = heuristic_choice

		state = SokoState(map_file=map_file,heuristic=True,astar=True)

		self.start = time.clock()
		try:
			winner = self._astar_helper(state)
		except RuntimeError:
			print 'This algorithm exceeded the maximum recursion depth.'
			winner = None

		self.runtime = (time.clock()-self.start)

		if winner:
			print 'Found a winning solution:'
			moves =  winner.moves[:-2]
			print moves
		else:
			print 'Did not find a winning solution.'

	def _update(self,sokostate):
		if self.heuristic == 1:
			sokostate.box_distance_from_goals_heuristic()
		elif self.heuristic == 2:
			sokostate.box_distance_from_player_heuristic()


	def _astar_helper(self, state):
		seen = defaultdict(lambda: None)

		q = Queue.PriorityQueue()
		self._update(state)
		q.put(state)

		while not q.empty():
			state = q.get()
			if state.is_win_state():
				self.num_on_fringe = q.qsize()
				self.num_explored_nodes = len(seen)
				return state
			if seen[state.__str__()]:
				self.num_previously_seen += 1
			else:
				seen[state.__str__()]=True
				for move in ['l','r','u','d']:
					new_state = state.next_sokostate(move)
					self.num_generated+=1
					if new_state != state: #only valid moves
						self._update(new_state)
						q.put(new_state)

		return None


	def print_statistics(self):
		print 'Number of nodes generated: {}'.format(self.num_generated)
		print 'Number of nodes containing states that were generated previously: {}'.format(self.num_previously_seen)
		print 'Number of nodes on the fringe: {}'.format(self.num_on_fringe)
		print 'Number of nodes on explored list when termination occurs: {}'.format(self.num_explored_nodes)
		print 'Actual runtime of the algorithm: {} seconds'.format(self.runtime)

if __name__ == "__main__":
	dumb_methods = {	'dfs':DFS,
						'bfs':BFS,
						'ucs':UCS}
	smart_methods = {	'gbfs':GBFS,
						'a*':ASTAR}
	
	filenames = None
	while not filenames:
		filenames = raw_input('Please type in the map files you\'d like to test, separated by spaces: ').strip().split()
	
	algos = None
	while not algos:
		algos = raw_input('Please type in the algorithms you would like to use on '
						  'these maps, separeted by spaces (BFS, DFS, UCS, GBFS, A*): ').strip().split() 

	stats = None
	while not stats:
		stats = raw_input('Would you like to display stats on each of these algorithms (y/n)? ').strip()

	for item in ['gbfs','GBFS','a*','A*']:
		if item in algos:
			heuristic = raw_input(('Would you like to use heuristic 1 (sum of Manhattan distances '
									'from each box to the goal closest to it) or heuristic 2 (Manhattan'
									' distance from player to closest box) for your informed searches? (1/2) ')).strip()	
			break

	for filename in filenames:
		print '\n-----------------------------'
		print filename+':'
		for algo in algos:
			print '\n'+algo.upper()+':'
			if algo.lower() in dumb_methods:
				search = dumb_methods[algo.lower()](filename)
			elif algo.lower() in smart_methods:
				search = smart_methods[algo.lower()](filename,int(heuristic))
			else:
				print 'Can\'t understand your input! Please try again.'
				sys.exit(2)
			if stats == 'y':
				search.print_statistics()

