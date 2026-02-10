from emulator import Emulator
from emulator import Board
from emulator import BoardLoader
from emulator import RightHandDriver
from emulator import LeftHandDriver
from emulator import Result
import time
import heapq

# -- A* pathfinding adapted from Main copy.py --

def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(roboard, start, goal):
    """A* pathfinding through known-open cells on the robot's internal map.

    Navigates through cells that are known passable (not walls or unknown).
    Returns the path as a list of (row, col) tuples, or None if unreachable.
    """
    rows = len(roboard)
    cols = len(roboard[0])

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            return list(reversed(path))

        r, c = current
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = roboard[nr][nc]
                if cell != 1 and cell != '*':
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

    def __init__(self, start_pos=(0,0), goal_pos=(1,1), board_size=[10,10]):
        self.curr_pos = start_pos
        self.goal_pos = goal_pos
        self.start_pos = start_pos
        self.direction = "N"
        self.is_found = False
        self.steps = 0
        self.board_size = board_size
        self.visited = set()
        self.visited.add(start_pos)

        rows, cols = board_size
        self.roboard = [['*' for _ in range(cols)] for _ in range(rows)]

        start_row, start_col = start_pos
        self.roboard[start_row][start_col] = "X"

    def find_path(self, board, direction):
        """Sense walls in all 4 directions from current position and update roboard."""
        for direction in self.DIR:
            dr, dc = self.DELTA[direction]
            row, col = self.curr_pos
            next_row, next_col = row + dr, col + dc

            if 0 <= next_row < len(self.roboard) and 0 <= next_col < len(self.roboard[0]):
                        if self.roboard[next_row][next_col] == "*":
                            if board.is_wall((next_row, next_col)):
                                self.roboard[next_row][next_col] = 1
                            elif board.is_goal((next_row, next_col)):
                                self.roboard[next_row][next_col] = "G"
                            else:
                                self.roboard[next_row][next_col] = 0

    def pick_nearest_unvisited(self):
        """Find the nearest reachable unvisited cell using A*.

        Iterates over all known-open unvisited cells and uses A* to find
        the one with the shortest path from the current position.
        Adapted from Main copy.py's pick_unexplored method.
        """
        best_path = None
        best_len = float('inf')

        rows = len(self.roboard)
        cols = len(self.roboard[0])

        for r in range(rows):
            for c in range(cols):
                if ((r, c) not in self.visited and
                    self.roboard[r][c] != 1 and
                    self.roboard[r][c] != '*'):
                    path = astar(self.roboard, self.curr_pos, (r, c))
                    if path and len(path) < best_len:
                        best_path = path
                        best_len = len(path)

        return best_path

    def path_to_commands(self, path):
        """Convert a list of (row, col) positions to an F/L/R command string.

        Uses the robot's initial direction. For each step in the path,
        generates turn commands (L/R) to face the next cell, then F to move.
        """
        commands = []
        direction = self.direction  # Initial facing direction

        for i in range(len(path) - 1):
            curr = path[i]
            next_pos = path[i + 1]

            dr = next_pos[0] - curr[0]
            dc = next_pos[1] - curr[1]

            # Find the direction we need to face
            needed_dir = None
            for d, (delta_r, delta_c) in self.DELTA.items():
                if (delta_r, delta_c) == (dr, dc):
                    needed_dir = d
                    break

            # Turn to face the needed direction (shortest rotation)
            while direction != needed_dir:
                curr_idx = self.DIR.index(direction)
                needed_idx = self.DIR.index(needed_dir)
                right_dist = (needed_idx - curr_idx) % 4
                left_dist = (curr_idx - needed_idx) % 4

                if right_dist <= left_dist:
                    commands.append('R')
                    direction = self.DIR[(curr_idx + 1) % 4]
                else:
                    commands.append('L')
                    direction = self.DIR[(curr_idx - 1) % 4]

            commands.append('F')

        return ''.join(commands)

    def fill_path(self, board):
        """Explore the entire maze, then find the optimal path to the goal.

        Phase 1 - Exploration:
            Visits every reachable cell using A* to navigate between
            unexplored areas. Notes the goal when discovered but does
            not stop until the entire reachable maze is mapped.

        Phase 2 - Optimal path:
            After full exploration, uses A* on the complete map to find
            the shortest path from start to goal. Outputs the path as
            a string of F (forward), L (left turn), R (right turn).
        """
        last_print = time.time()
        print("\nStatus:")
        print("Running...")

        # Phase 1: Explore entire reachable maze
        while True:
            now = time.time()
            if now - last_print >= 3:
                print("Running...")
                last_print = now

            # Sense walls at current position
            self.find_path(board, self.DIR)

            # Use A* to find nearest unvisited known-open cell
            path = self.pick_nearest_unvisited()

            if path is None:
                break  # All reachable cells explored

            # Navigate along the A* path, sensing at each step
            for pos in path[1:]:
                row, col = self.curr_pos
                self.roboard[row][col] = 0

                self.curr_pos = pos
                self.visited.add(pos)
                self.steps += 1

                # Preserve "G" marker on roboard
                if self.roboard[pos[0]][pos[1]] == "G":
                    self.is_found = True
                else:
                    self.roboard[pos[0]][pos[1]] = "X"

                # Sense walls at new position
                self.find_path(board, self.DIR)

        # Clean up current position marker
        row, col = self.curr_pos
        self.roboard[row][col] = 0

        print(f"Exploration complete after {self.steps} steps. Visited {len(self.visited)} cells.")

        # Phase 2: Optimal path from start to goal
        if self.is_found:
            optimal_path = astar(self.roboard, self.start_pos, self.goal_pos)

            if optimal_path:
                commands = self.path_to_commands(optimal_path)
                print(f"\nOptimal path ({len(optimal_path) - 1} moves): {commands}")
            else:
                print("\nNo path from start to goal exists.")
        else:
            print("\nGoal was not discovered during exploration.")

    def printRoboard(self):
        for r in range(len(self.roboard)):
            for c in range(len(self.roboard[0])):
                if (r, c) == self.start_pos:
                    print("S", end="")
                elif (r, c) == self.goal_pos:
                    print("G", end="")
                else:
                    print (self.roboard[r][c], end="")
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
    # Load the board
    board = BoardLoader.from_file("boards/easy1.txt")

    rows = len(board.grid)
    cols = len(board.grid[0]) if board.grid else 0

    robot = Robot(board.start, board.goal, [rows, cols])

    print("Initial board:")
    robot.printRoboard()

    robot.fill_path(board)

    print("\nFinal explored board:")
    robot.printRoboard()

    return robot.start_pos, robot.goal_pos, robot.roboard


if __name__ == "__main__":
    main()