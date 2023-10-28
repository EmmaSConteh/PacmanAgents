# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)


# GoWestAgent
#
# Alawys tries to go west on the grid when it is possible

class GoWestAgent(Agent):
    
    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        else:
            pick = random.choice(legal)
            return api.makeMove(pick, legal)

# HungryAgent
#
# Uses information about the location of the food to try to move towards the nearest food

class HungryAgent(Agent):

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman = api.whereAmI(state)
        food = api.food(state)

        food_distances = []
        for x in range(len(food)):
            food_distances.append(util.manhattanDistance(pacman,food[x]))

        min_food_distance = min(food_distances)
        nearest_food = food[food_distances.index(min_food_distance)]

        moveX = Directions.STOP
        moveY = Directions.STOP
        if  pacman[0] - nearest_food[0] >= 0:
            moveX = Directions.WEST
        else:
            moveX = Directions.EAST

        if pacman[1] - nearest_food[1] >= 0:
            moveY = Directions.SOUTH
        else:
            moveY = Directions.NORTH

        if abs(pacman[0] - nearest_food[0]) >= abs(pacman[1] - nearest_food[1]) and moveX in legal:
            return api.makeMove(moveX, legal)
        elif abs(pacman[1] - nearest_food[1]) >= 0 and moveY in legal:
            return api.makeMove(moveY, legal)
        elif abs(pacman[0] - nearest_food[0]) >= 0 and moveX in legal:
            return api.makeMove(moveX, legal)
        else:
            return api.makeMove(random.choice(legal), legal)

# Survival Agent
#
# uses the location of Pacman and the ghosts to stay alive as long as possible.

class SurvivalAgent(Agent):

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        moveX = Directions.STOP
        moveY = Directions.STOP
        bestLegalDistance = 0
        bestLegal = Directions.STOP

        ghosts_distances = []
        for i in range(len(ghosts)):
            ghosts_distances.append(util.manhattanDistance(pacman,ghosts[i]))

        nearestGhost = ghosts[ghosts_distances.index(min(ghosts_distances))]
        
        if pacman[0] - nearestGhost[0] >= 0:
            moveX = Directions.EAST
        else:
            moveX = Directions.WEST
        if pacman[1] - nearestGhost[1] >= 0:
            moveY = Directions.NORTH
        else:
            moveY = Directions.SOUTH

        if abs(pacman[0] - nearestGhost[0]) >= abs(pacman[1] - nearestGhost[1]) and moveX in legal:
            return api.makeMove(moveX, legal)
        elif abs(pacman[1] - nearestGhost[1]) >= 0 and moveY in legal:
            return api.makeMove(moveY, legal)
        elif abs(pacman[0] - nearestGhost[0]) >= 0 and moveX in legal:
            return api.makeMove(moveX, legal)
        else:
            legals = {}
            for i in range(len(legal)):
                if legal[i] == Directions.NORTH:
                    legals[legal[i]] = (pacman[0], pacman[1] + 1)
                if legal[i] == Directions.EAST:
                    legals[legal[i]] = (pacman[0] + 1, pacman[1])
                if legal[i] == Directions.SOUTH:
                    legals[legal[i]] = (pacman[0], pacman[1] - 1)
                if legal[i] == Directions.WEST:
                    legals[legal[i]] = (pacman[0] - 1, pacman[1])
            for k in legals:
                legals[k] = util.manhattanDistance(legals[k], nearestGhost)
            print legals
            for k in legals:
                if legals[k] >= bestLegalDistance:
                    bestLegal = k
                    bestLegalDistance = legals[k]
            return api.makeMove(bestLegal, legal)

class CombinedAgent(Agent):

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        food = api.food(state)
        moveX = Directions.STOP
        moveY = Directions.STOP

        food_distances = [util.manhattanDistance(pacman, f) for f in food]
        ghost_distances = [util.manhattanDistance(pacman, g) for g in ghosts]

        if food_distances:
            min_food_distance = min(food_distances)
            nearest_food = food[food_distances.index(min_food_distance)]

            if pacman[0] - nearest_food[0] >= 0:
                moveX = Directions.WEST
            else:
                moveX = Directions.EAST

            if pacman[1] - nearest_food[1] >= 0:
                moveY = Directions.SOUTH
            else:
                moveY = Directions.NORTH

            if ghost_distances:
                min_ghost_distance = min(ghost_distances)
                nearest_ghost = ghosts[ghost_distances.index(min_ghost_distance)]

                if min_ghost_distance < min_food_distance:
                    moveX = Directions.STOP
                    moveY = Directions.STOP

                    if pacman[0] - nearest_ghost[0] >= 0:
                        moveX = Directions.EAST
                    else:
                        moveX = Directions.WEST

                    if pacman[1] - nearest_ghost[1] >= 0:
                        moveY = Directions.NORTH
                    else:
                        moveY = Directions.SOUTH

            if abs(pacman[0] - nearest_food[0]) >= abs(pacman[1] - nearest_food[1]) and moveX in legal:
                return api.makeMove(moveX, legal)
            elif abs(pacman[1] - nearest_food[1]) >= 0 and moveY in legal:
                return api.makeMove(moveY, legal)
            elif abs(pacman[0] - nearest_food[0]) >= 0 and moveX in legal:
                return api.makeMove(moveX, legal)
            else:
                return api.makeMove(random.choice(legal), legal)
        else:
            # If there is no food, avoid ghosts to stay alive
            moveX = Directions.STOP
            moveY = Directions.STOP

            if pacman[0] - nearest_ghost[0] >= 0:
                moveX = Directions.EAST
            else:
                moveX = Directions.WEST

            if pacman[1] - nearest_ghost[1] >= 0:
                moveY = Directions.NORTH
            else:
                moveY = Directions.SOUTH

            if abs(pacman[0] - nearest_ghost[0]) >= abs(pacman[1] - nearest_ghost[1]) and moveX in legal:
                return api.makeMove(moveX, legal)
            elif abs(pacman[1] - nearest_ghost[1]) >= 0 and moveY in legal:
                return api.makeMove(moveY, legal)
            elif abs(pacman[0] - nearest_ghost[0]) >= 0 and moveX in legal:
                return api.makeMove(moveX, legal)
            else:
                legals = {}
                for i in range(len(legal)):
                    if legal[i] == Directions.NORTH:
                        legals[legal[i]] = (pacman[0], pacman[1] + 1)
                    if legal[i] == Directions.EAST:
                        legals[legal[i]] = (pacman[0] + 1, pacman[1])
                    if legal[i] == Directions.SOUTH:
                        legals[legal[i]] = (pacman[0], pacman[1] - 1)
                    if legal[i] == Directions.WEST:
                        legals[legal[i]] = (pacman[0] - 1, pacman[1])
                for k in legals:
                    legals[k] = util.manhattanDistance(legals[k], nearest_ghost)
                for k in legals:
                    if legals[k] >= bestLegalDistance:
                        bestLegal = k
                        bestLegalDistance = legals[k]
                return api.makeMove(bestLegal, legal)

        