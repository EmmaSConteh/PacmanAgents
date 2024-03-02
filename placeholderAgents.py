
# class HungryAgent(Agent):
#     def getAction(self, state):
#         foodLocation = {}
#         pacman = api.whereAmI(state)
#         legal = api.legalActions(state)
#         foods = api.food(state)

#         while len(foods) > 0:
#             for food in range(0,len(foods)):
#                 foodLocation[foods[food]] = util.manhattanDistance(pacman,foods[food])   

#             if Directions.STOP in legal:
#                 legal.remove(Directions.STOP)

#             if min(foodLocation)[0] - pacman[0] < 0:
#                 if Directions.WEST in legal:
#                     return api.makeMove(Directions.WEST, legal)
#                 else:
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(foodLocation)[0] - pacman[0] >= 1:
#                 if Directions.EAST in legal:
#                     return api.makeMove(Directions.EAST, legal)
#                 else:
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(foodLocation)[1] - pacman[1] < 0:
#                 if Directions.SOUTH in legal:
#                     return api.makeMove(Directions.SOUTH, legal)
#                 else:
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(foodLocation)[1] - pacman[1] >= 1:
#                 if Directions.NORTH in legal:
#                     return api.makeMove(Directions.NORTH, legal)
#                 else:
#                     return api.makeMove(random.choice(legal), legal)

# class CornerSeekingAgent(Agent):
#     def getAction(self, state):
#         cornerLocation = {}
#         pacman = api.whereAmI(state)
#         legal = api.legalActions(state)

#         while len(api.corners(state)) > 0:  

#             corners = api.corners(state)
#             for corner in range(0,len(api.corners(state))):
#                 cornerLocation[corners[corner]] = util.manhattanDistance(pacman,corners[corner])   

#             if Directions.STOP in legal:
#                 legal.remove(Directions.STOP)

#             if min(cornerLocation)[1] - pacman[1] >= 1:
#                 if Directions.NORTH in legal:
#                     return api.makeMove(Directions.NORTH, legal)
#                 else:
#                     return api.makeMove(random.choice(legal),legal)  
#             elif min(cornerLocation, key=cornerLocation.get)[1] - pacman[1] < 0:
#                 if Directions.SOUTH in legal:
#                     return api.makeMove(Directions.SOUTH, legal)
#                 else:
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(cornerLocation)[0] - pacman[0] >= 1:
#                 if Directions.EAST in legal:
#                     return api.makeMove(Directions.EAST, legal)
#                 else:
#                     return api.makeMove(random.choice(legal),legal)    
#             elif cornerLocation[0] - pacman[0] < 0:
#                 if Directions.WEST in legal:
#                     return api.makeMove(Directions.WEST, legal)
#                 else:
#                     return api.makeMove(random.choice(legal),legal)

# class SurvivalAgent(Agent):

#     def getAction(self, state):
#         pacman = api.whereAmI(state)
#         legal = api.legalActions(state)
#         ghosts = api.ghosts(state)
#         ghostDistance = {}

#         for i in range(len(ghosts)):
#             print util.manhattanDistance(pacman,ghosts[i])

#         while len(ghosts) > 0:
#             for ghost in range(0,len(ghosts)):
#                 ghostDistance[ghosts[ghost]] = util.manhattanDistance(pacman,ghosts[ghost])   

#             if min(ghostDistance)[0] - pacman[0] < 0:
#                 if Directions.EAST in legal:
#                     return api.makeMove(Directions.EAST, legal)
#                 else:
#                     if Directions.WEST in legal:
#                         legal.remove(Directions.WEST)
#                     return api.makeMove(random.choice(legal), legal)
#             if min(ghostDistance)[0] - pacman[0] >= 1:
#                 if Directions.WEST in legal:
#                     return api.makeMove(Directions.WEST, legal)
#                 else:
#                     if Directions.EAST in legal:
#                         legal.remove(Directions.EAST)
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(ghostDistance)[1] - pacman[1] < 0:
#                 if Directions.NORTH in legal:
#                     return api.makeMove(Directions.NORTH, legal)
#                 else:
#                     if Directions.SOUTH in legal:
#                         legal.remove(Directions.SOUTH)
#                     return api.makeMove(random.choice(legal), legal)
#             elif min(ghostDistance)[1] - pacman[1] >= 1:
#                 if Directions.SOUTH in legal:
#                     return api.makeMove(Directions.SOUTH, legal)
#                 else:
#                     if Directions.NORTH in legal:
#                         legal.remove(Directions.NORTH)
#                     return api.makeMove(random.choice(legal), legal)

# class MapBuildingAgent(Agent):
#     def __init__(self):
#         self.map = {}

#     def getAction(self, state):
#         legal = api.legalActions(state)
#         if Directions.STOP in legal:
#             legal.remove(Directions.STOP)
#         pacman = api.whereAmI(state)

#         food_locations = api.food(state)
#         ghost_positions = api.ghosts(state)
#         capsule_locations = api.capsules(state)
#         wall_locations = api.walls(state)

#         self.markVisited(pacman)

#         for food_location in food_locations:
#             self.markFood(food_location)

#         for ghost_position in ghost_positions:
#             self.markGhost(ghost_position)

#         for capsule_location in capsule_locations:
#             self.markCapsule(capsule_location)

#         for wall_location in wall_locations:
#             self.markWall(wall_location)

#         food_distances = []
#         for x in range(len(food_locations)):
#             food_distances.append(util.manhattanDistance(pacman,food_locations[x]))

#         min_food_distance = min(food_distances)
#         nearest_food = food_locations[food_distances.index(min_food_distance)]

#         moveX = Directions.STOP
#         moveY = Directions.STOP
#         if  pacman[0] - nearest_food[0] >= 0:
#             moveX = Directions.WEST
#         else:
#             moveX = Directions.EAST

#         if pacman[1] - nearest_food[1] >= 0:
#             moveY = Directions.SOUTH
#         else:
#             moveY = Directions.NORTH

#         if abs(pacman[0] - nearest_food[0]) >= abs(pacman[1] - nearest_food[1]) and moveX in legal:
#             return api.makeMove(moveX, legal)
#         elif abs(pacman[1] - nearest_food[1]) >= 0 and moveY in legal:
#             return api.makeMove(moveY, legal)
#         elif abs(pacman[0] - nearest_food[0]) >= 0 and moveX in legal:
#             return api.makeMove(moveX, legal)
#         else:
#             return api.makeMove(random.choice(legal), legal)
        
#     def markVisited(self, position):
#         if position not in self.map:
#             self.map[position] = {"visited": True, "food": False, "ghost": False, "capsule": False, "wall": False}

#     def markFood(self, position):
#         if position in self.map:
#             self.map[position]["food"] = True

#     def markGhost(self, position):
#         if position in self.map:
#             self.map[position]["ghost"] = True

#     def markCapsule(self, position):
#         if position in self.map:
#             self.map[position]["capsule"] = True

#     def markWall(self, position):
#         if position in self.map:
#             self.map[position]["wall"] = True

#     def isValidPosition(self, position):
#         return position not in self.map

#     def getSuccessor(self, position, move):
#         x, y = position
#         if move == Directions.NORTH:
#             return (x, y + 1)
#         elif move == Directions.SOUTH:
#             return (x, y - 1)
#         elif move == Directions.EAST:
#             return (x + 1, y)
#         elif move == Directions.WEST:
#             return (x - 1, y)
#         return position
