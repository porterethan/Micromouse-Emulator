from emulator import Emulator
from emulator import Board
from emulator import BoardLoader
from emulator import RightHandDriver
from emulator import LeftHandDriver
from emulator import Result

class Robot:
    DIR = ["N", "E", "S", "W"]
    DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    def __init__(self, start_pos=(0,0), goal_pos=(1,1), board_size=[10,10]):
        self.curr_pos = start_pos
        self.goal_pos = goal_pos
        self.start_pos = start_pos
        self.direction = "S"  
        self.is_found = False
        self.steps = 0
        self.board_size = board_size
        self.visited = set()
        self.visited.add(start_pos)
        self.path_stack = [self.start_pos] #Creates a stack to pop from and keep
        
        
        rows, cols = board_size
        self.roboard = [['*' for _ in range(cols)] for _ in range(rows)]
        
        start_row, start_col = start_pos
        self.roboard[start_row][start_col] = "X"
    
    def find_path(self, board, direction): 
        for direction in self.DIR:
            dr, dc = self.DELTA[direction]
            row, col = self.curr_pos
            next_pos = (row + dr, col + dc)
            next_row, next_col = row + dr, col + dc

            #This value will need to change in response to a real board.
            #This is where there will be an is_wall function that will
            #return a value and create the board
            if 0 <= next_row < len(self.roboard) and 0 <= next_col < len(self.roboard[0]):
                        if self.roboard[next_row][next_col] == "*":
                            if board.is_wall((next_row, next_col)):
                                self.roboard[next_row][next_col] = 1
                            elif board.is_goal((next_row, next_col)):
                                self.roboard[next_row][next_col] = "G"
                            else:
                                self.roboard[next_row][next_col] = 0
    
    #Checks if the move is valid, not sensing if it is a wall
    def is_valid_move(self, r, c): 
        return (0 <= r < len(self.roboard) and 0 <= c < len(self.roboard[0]) and
        self.roboard[r][c] != 1 and (r,c) not in self.visited)
        
        
    def move(self):
        for direction in self.DIR:
            next_row, next_col = self.get_next_pos(direction)

            if self.is_valid_move(next_row, next_col):
                curr_row, curr_col = self.curr_pos
                self.roboard[curr_row][curr_col] = 0  

                self.curr_pos = (next_row, next_col)
                self.visited.add(self.curr_pos)
                self.path_stack.append(self.curr_pos)


                if self.roboard[next_row][next_col] == "G":
                    self.is_found = True
                    return

                self.roboard[next_row][next_col] = "X"
                self.steps += 1
                return 
        self.backtrack()

    
    def backtrack(self):
        if len(self.path_stack) <= 1:
            return
        
        self.path_stack.pop()
        
        prev_pos = self.path_stack[-1]
        curr_row, curr_col = self.curr_pos
        
        self.roboard[curr_row][curr_col] = 0
        
        self.curr_pos = prev_pos
        pr, pc = prev_pos
        self.roboard[pr][pc] = "X"
    
    def check_for_ast(self):
        return any("*" in sublist for sublist in self.roboard)
    
    def fill_path(self, board):
        while self.check_for_ast() and not self.is_found:
            self.find_path(board)
            self.move()
                        
    def printRoboard(self, roboard):
        self.roboard = roboard
        rows = len(roboard)
        col = len(roboard[0])
        
        for i in range(rows):
            for c in range(col):
                print(self.roboard[i][c], end = "")
            print()
    
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

        
    
    
        
def main():
    board = BoardLoader.from_file("boards/file.txt")
    robot = Robot(board.start, board.goal)
    
    robot.printRoboard(robot.roboard)

if __name__ == "__main__":
    main()
