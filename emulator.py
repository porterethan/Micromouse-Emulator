class Emulator:
    def __init__(self, board, robot, driver): 
        self.board = board
        self.driver = driver
        self.robot = robot
        
    def run(self):
        for _ in range(1000):
            if(self.board.is_goal(self.robot.curr_pos)):
                return "SUCCESS"
            self.driver.step(self.robot, self.board)
        return "FAILED (loop)"
  

class Board:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.size = len(grid) * len(grid[0]) if grid else 0

    def is_wall(self, pos):
        row, col = pos
        return self.grid[row][col] == 1

    def is_goal(self, pos):
        return pos == self.goal

    def printBoard(self):
        print("Goal at:", self.goal)
        for row in self.grid:
            for c in row:
                print(c, end='')
            print()


class BoardLoader:
    @staticmethod
    def from_file(filename):
        grid = []
        start = None
        goal = None

        with open(filename, "r") as f:
            lines = f.readlines()
            lines = [line.rstrip("\n") for line in lines]
            maze_2d = [list(line) for line in lines]

            for i, row in enumerate(maze_2d):
                for j, char in enumerate(row):
                    if char == 'S':
                        start = (i, j)
                        maze_2d[i][j] = "S"
                    elif char == 'G':
                        goal = (i, j)
                        maze_2d[i][j] = "G"
                    elif char in ('|', '+', '-'):
                        maze_2d[i][j] = 1
                    else:
                        maze_2d[i][j] = " "

        return Board(maze_2d, start, goal)
class RightHandDriver:
    def step(self, robot, board):
        if robot.can_move_right(board):
            robot.turn_right()
            robot.move_forward(board)
        elif robot.can_move_forward(board):
            robot.move_forward(board)
        else:
            robot.turn_left()
            
            
class RandomDriver:
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
            
def run_simulation(board_file, driver_class, board_name, driver_name):
    print(f"\n--- {board_name} Board | {driver_name} ---")
    
    try:
        board = BoardLoader.from_file(board_file)
        robot = Robot(board.start, board.goal)
        driver = driver_class()
        emulator = Emulator(board, robot, driver)
        
        result = emulator.run()
        print(f"Result: {result}")
        
        result_obj = Result(robot)
        result_obj.statusReport()
        print()
        
    except FileNotFoundError:
        print(f"Error: Board file '{board_file}' not found!")
    except Exception as e:
        print(f"Error running simulation: {e}")

class Robot:
    DIR = ["N", "E", "S", "W"]
    DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    def __init__(self, start_pos, goal_pos):
        self.curr_pos = start_pos
        self.goal_pos = goal_pos
        self.direction = "S"  # Start facing South
        self.is_found = False
        self.steps = 0  

    def _get_next_pos(self, direction):
        dr, dc = self.DELTA[direction]
        row, col = self.curr_pos
        return (row + dr, col + dc)

    def can_move_right(self, board):
        right_idx = (self.DIR.index(self.direction) + 1) % 4
        right_dir = self.DIR[right_idx]
        next_pos = self._get_next_pos(right_dir)
        return not board.is_wall(next_pos)
    
    def can_move_left(self, board):
        left_idx = (self.DIR.index(self.direction) - 1) % 4
        left_dir = self.DIR[left_idx]
        next_pos = self._get_next_pos(left_dir)
        return not board.is_wall(next_pos)
    
    def can_move_forward(self, board):
        next_pos = self._get_next_pos(self.direction)
        return not board.is_wall(next_pos)
            
    def turn_right(self):
        idx = self.DIR.index(self.direction)
        self.direction = self.DIR[(idx + 1) % 4]

    def turn_left(self):
        idx = self.DIR.index(self.direction)
        self.direction = self.DIR[(idx - 1) % 4]

    def move_forward(self, board):
        next_pos = self._get_next_pos(self.direction)
        
        if not board.is_wall(next_pos):
            self.curr_pos = next_pos
            self.steps += 1
            return True
        return False
class Result:
    def __init__(self, robot):
        self.robot = robot
    
    def statusReport(self):
        print(f"Final position: {self.robot.curr_pos}")
        print(f"Total steps: {self.robot.steps}")
        print(f"Final direction: {self.robot.direction}")


def main():
    board = BoardLoader.from_file("/Users/ethanporter/CS Projects/Micromouse Project/boards/file.txt")
    robot = Robot(board.start, board.goal)
    driver = RightHandDriver()
    emulator = Emulator(board, robot, driver)
    result = emulator.run()
    print(result)
    
    result_obj = Result(robot)
    result_obj.statusReport()


if __name__ == "__main__":
    main()