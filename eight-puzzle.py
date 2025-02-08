from heapq import heappush, heappop
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

MOVES = [
  ("up", -1, 0),
  ("down", 1, 0),
  ("left", 0, -1),
  ("right", 0, 1)
]

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
            raise ValueError("Invalid heuristic")

        self.f = self.g + self.h # used in A* f(n) = g(n) + h(n). Cost of reaching the goals from start node.
    def __lt__(self, other):
        return self.f < other.f
    def manhattanDistance(self): # calculates the manhattan distance. Heuristic 1
        
        distance = 0 # distance for each tile to goal tile
        # finding the distance of how far away this tile is to it's goal position
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                tile = self.state[i][j]
                if tile != 0: 
                    x, y = GOAL_POSITIONS[tile]
                    distance += abs(i - x) + abs(j - y)
        return distance
    
    def misplacedTiles(self): # calculate the number of misplaced tiles in the puzzle. Heuristic 2
        tiles = 0
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                tile = self.state[i][j]
                if tile != 0 and tile != GOAL_VALUES[i][j]: # if the tile at state[i][j] doesn't match goal[i][j] then increment counter
                    tiles += 1 
        return tiles
    
    #Implement 3rd heuristic here.
    def thirdHeuristic(self):
        pass
class Solver:
    def __init__(self, initial_state, h="h1"): # constructor set default heuristic to h1
        self.initial_state = initial_state
        self.h = h
    
    def convert1D(self, state): # May convert arrays to 1d to improve efficiency. 
        return [tile for row in state for tile in row]
    
    def find0(self, state): # find the 0 (blank) in the puzzle 
        for i in range(ROW_LENGTH):
            for j in range(ROW_LENGTH):
                if state[i][j] == 0:
                    return i, j
        return None  # Return None if no blank tile is found

    def getNeighbours(self, node): # get the neighbours of current node.
        
        i, j = self.find0(node.state) # find blank tile location at [i][j]
        neighbours = [] # array to store node neighbours = list of possible moves.

        # loop through MOVES
        for action, di, dj in MOVES: 

            newI = i + di # calculate new row position
            newJ = j + dj #       and new col position

            if (0 <= newI < ROW_LENGTH) and (0 <= newJ < ROW_LENGTH): # make sure the [newI][newJ] exists inside puzzle 

                newState = [] # create list to copy rows from node

                for row in node.state:
                    newState.append(row[:]) # add the rows to newState

                # swap the blank tile with the blank tile's new position (it's neighbour)
                temp = newState[i][j]
                newState[i][j] = newState[newI][newJ]
                newState[newI][newJ] = temp
                
                neighbours.append(Node(newState, node, action, node.g + 1, self.h)) # create and add node into neighbours array

        return neighbours
    def aStar(self):
        start = Node(self.initial_state, h=self.h) # create starting note with given state + heuristic.
        pq = [] # priority queue of nodes to be explored
        heappush(pq, (start.f, start)) # its f(n) = g(n) + h(n) value that was calculated in Node class constructor is the Node's priority in the PQ.
        visited = set() # create a set in order to avoid duplicate nodes from being explored in A*

        while pq:
            _, current = heappop(pq) # grab the node with the lowest f value (best cost)
            equals = True

            # compare every value in the current state with every value in the goal state.
            for i in range(ROW_LENGTH):
                for j in range(ROW_LENGTH):
                    if current.state[i][j] != GOAL_VALUES[i][j]:
                        equals = False
                        break
            if equals: # if every value is equal, we know we are at the right state and we can return the path
                return self.reconstructPath(current)
            
            visited.add(tuple(map(tuple, current.state)))

            for neighbour in self.getNeighbours(current):
                if tuple(map(tuple, neighbour.state)) not in visited:
                    heappush(pq, (neighbour.f, neighbour))
        return None

    def reconstructPath(self, node):
        path = []
        while node.parent:
          path.append(node.action)
          node = node.parent
        return path[::-1]
      
if __name__ == "__main__":
    initial_state = [
        [0, 8, 7],
        [2, 1, 4],
        [3, 6, 5]
    ]
    solve = Solver(initial_state, h="h2")
    solution = solve.aStar()

    if solution:
        print("SOLUTION FOUND: ", solution)
    else:
        print("NO SOLUTION")