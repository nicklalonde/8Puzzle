from heapq import heappush, heappop
from math import sqrt
import random
import pandas as pd
# dictionary to store values and indices of goal state.
#Primary Goal State
GOAL_POSITIONS_3 =  {0 : (0,0), 1 :(0,1), 2 : (1,0), 3 :(1,1)}
GOAL_VALUES_3 = ((0,1), (2,3))
GOAL_POSITIONS_8 = {
            0 : (0,0), 1 : (0,1), 2 : (0,2),
            3 : (1,0), 4 : (1,1), 5 : (1,2),
            6 : (2,0), 7 : (2,1), 8 : (2,2)
                 } 

GOAL_VALUES_8 = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8)
)

GOAL_POSITIONS_15 = {
    0 : (0, 0),  1: (0, 1),  2: (0, 2),  3: (0, 3),
    4: (1, 0),  5: (1, 1),  6: (1, 2),  7: (1, 3),
    8: (2, 0),  9: (2, 1), 10: (2, 2), 11: (2, 3),
    12: (3, 0), 13: (3, 1), 14: (3, 2), 15: (3, 3)
}
GOAL_VALUES_15 = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
    (12, 13, 14, 15)
)

MOVES = [
  ("up", -1, 0),
  ("down", 1, 0),
  ("left", 0, -1),
  ("right", 0, 1)
]

#List of 100 puzzles.
PUZZLES8 = []
PUZZLES15 = []
numPuzzles = 0
class Node:
    def __init__(self, state, parent=None, action=None, g=0, h="h1", puzzleType=8):
        self.state = tuple(map(tuple, state))   # current state of puzzle
        self.parent = parent # parent node of current node
        self.action = action # up down left right . . . 
        self.g = g           # the cost/depth from the start node to this node.
        
        # defining our h1, h2, and h3 heuristics
        if puzzleType == 8:
            self.goalPositions = GOAL_POSITIONS_8
            self.goalValues = GOAL_VALUES_8
            self.puzzleLength = 3
        elif puzzleType == 15:
            self.goalPositions = GOAL_POSITIONS_15
            self.goalValues = GOAL_VALUES_15
            self.puzzleLength = 4
        elif puzzleType == 3:
            self.goalPositions = GOAL_POSITIONS_3
            self.goalValues = GOAL_VALUES_3
            self.puzzleLength = 2
        else:
            raise ValueError("Invalid puzzle tpye")
        
        if h == "h1":
            self.h = self.manhattanDistance()
        elif h == "h2":
            self.h = self.misplacedTiles()
        # elif h == "h3":
        #     self.h = self.3rd()
        else:
            raise ValueError("Invalid heuristic")

        
        self.f = self.g + self.h # used in A* f(n) = g(n) + h(n). Cost of reaching the goals from start node.
    def __lt__(self, other):
        return self.f < other.f
    def manhattanDistance(self): # calculates the manhattan distance. Heuristic 1
        distance = 0 # distance for each tile to goal tile
        # finding the distance of how far away this tile is to it's goal position
        length = self.puzzleLength
        for i in range(length):
            for j in range(length):
                tile = self.state[i][j]
                if tile != 0: 
                    x, y = self.goalPositions[tile]
                    distance += abs(i - x) + abs(j - y)
        return distance
    
    def misplacedTiles(self): # calculate the number of misplaced tiles in the puzzle. Heuristic 2
        tiles = 0
        length = self.puzzleLength
        for i in range(length):
            for j in range(length):
                tile = self.state[i][j]
                if tile != 0 and tile != self.goalValues[i][j]: # if the tile at state[i][j] doesn't match goal[i][j] then increment counter
                    tiles += 1 
        return tiles
    
    #Implement 3rd heuristic here.
    def thirdHeuristic(self):
        pass
