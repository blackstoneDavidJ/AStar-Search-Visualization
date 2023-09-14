from asyncio.windows_events import NULL
from cgitb import reset
from tracemalloc import start
import pygame, sys, math
import numpy as np

SCREEN_HEIGHT = 1280
SCREEN_WIDTH = 1280
GRID_DIM = 80
SQUARE_SIZE = SCREEN_WIDTH // GRID_DIM
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fpsClock = pygame.time.Clock()

class Node:
    gCost = 0
    hCost = 0
    parent = NULL
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    
    def getFCost(self):
        return self.gCost + self.hCost
    

mouseX = 0
mouseY = 0
distanceArray = []
def createGrid(dimension):
    if dimension < 1:
        raise ValueError("Dimension must be at least 1.")
    
    grid = [[0] * dimension for _ in range(dimension)]
    
    return grid

gridSquare = createGrid(GRID_DIM)
nodeVisited = []
nodeList = []
queueList = []
startPlaced = False
drawingWall = False
useDiagonalMovements = False
startX = 0
startY = 0
endX = 9
endY = 9

for i in range(GRID_DIM):
    for j in range(GRID_DIM):
        if gridSquare[i][j] == 2:
            startX = i
            startY = j
        elif gridSquare[i][j] == 3:
            endX = i
            endY = j

def initArrays():
    for row in range(GRID_DIM):
        distanceArray.append([])
        nodeVisited.append([])
        for column in range(GRID_DIM):
            distanceArray[row].append(0)
            nodeVisited[row].append(False)
            
def createInitBoard():
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            pygame.draw.rect(screen, color, pygame.Rect(SQUARE_SIZE * y, SQUARE_SIZE * x, SQUARE_SIZE, SQUARE_SIZE), 1)

def isValidNode(x, y):
    return (x >= 0) and (x < GRID_DIM) and (y >= 0) and (y < GRID_DIM) and gridSquare[x][y] != 1

def inList(currlist, x, y):
    for node in currlist:
        if node.x == x and node.y == y:
            return True
    return False

def resetGrid():
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            gridSquare[x][y] = 0

def getDistance(currNode, goalNode):
    distX = abs(currNode.x - goalNode.x)
    distY = abs(currNode.y - goalNode.y)
    
    if distX > distY:
        return 14 * distY + 10 * (distX - distY)
    return 14 * distY + 10 * (distY - distX)
    
def getEndNode(closedList, x, y):
    for node in closedList:
        if node.x == x and node.y == y:
            return node
    return False    

def solveMazeAStar():
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
            if isValidNode(currX, currY):
                neighborList.append(Node(currX, currY))
        
        for node in neighborList:
            if not inList(closedList, node.x, node.y):
                newMovementCost = currNode.gCost + getDistance(currNode, node)
                if not inList(openList, node.x, node.y) or newMovementCost < node.gCost:
                    node.gCost = newMovementCost
                    node.hCost = getDistance(node, endNode)
                    node.parent = currNode
                    if not inList(openList, node.x, node.y):
                        openList.append(node)
        neighborList.clear()
    
    curr = getEndNode(closedList, endX, endY)
    path = []
    while curr != startNode:
        path.append(curr)
        curr = curr.parent
    
    path.reverse()
    for node in path:
        gridSquare[node.x][node.y] = 5
    return closedList

while(True):
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            mouseY = int(pos[0] / SQUARE_SIZE)
            mouseX = int(pos[1] / SQUARE_SIZE)
            if drawingWall:
                gridSquare[mouseX][mouseY] = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            drawingWall = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawingWall = True
            pos = pygame.mouse.get_pos()
            mouseY = int(pos[0] / SQUARE_SIZE)
            mouseX = int(pos[1] / SQUARE_SIZE)
            if event.button == 3:
                if not startPlaced:
                    gridSquare[mouseX][mouseY] = 2
                    startX = mouseX
                    startY = mouseY
                    startPlaced = True
                else:
                    gridSquare[mouseX][mouseY] = 3
                    endX = mouseX
                    endY = mouseY
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                startPlaced = False
                resetGrid()
                queueList.clear()
                nodeList.clear()
                distanceArray.clear()
                initArrays()
                print("Start/End have been reset.")
            if event.key == pygame.K_s:
                print("Solver has started.")
                solveMazeAStar()
                gridSquare[endX][endY] = 3
            if event.key == pygame.K_d:
                if useDiagonalMovements == False:
                    useDiagonalMovements = True
                    print("Enabled: Diagonal Movements")
                else:
                    useDiagonalMovements = False
                    print("Disabled: Diagonal Movements")
                    
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            if gridSquare[x][y] == 1:
                color = (255,255,255)
            elif gridSquare[x][y] == 2:
                color = (0,255,0)
            elif gridSquare[x][y] == 3:
                color = (255,0,0)
            elif gridSquare[x][y] == 5:
                color = (255, 0, 255)
            else:
                color = (0,0,0)
            pygame.draw.rect(screen, color, pygame.Rect(SQUARE_SIZE * y, SQUARE_SIZE * x, SQUARE_SIZE, SQUARE_SIZE))
                
    pygame.display.set_caption("FPS: " +str(int(fpsClock.get_fps())) 
        +" X: " +str(mouseX)+"-Y: " +str(mouseY))
    pygame.display.flip()
    fpsClock.tick(FPS)