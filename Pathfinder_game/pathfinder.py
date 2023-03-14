import curses
from curses import wrapper
import queue
import time

# O = maze entrance
# X = maze exit
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"] 
]

def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze): #enumerate - provides index + value; i indicates which row we're on
        for j, value in enumerate(row): #j indicates which column
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED) #draw at the current position
            else:
                stdscr.addstr(i, j*2, value, BLUE)

def find_start(maze, start): #determines starting spot, maze can be rearranged
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
            
    return None    

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_spot = find_start(maze, start)

    q = queue.Queue() #first in - first out
    q.put((start_spot, [start_spot])) #insert first q element - start spot; path stored in the list with each consecutive check

    visited = set()

    while not q.empty():
        current_pos, path = q.get() 
        row, col = current_pos 

        stdscr.clear() #clears terminal
        print_maze(maze, stdscr, path) #draws progress through the maze
        time.sleep(0.2) #processing delay for better visual representation
        stdscr.refresh() #updates path via terminal refresh

        if maze[row][col] == end: #maze exit check and final path print
            return path
        
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors: #obstacle / visited check
            if neighbor in visited: #skip visited
                continue

            r, c = neighbor #r = row, c = col
            if maze[r][c] == "#": #check whether neighbor is an obstacle
                continue

            new_path = path + [neighbor] #add non-obstacle to q for checks
            q.put((neighbor, new_path)) 
            visited.add(neighbor)
        
def find_neighbors(maze, row, col): 
    neighbors = []

    if row > 0: #moves up
        neighbors.append((row-1, col))
    elif row +1 < len(maze): #down
        neighbors.append((row + 1, col))
    elif col > 0: #left
        neighbors.append((row, col - 1))
    elif col + 1 < len(maze[0]): #right
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr): #stdscr - standart output screen
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #color pairs require an id (X)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    blue_and_black = curses.color_pair(1)

    find_path(maze, stdscr)
    stdscr.getch() #getch - get character -- waiting for user input in order to proceed

wrapper(main)
