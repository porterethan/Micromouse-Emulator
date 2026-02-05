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
        self.direction = "S"  
        self.is_found = False
        self.steps = 0
        self.board_size = board_size
        
        
        rows, cols = board_size
        self.roboard = [['*' for _ in range(cols)] for _ in range(rows)]
        
        start_row, start_col = start_pos
        self.roboard[start_row][start_col] = "X"
        
    def get_next_pos(self, board, direction): 
        dr, dc = self.DELTA[direction]
        row, col = self.curr_pos
        return (row+dr, col+dc)
    
    def find_path(self, board, direction): 
        for dir in self.DIR:
            dr, dc = self.DELTA[direction]
            row, col = self.curr_pos
            next_pos = [(dr+row), (dc+col)]
            next_row, next_col = next_pos
        
            if 0 <= next_row < len(self.roboard) and 0 <= next_col < len(self.roboard[0]):
                if self.roboard[next_row][next_col] == "*": 
    
    #This value will need to change in response to a real board.
    #This is where there will be an is_wall function that will
    #return a value and create the board   
                 
                    if board.is_wall(next_pos):
                        self.roboard[next_row][next_col] = 1
                    elif board.is_goal(next_pos):
                        self.roboard[next_row][next_col] = "G"
                    else:
                        self.roboard[next_row][next_col] = 0
                        
    def printRoboard(self, roboard):
        self.roboard = roboard
        rows = len(roboard)
        col = len(rows)
        
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
    
    robot.printRoboard(board)

if __name__ == "__main__":
    main()
