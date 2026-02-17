from Emulator import *
import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    frontier = []
    heapq.heappush(frontier, (0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return list(reversed(path))

        r, c = current

        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != 1:
                    new_cost = cost_so_far[current] + 1
                    if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                        cost_so_far[(nr, nc)] = new_cost
                        priority = new_cost + heuristic((nr, nc), goal)
                        heapq.heappush(frontier, (priority, (nr, nc)))
                        came_from[(nr, nc)] = current

    return None


class Robot:
    DIR = ["N", "E", "S", "W"]
    DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    def __init__(self, start_pos, goal_pos, board_size):
        self.curr_pos = start_pos
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.direction = "N"
        self.steps = 0

        self.command_string = ""
        self.command_index = 0
        self.board_size = board_size

    def generate_path(self, board):
        path = astar(board.grid, self.start_pos, self.goal_pos)
        if not path:
            return ""

        commands = []
        direction = self.direction

        for i in range(len(path) - 1):
            dr = path[i + 1][0] - path[i][0]
            dc = path[i + 1][1] - path[i][1]

            for d, delta in self.DELTA.items():
                if delta == (dr, dc):
                    needed = d
                    break

            while direction != needed:
                ci = self.DIR.index(direction)
                ni = self.DIR.index(needed)

                if (ni - ci) % 4 <= (ci - ni) % 4:
                    commands.append("R")
                    direction = self.DIR[(ci + 1) % 4]
                else:
                    commands.append("L")
                    direction = self.DIR[(ci - 1) % 4]

            commands.append("F")

        return "".join(commands)

    def execute_next(self, board):
        if not self.command_string:
            self.command_string = self.generate_path(board)
            self.command_index = 0

        if self.command_index >= len(self.command_string):
            return

        cmd = self.command_string[self.command_index]
        self.command_index += 1

        if cmd == "F":
            self.move_forward(board)
        elif cmd == "R":
            self.turn_right()
        elif cmd == "L":
            self.turn_left()

    def _get_next_pos(self, direction):
        dr, dc = self.DELTA[direction]
        r, c = self.curr_pos
        return r + dr, c + dc

    def move_forward(self, board):
        next_pos = self._get_next_pos(self.direction)
        if not board.is_wall(next_pos):
            self.curr_pos = next_pos
            self.steps += 1

    def turn_right(self):
        i = self.DIR.index(self.direction)
        self.direction = self.DIR[(i + 1) % 4]

    def turn_left(self):
        i = self.DIR.index(self.direction)
        self.direction = self.DIR[(i - 1) % 4]

    def can_move_forward(self, board):
        return not board.is_wall(self._get_next_pos(self.direction))

    def can_move_right(self, board):
        i = (self.DIR.index(self.direction) + 1) % 4
        return not board.is_wall(self._get_next_pos(self.DIR[i]))

    def can_move_left(self, board):
        i = (self.DIR.index(self.direction) - 1) % 4
        return not board.is_wall(self._get_next_pos(self.DIR[i]))


class AStarDriver:
    def step(self, robot, board):
        robot.execute_next(board)
        
    
def main():
    board = BoardLoader.from_file("boards/file.txt")
    rows = len(board.grid)
    cols = len(board.grid[0])

    robot = Robot(board.start, board.goal, (rows, cols))
    driver = AStarDriver()

    emulator = Emulator(board, robot, driver)
    result = emulator.run()

    print(result)
    Result(robot).statusReport()


if __name__ == "__main__":
    main()
