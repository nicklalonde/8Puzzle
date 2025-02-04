
import numpy as np
class BoardNode:
    def __init__(self, s):
        self.child = s
        self.parent = None
        self.gn = 0
        self.hn = 0
        self.fn = 0
    
    def getParentNode(self):
        return self.parent
    def getHn(self):
        return self.hn
    def getFn(self):
        return self.fn
    def getGn(self):
        return self.gn
    def getCurrentBoardState(self):
        return self.child
    def setHn(self, hn):
        self.hn = hn
    def setGn(self, gn):
        self.gn = gn
    def setParent(self, parent):
        self.parent = parent
    

    def exploreNode(fringe, exploredNodes, currentNode, goalNode, zero, g, count, heuristic):
        a = [list(item.getCurrentBoardState()) for item in exploredNodes]
        exploredNodes.append(currentNode)
        currentNodeArray = np.asarray(currentNode.getCurrentBoardState())

        if zero != 0 and zero != 3 and zero != 6:
            nodeCopy = currentNodeArray.copy()
            temp = nodeCopy[zero - 1]
            nodeCopy[zero - 1] = currentNodeArray[zero]
            nodeCopy[zero] = temp
            distance = Distance.distance(nodeCopy, goalNode, heuristic)
            count += 1

            if not list(nodeCopy) in a:
                nodeCopy = BoardNode(nodeCopy)
                nodeCopy.setGn(g)
                nodeCopy.setHn(distance)
                nodeCopy.setParent(currentNode)
                fringe.append(nodeCopy)
        
        if zero != 6 and zero != 7 and zero != 8:
            nodeCopy = currentNodeArray.copy()
            temp = nodeCopy[zero + 3]
            nodeCopy[zero + 3] = currentNodeArray[zero]
            nodeCopy[zero] = temp
            distance = Distance.distance(nodeCopy, goalNode, heuristic)
            count += 1
            if not list(nodeCopy) in a:
                nodeCopy = BoardNode(nodeCopy)
                nodeCopy.setGn(g)
                nodeCopy.setHn(distance)
                nodeCopy.setParent(currentNode)
                fringe.append(nodeCopy)

        if zero != 2 and zero != 5 and zero != 8:
            nodeCopy = currentNodeArray.copy()
            temp = nodeCopy[zero + 1]
            nodeCopy[zero + 1] = currentNodeArray[zero]
            nodeCopy[zero] = temp
            distance = Distance.distance(nodeCopy, goalNode, heuristic)
            count += 1
            if not list(nodeCopy) in a:
                nodeCopy = BoardNode(nodeCopy)
                nodeCopy.setGn(g)
                nodeCopy.setHn(distance)
                nodeCopy.setParent(currentNode)
                fringe.append(nodeCopy)
        return count
    
    class Puzzle:
        def least_fn(fringe):
            fnFringe = []
            for i in range(len(fringe)):
                fnFringe.append(fringe[i].getFn())
            minimumFn = min(fnFringe)
            minimumFnIndex = fnFringe.index(minimumFn)
            return minimumFnIndex
        def print_state(node):
            print("g(n) = ", node.getGn(), "h(n) = ", node.getHn(), "f(n) = ", node.getFn(), "\n")
            print(node.getCurrentBoardState()[0], " | ", node.getCurrentBoardState()[1], " | ", node.getCurrentBoardState()[2])
            print("--------------")
            print(node.getCurrentBoardState()[3], " | ", node.getCurrentBoardState()[4], " | ", node.getCurrentBoardState()[5])
            print("--------------")
            print(node.getCurrentBoardState()[6], " | ", node.getCurrentBoardState()[7], " | ", node.getCurrentBoardState()[8])
        
        def goalReached(exploredNodes, count):
            nodesExpanded = len(exploredNodes) - 1
            path = []
            init = exploredNodes[0]
            curr = exploredNodes.pop()

            while init != curr:
                path.append(curr)
                curr = curr.getParent()
            path.append(init)
            path.reverse()

            for i in path:
                Puzzle.print_state()
            
            print("Goal Reached \n")
            print("The number of nodes expanded: " , nodes_expanded, "\n")
            print("The number of nodes generated: ", count, "\n")
            print("Path Cost: ", len(path)-1, "\n")

        def path(exploredNodes):
            exploredNodes.pop()
    
    class Distance:
        def distance(arr, goal, heurisitic):
            distance = 0
            if heuristic == 1:
                for i in range(8):
                    if arr[i] != goal[i]:
                        distance += 1
                return distance
            elif heurisitic == 2:
                arr = np.asarray(arr).reshape(3,3)
                goal = np.asarray(arr).reshape(3,3)

                for i in range(8):
                    a,b = np.where(arr == i + 1)
                    x,y = np.where(goal == i + 1)
                    distance = distance + abs((a-x_[0]) + abs(b - y)[0])
                return distance
def main():
    heuristic = input("Choose a Heuristic: \n 1. Misplaced Tiles \n 2. Manhattan Distance \n")
    heuristic=int(heuristic)

    initial_board=[]
    final_board=[]

    print("Enter the 8 puzzle problem: \n")

    for i in range(9):
        x = int(input())
        initial_board.append(x) 

    print("Enter the 8 puzzle goal: \n")

    for i in range(9):
        x = int(input())
        final_board.append(x) 

    initial_board   =   BoardNode(initial_board)
    final_board     =   BoardNode(final_board)
    explored_nodes  =   []
    fringe          =   [initial_board]
    distance        =   Distance.distance(initial_board.getCurrentBoardState(),final_board.getCurrentBoardState(),heuristic)
    fringe[0].setHn(distance)
    count=1

    print("---------------Printing Solution Path---------------\n \n")

    while not not fringe:
        minimum_fn_index    =   Puzzle.least_fn(fringe)
        current_node        =   fringe.pop(minimum_fn_index)
        g                   =   current_node.get_gn()+1
        goal_node           =   np.asarray(final_board.get_current_state())
        if np.array_equal(np.asarray(current_node.get_current_state()), goal_node ):
            distance    =   Distance.distance(np.asarray(current_node.get_current_state()),goal_node,heuristic)
            explored_nodes.append(current_node)
            Puzzle.goalReached(explored_nodes,count)
            fringe      =   []
        elif not np.array_equal(current_node, goal_node ):
            zero    =   np.where(np.asarray(current_node.get_current_state()) == 0)[0][0]
            count   =   BoardNode.expand_node(fringe, explored_nodes, current_node,goal_node, zero, g, count,heuristic)

if __name__ == '__main__':
    main()
   