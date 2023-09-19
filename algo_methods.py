from asyncio.windows_events import NULL
from enum import Enum
import pygame_gui
import random 
import mazecreator as mc

GRID_DIM = 10
SQUARE_SIZE = 500 // GRID_DIM

class Node:
    gCost = 0
    hCost = 0
    parent = NULL
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    def getFCost(self):
        return self.gCost + self.hCost

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

class Edge:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.faces = []

    def __str__(self):
        return f"Edge at ({self.x}, {self.y}), Faces: {[face.name for face in self.faces]}"

def create_2d_edge_list(rows, cols):
    edge_matrix = [[Edge(x, y) for y in range(cols)] for x in range(rows)]
    return edge_matrix

gridSquareEdges = create_2d_edge_list(GRID_DIM, GRID_DIM)

mouseX = 0
mouseY = 0
distanceArray = []

def createGrid(dimension, val):
    if dimension < 1:
        raise ValueError("Dimension must be at least 1.")
    
    grid = [[val] * dimension for _ in range(dimension)]
    
    return grid
gridSquare = createGrid(GRID_DIM,0)
grids = mc.random_maze(GRID_DIM, gridSquare, gridSquareEdges)
gridSquare = grids[0]
gridSquareEdges = grids[1]
nodeVisited = []
nodeList = []
queueList = []
startPlaced = False
drawingWall = False
useDiagonalMovements = False
startX = 0
startY = 0
endX = GRID_DIM-1
endY = GRID_DIM-1

for i in range(GRID_DIM):
    for j in range(GRID_DIM):
        if gridSquare[i][j] == 2:
            startX = i
            startY = j
        elif gridSquare[i][j] == 3:
            endX = i
            endY = j

def create_random_maze() -> tuple:
    gridSquareEdges = create_2d_edge_list(GRID_DIM, GRID_DIM)
    gridSquare = createGrid(GRID_DIM,0)
    grids = mc.random_maze(GRID_DIM, gridSquare, gridSquareEdges)
    gridSquare = grids[0]
    gridSquareEdges = grids[1]
    return grids

def init_arrays():
    for row in range(GRID_DIM):
        distanceArray.append([])
        nodeVisited.append([])
        for column in range(GRID_DIM):
            distanceArray[row].append(0)
            nodeVisited[row].append(False)

def is_valid_node(x, y):
    return (x >= 0) and (x < GRID_DIM) and (y >= 0) and (y < GRID_DIM) and gridSquare[x][y] != 1

def in_list(currlist, x, y):
    for node in currlist:
        if node.x == x and node.y == y:
            return True
    return False

def clear_grid():
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            if gridSquare[x][y] == 5:
                    gridSquare[x][y] = 0
def reset_grid():
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            gridSquare[x][y] = random.randint(0, 1)
    try:
        solve_a_star_maze()
        clear_grid()     
    except IndexError:
        reset_grid()

def get_distance(currNode, goalNode):
    distX = abs(currNode.x - goalNode.x)
    distY = abs(currNode.y - goalNode.y)
    
    if distX > distY:
        return 14 * distY + 10 * (distX - distY)
    return 14 * distY + 10 * (distY - distX)
    
def get_end_node(closedList, x, y):
    for node in closedList:
        if node.x == x and node.y == y:
            return node
    return False    

def solve_a_star_maze():
    try:
        openList = []
        closedList = []
        if useDiagonalMovements:
            xList = [1, -1, 0, 0, -1, 1, -1, 1]
            yList = [0, 0, -1, 1, 1, -1, -1, 1]
        else:
            xList = [1, -1, 0, 0]
            yList = [0, 0, -1, 1]
        startNode = Node(startX, startY)
        endNode = Node(endX, endY)
        openList.append(startNode)
        endFound = False
        while len(openList) > 0 or not endFound:
            currNode = openList[0]
            for i in range(len(openList)):
                if(openList[i].getFCost() < currNode.getFCost()) or openList[i].getFCost() == currNode.getFCost() and openList[i].hCost < currNode.hCost:
                    currNode = openList[i]
            openList.remove(currNode)
            closedList.append(currNode)
            
            if currNode.x == endX and currNode.y == endY:
                endFound = True 

            neighborList = []
            for i in range(len(xList)):
                currX = currNode.x + xList[i]
                currY = currNode.y + yList[i]
                if is_valid_node(currX, currY):
                    neighborList.append(Node(currX, currY))
            
            for node in neighborList:
                if not in_list(closedList, node.x, node.y):
                    newMovementCost = currNode.gCost + get_distance(currNode, node)
                    if not in_list(openList, node.x, node.y) or newMovementCost < node.gCost:
                        node.gCost = newMovementCost
                        node.hCost = get_distance(node, endNode)
                        node.parent = currNode
                        if not in_list(openList, node.x, node.y):
                            openList.append(node)
            neighborList.clear()
        
        curr = get_end_node(closedList, endX, endY)
        path = []
        while curr != startNode:
            path.append(curr)
            curr = curr.parent
        
        path.reverse()
        for node in path:
            gridSquare[node.x][node.y] = 5
        return closedList
    except IndexError:
        raise IndexError