class Solver:
    def __init__(self, initial_state, h="h1", puzzleType=8): # constructor set default heuristic to h1
        self.initial_state = initial_state
        self.h = h
        self.nodes_expanded = 0
        self.puzzleType = puzzleType
        if puzzleType == 8:
            self.goalPositions = GOAL_POSITIONS_8
            self.goalValues = GOAL_VALUES_8
            self.puzzleLength = 3
        elif puzzleType == 15:
            self.goalPositions = GOAL_POSITIONS_15
            self.goalValues = GOAL_VALUES_15
            self.puzzleLength = 4
        elif puzzleType == 3:
            self.goalPositions = GOAL_POSITIONS_3
            self.goalValues = GOAL_VALUES_3
            self.puzzleLength = 2
        else:
            raise ValueError("Invalid puzzle type.")

    def find0(self, state): # find the 0 (blank) in the puzzle 
        length = self.puzzleLength
        for i in range(length):
            for j in range(length):
                if state[i][j] == 0:
                    return i, j
        return None  # Return None if no blank tile is found

    def getNeighbours(self, node): # get the neighbours of current node.
        
        i, j = self.find0(node.state) # find blank tile location at [i][j]
        neighbours = [] # array to store node neighbours = list of possible moves.

        # loop through MOVES
        for action, di, dj in MOVES: 

            newI = i + di # calculate new row position
            newJ = j + dj # and new col position
            length = self.puzzleLength
            if (0 <= newI < length ) and (0 <= newJ < length): # make sure the [newI][newJ] exists inside puzzle 

                newState = list(map(list, node.state))
                newState[i][j], newState[newI][newJ] = newState[newI][newJ], newState[i][j]
                neighbours.append(Node(tuple(map(tuple, newState)), node, action, node.g + 1, self.h, self.puzzleType)) # create and add node into neighbours array

        return neighbours
    
    def aStar(self):
        start = Node(self.initial_state, h=self.h, puzzleType=self.puzzleType) # create starting note with given state + heuristic.
        pq = [] # priority queue of nodes to be explored
        heappush(pq, (start.f, start)) # its f(n) = g(n) + h(n) value that was calculated in Node class constructor is the Node's priority in the PQ.
        visited = set() # create a set in order to avoid duplicate nodes from being explored in A*

        while pq:
            
            _, current = heappop(pq) # grab the node with the lowest f value (best cost)
            self.nodes_expanded += 1
            
            if current.state == self.goalValues:
                return self.getPath(current)
            
            if current.state in visited: # skip to next iteration as to not do same thing twice.
                continue
            visited.add(current.state)

            for neighbour in self.getNeighbours(current):
                heappush(pq, (neighbour.f, neighbour))

        return None
    
    def getPath(self, node):
        path = []
        while node.parent: # loop until the root node 
            path.append(node.action) # add every action to the path
            node = node.parent #point to parent node
        return path[::-1] # since we worked from completed puzzle node to the root node, we must reverse the path and return it.

def isSolvable(nums):
    size = sqrt(len(nums))
    inversions = 0
    zerow = 0
    solvable = False
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > 0 and nums[j] > 0 and nums[i] > nums[j]:
                count += 1
    if count % 2 == 0 and size == 3:
        return True
    elif size == 4:
        zerowIndex = nums.index(0)
        zerow = zerowIndex // size
        return (inversions + zerow) % 2 == 0
        
    
def generateRandomPuzzle(puzzleLength):
    while True:
        nums = random.sample(range(puzzleLength * puzzleLength), puzzleLength * puzzleLength) # Ensure unique values for puzzle size
        if isSolvable(nums):
            puzzle = tuple(
                tuple(nums[i * puzzleLength:(i + 1) * puzzleLength])
                for i in range(puzzleLength)
            )
            return puzzle
def main():
    results = []
    length = 0
    for puzzleType in [3]:
        for heuristic in ["h1", "h2"]:
            total_steps = 0
            total_nodes = 0
            solved_count = 0

            for _ in range(5):

                if puzzleType == 8:
                    length = 3
                elif puzzleType == 15:
                    length = 4
                elif puzzleType == 3:
                    length = 2

                puzzle = generateRandomPuzzle(length)
                print(puzzle)
                solver = Solver(puzzle, h=heuristic, puzzleType=puzzleType)
                solution = solver.aStar()

                if solution:
                    total_steps += len(solution)
                    total_nodes += solver.nodes_expanded
                    solved_count += 1

            # Compute averages
            avg_steps = total_steps / solved_count if solved_count > 0 else 0
            avg_nodes = total_nodes / solved_count if solved_count > 0 else 0

            # Store results
            results.append([f"{puzzleType}-puzzle", heuristic, avg_steps, avg_nodes])

    # Convert results into a Pandas DataFrame
    df = pd.DataFrame(results, columns=["Puzzle Type", "Heuristic", "Average Steps to Solution", "Average Nodes Expanded"])
    print(df)


if __name__ == "__main__":
    main()   