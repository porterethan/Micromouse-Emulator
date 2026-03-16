import os
import time

DIR   = ["N", "E", "S", "W"]
DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    
class ExplorationRobot:
    DIR   = ["N", "E", "S", "W"]
    DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    def __init__(self, start_pos, goal_pos, board_size):
        self.curr_pos   = start_pos
        self.start_pos  = start_pos
        self.goal_pos   = goal_pos
        self.board_size = board_size          
        self.direction  = 1                  
                                              
        self.steps = 0
        self.turns = 0
        self.command_string = ""              
       
       #Creates the internal board size
        rows, cols = board_size
        self.maze    = [["*"] * cols for _ in range(rows)]
        self.visited = [[False] * cols for _ in range(rows)]

        #sets the maze
        for i in range(rows):
            self.maze[i][0]      = "1"
            self.maze[i][cols-1] = "1"
        for j in range(cols):
            self.maze[0][j]      = "1"
            self.maze[rows-1][j] = "1"

        #Create stack
        self.stack = []
        self.explore_done = False

        self._gen = None

    #Check the wall with the given board on all sides
    def front_wall(self, board):
        dr, dc = self.DELTA[self.DIR[self.direction]]
        r, c   = self.curr_pos
        return board.is_wall((r + dr, c + dc))

    def left_wall(self, board):
        d = (self.direction - 1) % 4
        dr, dc = self.DELTA[self.DIR[d]]
        r, c   = self.curr_pos
        return board.is_wall((r + dr, c + dc))

    def right_wall(self, board):
        d = (self.direction + 1) % 4
        dr, dc = self.DELTA[self.DIR[d]]
        r, c   = self.curr_pos
        #Is_wall acts as the sensor
        return board.is_wall((r + dr, c + dc))

    def move_forward(self, board):
        dr, dc = self.DELTA[self.DIR[self.direction]]
        r, c   = self.curr_pos
        nr, nc = r + dr, c + dc
        if not board.is_wall((nr, nc)):
            self.curr_pos = (nr, nc)
            self.steps += 1
            
    def turn_right_action(self):
        self.direction = (self.direction + 1) % 4
        self.turns += 1

    def turn_left_action(self):
        self.direction = (self.direction - 1) % 4
        self.turns += 1

    def detect_walls(self, board):
        r, c = self.curr_pos

        if self.front_wall(board):
            dr, dc = self.DELTA[self.DIR[self.direction]]
            nr, nc = r + dr, c + dc
            rows, cols = self.board_size
            if 0 <= nr < rows and 0 <= nc < cols:
                self.maze[nr][nc] = "1"
        left_d = (self.direction - 1) % 4
        
        
        if self.left_wall(board):
            dr, dc = self.DELTA[self.DIR[left_d]]
            nr, nc = r + dr, c + dc
            rows, cols = self.board_size
            if 0 <= nr < rows and 0 <= nc < cols:
                self.maze[nr][nc] = "1"
        right_d = (self.direction + 1) % 4
        
        if self.right_wall(board):
            dr, dc = self.DELTA[self.DIR[right_d]]
            nr, nc = r + dr, c + dc
            rows, cols = self.board_size
            if 0 <= nr < rows and 0 <= nc < cols:
                self.maze[nr][nc] = "1"

    def print_discovered_maze(self):
        r, c = self.curr_pos
        gr, gc = self.goal_pos
        print()
        rows, cols = self.board_size
        for i in range(rows):
            row_str = ""
            for j in range(cols):
                if (i, j) == (r, c):
                    row_str += self.DIR[self.direction][0]   # show heading
                elif (i, j) == (gr, gc):
                    row_str += "G"
                elif self.maze[i][j] == "1":
                    row_str += "1"
                elif self.maze[i][j] == "V":
                    row_str += "·"
                else:
                    row_str += " "
            print(row_str)
        print()


class ExplorationDriver:
    def step(self, robot, board):
        if robot.explore_done:
            return
        if robot._gen is None:
            robot._gen = self._explore_gen(robot, board)

        try:
            next(robot._gen)
        except StopIteration:
            robot.explore_done = True
            robot.print_discovered_maze()


    #This is the emulated version of the exploration file. 
    def _explore_gen(self, robot, board):
        call_stack = []  

        def _mark_visited():
            r, c = robot.curr_pos
            robot.visited[r][c] = True
            robot.maze[r][c]    = "V"

        def _detect():
            robot.detect_walls(board)

        _mark_visited()
        _detect()
        call_stack.append([robot.curr_pos[0], robot.curr_pos[1], robot.direction, 0])

        #While there is still things in the stack
        while call_stack:
            frame = call_stack[-1]
            fr, fc, _, next_dir = frame
            if next_dir == 4:
                call_stack.pop()
                if not call_stack:
                    break
                parent = call_stack[-1]
                pr, pc = parent[0], parent[1]
                yield from self._turn_toward(robot, board, pr, pc)
                robot.move_forward(board)
                #Yield allows the animation time to run the code. 
                yield
                continue

            frame[3] += 1
            new_dir = next_dir

            dr, dc = DELTA[DIR[new_dir]]
            nr, nc = fr + dr, fc + dc
            rows, cols = robot.board_size

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if robot.maze[nr][nc] == "1":
                continue

            if robot.visited[nr][nc]:
                continue

            yield from self._turn_toward(robot, board, nr, nc)
            robot.move_forward(board)
            yield

            _mark_visited()
            _detect()

            call_stack.append([robot.curr_pos[0], robot.curr_pos[1],
                               robot.direction, 0])

    def _turn_toward(self, robot, board, target_r, target_c):
        # Get the robot's current position
        r, c = robot.curr_pos
        # Find how far the target cell is from the robot
        dr = target_r - r
        dc = target_c - c
        # Determine which direction the robot needs to face
        needed_dir = None
        for i in range(len(DIR)):
            direction_name = DIR[i]         
            move = DELTA[direction_name]    
            if move == (dr, dc):
                needed_dir = i
                break
       
        while robot.direction != needed_dir:
            clockwise_turns = (needed_dir - robot.direction) % 4
            counterclockwise_turns = (robot.direction - needed_dir) % 4
            if clockwise_turns <= counterclockwise_turns:
                robot.turn_right_action()
            else:
                robot.turn_left_action()
            yield