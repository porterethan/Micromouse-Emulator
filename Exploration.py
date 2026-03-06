from romi import Romi
import time
import board
import digitalio
from adafruit_debouncer import Debouncer

pin = digitalio.DigitalInOut(board.IO14)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

robot = Romi() 

# AVAILABLE FUNCTIONS
# moveSquare() - moves 10 inches
# turnRight() - turns 90 degrees
# turnLeft() - turns -90 degrees
# frontWall() - returns 1 if the the front sensor detects a wall in the occupied square

DIR = ["N", "E", "S", "W"]
STACK = []

DELTA = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1)
}

SIZE = 12
visited = [[False for _ in range(SIZE)] for _ in range(SIZE)]

def create_board():
    b = [["*" for _ in range(12)] for _ in range(12)]
    for i in range(12):
        b[i][11] = "1"
        b[11][i] = "1"
        b[i][0] = "1"
        b[0][i] = "1"
    return b

def print_board(b):
    print()
    for r in b:
        print(" ".join(r))
    print()

maze = create_board()

start_r = 1
start_c = 1
row = start_r
col = start_c

direction = 1  # 0 is starting N, 1 is E...
    
#Temporary Solution
def detect_walls():
    global row, col, direction

    robot.getWalls()
    front = robot.frontWall()
    left = robot.leftWall()
    right = robot.rightWall()
    print(f"front wall: {front}")
    print(f"left wall: {left}")
    print(f"right wall: {right}")

    # FRONT
    if front:
        dr, dc = DELTA[DIR[direction]]
        nr = row + dr
        nc = col + dc
        if 0 <= nr < 12 and 0 <= nc < 12:
            maze[nr][nc] = "1"

    # LEFT
    left_dir = (direction - 1) % 4
    if left:
        dr, dc = DELTA[DIR[left_dir]]
        nr = row + dr
        nc = col + dc
        if 0 <= nr < 12 and 0 <= nc < 12:
            print("LEFT WALL DETECTED")
            maze[nr][nc] = "1"

    # RIGHT
    right_dir = (direction + 1) % 4
    if right:
        dr, dc = DELTA[DIR[right_dir]]
        nr = row + dr
        nc = col + dc
        if 0 <= nr < 12 and 0 <= nc < 12:
            maze[nr][nc] = "1"
            
def turn_to(new_dir):
    global direction

    while direction != new_dir:
        if DIR[direction] == "S":
            if DIR[new_dir] == "E":
                robot.turnLeft()
                direction = (direction - 1) % 4
            elif DIR[new_dir] == "W":
                robot.turnRight()
                direction = (direction + 1) % 4
            else:
                robot.turnRight()
                robot.turnRight()
                direction = (direction + 2) % 4
        elif DIR[direction] == "N":
            if DIR[new_dir] == "W":
                robot.turnLeft()
                direction = (direction - 1) % 4
            elif DIR[new_dir] == "E":
                robot.turnRight()
                direction = (direction + 1) % 4
            else:
                robot.turnRight()
                robot.turnRight()
                direction = (direction + 2) % 4
        elif DIR[direction] == "E":
            if DIR[new_dir] == "N":
                robot.turnLeft()
                direction = (direction - 1) % 4
            elif DIR[new_dir] == "S":
                robot.turnRight()
                direction = (direction + 1) % 4
            else:
                robot.turnRight()
                robot.turnRight()
                direction = (direction + 2) % 4
        elif DIR[direction] == "W":
            if DIR[new_dir] == "S":
                robot.turnLeft()
                direction = (direction - 1) % 4
            elif DIR[new_dir] == "N":
                robot.turnRight()
                direction = (direction + 1) % 4
            else:
                robot.turnRight()
                robot.turnRight()
                direction = (direction + 2) % 4
        else:
            print("Else")
            robot.turnRight()
            robot.turnRight()
            direction = (direction + 2) % 4
            
        time.sleep(0.1)

def move_forward():
    global row, col
    robot.moveSquare() 
    dr, dc = DELTA[DIR[direction]]
    row += dr
    col += dc
    time.sleep(0.5)
    
def explore():
    global row, col

    visited[row][col] = True
    maze[row][col] = "V"
    print_board(maze)

    detect_walls()

    for new_dir in range(4):

        dr, dc = DELTA[DIR[new_dir]]
        new_r = row + dr
        new_c = col + dc

        if maze[new_r][new_c] == "1":
            print(f"{DIR[new_dir]} is wall")
            continue

        if visited[new_r][new_c]:
            continue

        STACK.append((row, col))
    
        print(f"Should turn to {DIR[new_dir]}")
        turn_to(new_dir)
        move_forward()

        explore()  

        prev_r, prev_c = STACK.pop()

        for d in range(4):
            if row + DELTA[DIR[d]][0] == prev_r and col + DELTA[DIR[d]][1] == prev_c:
                turn_to(d)
                break

        move_forward()
    
while True:
    switch.update()
    if switch.fell:
        detect_walls()
        print("Beginning Exploration")
        maze[row][col] = "X"
        print_board(maze)
        explore()
        print_board(maze)
    time.sleep(0.01)