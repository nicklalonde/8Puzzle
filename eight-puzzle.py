
# dictionary to store values and indices of goal state.
GOAL_POSITIONS = {
            0 : (0,0), 1 : (0,1), 2 : (0,2),
            3 : (1,0), 4 : (1,1), 5 : (1,2),
            6 : (2,0), 7 : (2,1), 8 : (2,2)
                 } 
GOAL_VALUES = [
            [0, 1, 2], 
            [3, 4, 5], 
            [6, 7, 8]
               ]

ROW_LENGTH = 3





class Node:
    def __init__(self, state, parent=None, action=None, g=0, h="h1"):
        self.state = state   # current state of puzzle
        self.parent = parent # parent node of current node
        self.action = action # up down left right . . . 
        self.g = g           # the cost/depth from the start node to this node.
        
        # defining our h1, h2, and h3 heuristics
        if h == "h1":
            self.h = self.manhattanDistance()
        elif h == "h2":
            self.h = self.misplacedTiles()
        # elif h == "h3":
        #     self.h = self.linearConflict()
        else:
            print("invalid heuristic")

        self.f = self.g + self.h
    
    def manhattanDistance(self): # calculates the manhattan distance
        
        distance = 0 # distance for each tile to goal tile
        
        for i in range(0, ROW_LENGTH):
            for j in range(0, ROW_LENGTH):
                tile = self.state[i][j]
                if tile != 0:
                    # finding the distance of how far away this tile is to it's goal position
                    x, y = GOAL_POSITIONS[tile]
                    distance += abs(i - x) + abs(j - y)
        return distance
    
    def misplacedTiles(self):
        tiles = 0
        for i in range(0, ROW_LENGTH):
            for j in range(0, ROW_LENGTH):
                tile = self.state[i][j]
                if tile != 0 and tile != GOAL_VALUES[i][j]: # if the tile at state[i] i doesn't match goal[i] then increment counter
                    tiles += 1 
        return tiles
    

                    
