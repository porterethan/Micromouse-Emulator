import time
import os
import random

class Emulator:
    def __init__(self, board, robot, driver, live_run=False):
        self.board = board
        self.robot = robot
        self.driver = driver
        self.live_run = live_run

    def run(self):
        for _ in range(1000):
            if self.board.is_goal(self.robot.curr_pos):
                return "SUCCESS"
            self.driver.step(self.robot, self.board)
            if not self.live_run:
                os.system("cls" if os.name == "nt" else "clear")
                self.board.printBoard(self.robot)
                time.sleep(0.05)
        return "FAILED (loop)"


class Board:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    def is_wall(self, pos):
        r, c = pos
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
            return True
        return self.grid[r][c] == 1

    def is_goal(self, pos):
        return pos == self.goal

    def printBoard(self, robot):
        print("\n" + "-" * 30)
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if (i, j) == robot.curr_pos:
                    print("*", end="")
                elif (i, j) == self.goal:
                    print("G", end="")
                elif cell == 1:
                    print("1", end="")
                else:
                    print(" ", end="")
            print()
        print("-" * 30)


class BoardLoader:
    @staticmethod
    def from_file(filename):
        grid = []
        start = None
        goal = None
        with open(filename, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
            maze = [list(line) for line in lines]
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == "S":
                    start = (i, j)
                    maze[i][j] = " "
                elif maze[i][j] == "G":
                    goal = (i, j)
                    maze[i][j] = " "
                elif maze[i][j] in ("|", "+", "-"):
                    maze[i][j] = 1
                else:
                    maze[i][j] = " "
        return Board(maze, start, goal)


class RightHandDriver:
    def step(self, robot, board):
        if robot.can_move_right(board):
            robot.turn_right()
            robot.move_forward(board)
        elif robot.can_move_forward(board):
            robot.move_forward(board)
        else:
            robot.turn_left()


class LeftHandDriver:
    def step(self, robot, board):
        if robot.can_move_left(board):
            robot.turn_left()
            robot.move_forward(board)
        elif robot.can_move_forward(board):
            robot.move_forward(board)
        else:
            robot.turn_right()


class RandomDriver:
    def step(self, robot, board):
        options = []
        if robot.can_move_forward(board):
            options.append("F")
        if robot.can_move_right(board):
            options.append("R")
        if robot.can_move_left(board):
            options.append("L")
        if not options:
            robot.turn_right()
            return
        choice = random.choice(options)
        if choice == "F":
            robot.move_forward(board)
        elif choice == "R":
            robot.turn_right()
            robot.move_forward(board)
        elif choice == "L":
            robot.turn_left()
            robot.move_forward(board)


class Result:
    def __init__(self, robot):
        self.robot = robot

    def statusReport(self):
        print(f"Final position: {self.robot.curr_pos}")
        print(f"Total steps: {self.robot.steps}")
        print(f"Final direction: {self.robot.direction}")
