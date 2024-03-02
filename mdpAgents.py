# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import itertools as it

ghost_penalty = -50
food_reward = 10
capsule_reward = 20
blank_penalty = -1
scared_ghost_reward = 100

# # Creates a grid to be used in MapAgent
# #
# # The Grid class and its elements were provided by module leads in Week 5. 
class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class MDPAgent(Agent):
	# Constructor: this gets run when we first invoke pacman.py
	def __init__(self):
		print "Starting up MDPAgent!"
		name = "Pacman"

		# Initialising lists for food, capsules, walls and pacmans visited locations
		self.food_locs = []
		self.capsule_locs = []
		self.wall_locs = []
		self.pac_locs = []

	#Gets run after an MDPAgent object is created and once there is
    # game state to access.
	def registerInitialState(self, state):
		print "Running registerInitialState for MDPAgent!"
		print "I'm at:"
		print api.whereAmI(state)

		# makeMap(), addWallsToMap() getLayoutWidth() and getLayoutHeight() are taken from mapAgents.py provided in Week 5
		self.makeMap(state)
		self.addWallsToMap(state)
		corners = api.corners(state)
		self.width = self.getLayoutWidth(corners)
		self.height = self.getLayoutHeight(corners)

	# This is what gets run in between multiple games
	def final(self, state):
		print "Looks like the game just ended!"

		# Resetting lists 
		self.food_locs = []
		self.capsule_locs = []
		self.wall_locs = []
		self.pac_locs = []

	""" makeMap(), addWallsToMap() getLayoutWidth() and getLayoutHeight() are taken from mapAgents.py provided in Week 5"""
	def makeMap(self, state):
		corners = api.corners(state)
		height = self.getLayoutHeight(corners)
		width = self.getLayoutWidth(corners)
		self.map = Grid(width, height)

	def getLayoutHeight(self, corners):
		height = -1
		for i in range(len(corners)):
			if corners[i][1] > height:
				height = corners[i][1]
		return height + 1

	def getLayoutWidth(self, corners):
		width = -1
		for i in range(len(corners)):
			if corners[i][0] > width:
				width = corners[i][0]
		return width + 1

	def addWallsToMap(self, state):
		walls = api.walls(state)
		for i in range(len(walls)):
			self.map.setValue(walls[i][0], walls[i][1], 0)

	def assignRewards(self, state):
		""" Assigns rewards to each square in the map"""

		rewards = {}
		food = api.food(state)
		walls = api.walls(state)
		capsules = api.capsules(state)
		pacman = api.whereAmI(state)
		ghosts = api.ghosts(state)
		ghost_states = api.ghostStates(state)

		# Convert ghosts to integers for easy comparison
		int_ghosts = []
		for i in range(len(ghosts)):
			int_ghosts.append((int(ghosts[i][0]), int(ghosts[i][1])))

		# add new locations to lists, and update pacman's locations
		if pacman not in self.pac_locs:
			self.pac_locs.append(pacman)
		self.food_locs += [i for i in food if i not in self.food_locs]
		self.capsule_locs += [i for i in capsules if i not in self.capsule_locs]
		self.wall_locs += [i for i in walls if i not in self.wall_locs]
		rewards.update({i: 0 for i in self.food_locs if i in self.pac_locs})
		rewards.update({i: 0 for i in self.capsule_locs if i in self.pac_locs})

		# rewards for food and capsules are positive, walls are negative
		rewards.update({f: food_reward for f in self.food_locs})
		rewards.update({w: blank_penalty for w in self.wall_locs})
		rewards.update({c: capsule_reward for c in self.capsule_locs})

		# rewards/penalty for ghosts depend on whether they are scared or not
		for ghost in ghost_states:
			if ghost[1] == 1:
				rewards.update({ghost[0]: scared_ghost_reward})
			else:
				rewards.update({ghost[0]: ghost_penalty})

		# for i in rewards.keys():
		# 	for j in range(len(int_ghosts)):
		# 		if i == int_ghosts[j]:
		# 			rewards[i] = ghost_penalty
		
		# anything I missed gets a reward of 0
		for i in range(self.width - 1):
			for j in range(self.height - 1):
				if (i, j) not in rewards.keys():
					rewards[(i, j)] = 0
		return rewards


	def getUtility(self, x, y, reward_map):
		""" Returns the best utility of a given location by looking at the utilities of its neighbours """
		pos = (x, y)
		# neighbouring locations
		north = (x, y + 1)
		south = (x, y - 1)
		east = (x + 1, y)
		west = (x - 1, y)

		# for each direction calculate it's utility. If there is a wall in that direction, calculate the utility of the current location	
		temp = north if reward_map[north] != -1 else pos
		nu = (0.8 * reward_map[temp])
		for direction in east, west:
			if reward_map[direction] != -1:
				nu += (0.1 * reward_map[direction])
			else:
				nu += (0.1 * reward_map[pos])

		temp = south if reward_map[south] != -1 else pos
		su = (0.8 * reward_map[temp])
		for direction in east, west:
			if reward_map[direction] != -1:
				su += (0.1 * reward_map[direction])
			else:
				su += (0.1 * reward_map[pos])

		temp = east if reward_map[east] != -1 else pos
		eu = (0.8 * reward_map[temp])
		for direction in north, south:
			if reward_map[direction] != -1:
				eu += (0.1 * reward_map[direction])
			else:
				eu += (0.1 * reward_map[pos])

		temp = west if reward_map[west] != -1 else pos
		wu = (0.8 * reward_map[temp])
		for direction in north, south:
			if reward_map[direction] != -1:
				wu += (0.1 * reward_map[direction])
			else:
				wu += (0.1 * reward_map[pos])
		
		utilities = {}
		utilities.update({"nu": nu, "su": su, "eu": eu, "wu": wu})
		best_utility =  max(utilities.values())

		return best_utility
		
	def valueIteration(self, state, gamma, reward_map, aura_radius, iter):
		""" Value Iteration algorithm using bellman update equation"""

		walls = api.walls(state)
		food = api.food(state)
		ghosts = api.ghosts(state)
		capsules = api.capsules(state)

		# create an aura around the ghosts so discourage pacman from going near them
		aura = self.Aura(aura_radius, ghosts)
		ghost_aura = [i for i in food if i not in aura]

		# run the bellman update equation iter times. iter is passed in as a parameter so it can be changed depending on the size of the map
		while iter > 0:
			for i in range(self.width - 1):
				for j in range(self.height - 1):
					if all((i, j) not in lst for lst in [walls, ghosts, capsules, ghost_aura]):
						reward_map[(i, j)] = gamma * self.getUtility(i, j, reward_map)
			iter -= 1
		return reward_map

	def Aura(self, radius, ghosts):
		"""Creates a 'aura' or radius around the ghost"""
		aura = []
		# for each ghost, create a list of all the locations within the radius
		for i in range(radius):
			for x in range(len(ghosts)):
				ghost_x, ghost_y = int(ghosts[x][0]), int(ghosts[x][1])
				neighbour = [(ghost_x + i, ghost_y), (ghost_x - i, ghost_y), (ghost_x, ghost_y + i), (ghost_x, ghost_y - i)]
				for n in neighbour:
					if n not in aura:
						aura.append(n)
		return aura
	
	def bestLegalMove(self, state, vals):
		""" Returns the best legal move for Pacman from his current position"""
		walls = set(api.walls(state))
		pacman = api.whereAmI(state)
		# determine the best move by looking at the utilities of the neighbouring locations
		x, y = pacman
		neighbours = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
		states = [i for i in neighbours if i not in walls]
		n_util = [vals[i] for i in states]
		best = states[n_util.index(max(n_util))]
		
		# convert that move into a direction
		direction = tuple(x - y for x, y in zip(pacman, best))
		if direction == (0, -1):
			return Directions.NORTH
		if direction == (-1, 0):
			return Directions.EAST
		if direction == (0, 1):
			return Directions.SOUTH
		if direction == (1, 0):
			return Directions.WEST
	
	def getAction(self, state):
		legal = api.legalActions(state)
		if Directions.STOP in legal:
			legal.remove(Directions.STOP)
		reward_map = self.assignRewards(state)
		
		# run value iteration with different parameters depending on the size of the map
		if (self.width -1) >= 8 and (self.height - 1) >= 8:
			iter = self.valueIteration(state, 0.8, reward_map, 3, 200)
		else:
			iter = self.valueIteration(state, 0.72, reward_map, 3, 100)


		pick = self.bestLegalMove(state, iter)
		return api.makeMove(pick, legal)