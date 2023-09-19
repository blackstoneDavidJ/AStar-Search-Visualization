import random
from enum import Enum

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def random_maze(grid_size, grid, gridSquareEdge) -> tuple:
    stack = []
    visited_grid = create_grid(grid_size)
    startX = grid_size // 2
    startY = grid_size // 2
    # Pick initial starting point
    init_cell = Cell(startX, startY)

    # Push the initial cell to the stack and mark it as visited
    visited_grid[startX][startY] = True
    stack.append(init_cell)

    # While the stack is not empty
    while len(stack) > 0:
        curr_cell = stack.pop()
        cells = get_cell_neighbors(grid_size, curr_cell, visited_grid)

        if cells:
            stack.append(curr_cell)
            cell = random.choice(cells)
            rand_cell = cell[0]
            rand_cell_dir = cell[1]

            gridSquareEdge[curr_cell.x][curr_cell.y].faces.append(rand_cell_dir)
            if rand_cell_dir == Direction.NORTH:
                gridSquareEdge[rand_cell.x][rand_cell.y].faces.append(Direction.SOUTH)
            if rand_cell_dir == Direction.SOUTH:
                gridSquareEdge[rand_cell.x][rand_cell.y].faces.append(Direction.NORTH)
            if rand_cell_dir == Direction.EAST:
                gridSquareEdge[rand_cell.x][rand_cell.y].faces.append(Direction.WEST)
            if rand_cell_dir == Direction.WEST:
                gridSquareEdge[rand_cell.x][rand_cell.y].faces.append(Direction.EAST)

            visited_grid[rand_cell.x][rand_cell.y] = True
            stack.append(rand_cell)

    grids = (grid, gridSquareEdge)
    return grids


def get_cell_neighbors(grid_size, cell, visited_grid) -> list:
    cell_neighbors = []

    # Define the possible relative coordinates of neighboring cells
    neighbors = [
        Direction.NORTH,
        Direction.WEST,Direction.EAST,
        Direction.SOUTH
    ]

    for i in neighbors:
        # Calculate the coordinates of the potential neighbor
        dx = i.value[0]
        dy = i.value[1]
        neighbor_x, neighbor_y = cell.x + dx, cell.y + dy

        # Check if the potential neighbor is within the grid bounds
        if 0 <= neighbor_x < grid_size and 0 <= neighbor_y < grid_size:
            # Check if the potential neighbor has not been visited
            if not visited_grid[neighbor_x][neighbor_y]:
                cell_neighbors.append((Cell(neighbor_x, neighbor_y), i.name))

    return cell_neighbors

def grid_to_cell_grid(grid, grid_size) -> list:
    cell_grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(Cell(i, j))
        cell_grid.append(row)
    
    print(cell_grid)
    return cell_grid

def create_grid(dimension):
    return [[False] * dimension for _ in range(dimension)]