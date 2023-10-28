# sampleAgents.py
# parsons/07-oct-2017

# Version 1.1

# Some simple agents to work with the PacMan AI projects from:

# http://ai.berkeley.edu/

# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.

# As required by the licensing agreement for the PacMan AI we have:

# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

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

        # # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # # Where is the food?
        print "Food locations: "
        print api.food(state)

        # # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # # getAction has to return a move. Here we pass "STOP" to the
        # # API to ask Pacman to stay where they are.
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

        if ghosts:
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
                for k in legals:
                    if legals[k] >= bestLegalDistance:
                        bestLegal = k
                        bestLegalDistance = legals[k]
                return api.makeMove(bestLegal, legal)
          
        else:
            return api.makeMove(random.choice(legal), legal)

class CombinedAgent(Agent):
    def __init__(self):
        self.BL = False
        self.TR = False
        self.TL = False
        self.BR = False

    def visited(self, position):
        if position not in self.map:
            self.map[position] = {position: True}
        print(self.map)

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        food = api.food(state)
        corners = api.corners(state)
        moveX = Directions.STOP
        moveY = Directions.STOP
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0
        bestLegalDistance = 0
        bestLegal = Directions.STOP

        if ghosts:
            print "survivor mode"
            #worried survivor state
            ghosts_distances = []
            for i in range(len(ghosts)):
                ghosts_distances.append(util.manhattanDistance(pacman,ghosts[i]))

            nearest_ghost = ghosts[ghosts_distances.index(min(ghosts_distances))]
        
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
          
        else:
            #happy forager state
            print "forager mode"
            food_distances = []
            if food:
                for x in range(len(food)):
                    food_distances.append(util.manhattanDistance(pacman,food[x]))

                min_food_distance = min(food_distances)
                nearest_food = food[food_distances.index(min_food_distance)]

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
            else:
                # seek food by journeying to the any unvisited corner
                print "corner seeking mode"

                for i in range(len(corners)):
                    cornerX = corners[i][0]
                    cornerY = corners[i][1]
            
                    if cornerX < minX:
                        minX = cornerX
                    if cornerY < minY:
                        minY = cornerY
                    if cornerX > maxX:
                        maxX = cornerX
                    if cornerY > maxY:
                        maxY = cornerY

                if pacman[0] == minX + 1:
                    if pacman[1] == minY + 1:
                        self.BL = True
                
                if pacman[0] == maxX - 1:
                    if pacman[1] == maxY - 1:
                        self.TR = True

                if pacman[0] == minX + 1:
                    if pacman[1] == maxY - 1:
                        self.TL = True
                
                if pacman[0] == maxX - 1:
                    if pacman[1] == minY + 1:
                        self.BR = True

                if self.BL == False:
                    if pacman[0] > minX + 1:
                        if Directions.WEST in legal:
                            return api.makeMove(Directions.WEST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.SOUTH in legal:
                            return api.makeMove(Directions.SOUTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif self.TR == False:
                    if pacman[0] < maxX - 1:
                        if Directions.EAST in legal:
                            return api.makeMove(Directions.EAST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.NORTH in legal:
                            return api.makeMove(Directions.NORTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif self.TL == False:
                    if pacman[0] > minX + 1:
                        if Directions.WEST in legal:
                            return api.makeMove(Directions.WEST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.NORTH in legal:
                            return api.makeMove(Directions.NORTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                elif self.BR == False:
                    if pacman[0] < maxX - 1:
                        if Directions.EAST in legal:
                            return api.makeMove(Directions.EAST, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                    else:
                        if Directions.SOUTH in legal:
                            return api.makeMove(Directions.SOUTH, legal)
                        else:
                            pick = random.choice(legal)
                            return api.makeMove(pick, legal)
                else:
                    return api.makeMove(random.choice(legal), legal)


                
                
             
# # try to get to bl
#                 if self.BL == False:
#                     if Directions.WEST in legal:
#                         return api.makeMove(Directions.WEST, legal)
#                     elif Directions.SOUTH in legal:
#                         return api.makeMove(Directions.SOUTH, legal)
#                     else:
#                         return api.makeMove(random.choice(legal), legal)
                                
       
#Corner Seeking Agent 
#
#forces Pacman to move to the four corners of the environment
class CornerSeekingAgent(Agent):

        # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False

    def final(self, state):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
        
    def getAction(self, state):

        # Get extreme x and y values for the grid
        corners = api.corners(state)
        print corners
        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0
        
        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]
            
            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print pacman
        #
        # If we haven't got to the lower left corner, try to do that
        #
        
        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print "Got to BL!"
                self.BL = True

        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner
        
        # Check we aren't there:
        if pacman[0] == minX + 1:
           if pacman[1] == maxY - 1:
                print "Got to TL!"
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner
        
        # Check we aren't there:
        if pacman[0] == maxX - 1:
           if pacman[1] == maxY - 1:
                print "Got to TR!"
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.
        
        if pacman[0] == maxX - 1:
           if pacman[1] == minY + 1:
                print "Got to BR!"
                self.BR = True
                return api.makeMove(Directions.STOP, legal)
           else:
               print "Nearly there"
               return api.makeMove(Directions.SOUTH, legal)

        print "Not doing anything!"
        return api.makeMove(Directions.STOP, legal)
            

class MapBuildingAgent(Agent):
    def __init__(self):
        self.map = {}

    def getAction(self, state):
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)

        self.visited(pacman)

        return api.makeMove(random.choice(legal), legal)

    def visited(self, position):
        if position not in self.map:
            self.map[position] = {position: True}
        print(self.map)


