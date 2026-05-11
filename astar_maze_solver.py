import random
import heapq
import matplotlib.pyplot as plt
import numpy as np
def generate_maze(rows, cols, wall_probability=0.3):
    maze = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < wall_probability:
                row.append('#')   # wall
            else:
                row.append('.')   # free space
        maze.append(row)
    maze[0][0] = 'S'                 # start
    maze[rows - 1][cols - 1] = 'G'   # goal
    return maze

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(maze, start, goal):
    priority_queue = [(0, start)]
    parent_map = {}
    cost_so_far = {start: 0}
    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        x, y = current
        if current == goal:
            path = []
            while current in parent_map:
                path.append(current)
                current = parent_map[current]
            path.append(start)
            return path[::-1]
        for d in "ESNW":
            if d == 'E':
                nx, ny = x, y + 1
            elif d == 'S':
                nx, ny = x + 1, y
            elif d == 'N':
                nx, ny = x - 1, y
            else:  # W
                nx, ny = x, y - 1
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] != '#':
                    neighbor = (nx, ny)
                    new_cost = cost_so_far[current] + 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        parent_map[neighbor] = current
                        priority = new_cost + heuristic(neighbor, goal)
                        heapq.heappush(priority_queue, (priority, neighbor))
    return None

def visualize_maze(maze, path=None):
    rows, cols = len(maze), len(maze[0])
    grid = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == '#':
                grid[i][j] = 1
            elif maze[i][j] == 'S':
                grid[i][j] = 2
            elif maze[i][j] == 'G':
                grid[i][j] = 3
    if path:
        for x, y in path:
            if maze[x][y] not in ('S', 'G'):
                grid[x][y] = 4
    plt.imshow(grid)
    plt.title("A* Maze Solver")
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
rows, cols = map(int, input("Enter rows ,cols: ").split())
maze = generate_maze(rows, cols)
start = (0, 0)
goal = (rows - 1, cols - 1)
path = a_star_search(maze, start, goal)
print("\nResult:")
print("No path found" if not path else "Path found!")
visualize_maze(maze, path)