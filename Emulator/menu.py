from emulator import *
from Robot import *                          
from Exploration_Emulated import ExplorationRobot, ExplorationDriver


def run_simulation(board_path, driver_class, board_name, driver_name,
                   use_exploration_robot=False):
    print(f"\nRunning {driver_name} on {board_name}  —  {board_path}")
    print("-" * 50)

    board = BoardLoader.from_file(board_path)
    rows  = len(board.grid)
    cols  = len(board.grid[0])

    if use_exploration_robot:
        robot = ExplorationRobot(board.start, board.goal, (rows, cols))
    else:
        robot = Robot(board.start, board.goal, (rows, cols))

    driver   = driver_class()
    emu    = Emulator(board, robot, driver)
    result = emu.run()

    print(result)
    Result(robot).statusReport()

    # Show the discovered map after an exploration run
    if use_exploration_robot:
        print("\n── Discovered Maze Map ──")
        robot.print_discovered_maze()


def menu():
    board_files = {
        1: {"easy1.txt":   "Easy Board 1",
            "easy2.txt":   "Easy Board 2",
            "easy3.txt":   "Easy Board 3"},
        2: {"medium1.txt": "Medium Board 1",
            "medium2.txt": "Medium Board 2",
            "medium3.txt": "Medium Board 3"},
        3: {"hard1.txt":   "Hard Board 1",
            "hard2.txt":   "Hard Board 2"},
    }

    driver_classes = {
        2: RightHandDriver,
        3: LeftHandDriver,
        4: RandomDriver,
        5: AStarDriver,
        6: ExplorationDriver,   # ← NEW
    }

    # Drivers that need ExplorationRobot instead of Robot
    exploration_drivers = {6}

    board_names = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "ALL"}

    driver_names = {
        1: "ALL DRIVERS",
        2: "RIGHT HAND DRIVER",
        3: "LEFT HAND DRIVER",
        4: "RANDOM DRIVER",
        5: "A* DRIVER",
        6: "EXPLORATION (DFS) DRIVER",   # ← NEW
    }

    while True:
        print("\n" + "=" * 40)
        print("       Micromouse Emulator")
        print("=" * 40)
        print("\nSELECT BOARD:")
        print("  [1] EASY")
        print("  [2] MEDIUM")
        print("  [3] HARD")
        print("  [4] ALL")
        print("  [0] EXIT")

        try:
            board_choice = int(input("\n>>> "))
        except ValueError:
            continue

        if board_choice == 0:
            break
        if board_choice not in [1, 2, 3, 4]:
            continue

        # ── board selection ──────────────────────────────────────────
        selected_boards = []

        if board_choice in [1, 2, 3]:
            board_options = list(board_files[board_choice].items())
            print()
            for i, (_, name) in enumerate(board_options, 1):
                print(f"  [{i}] {name}")
            print("  [0] BACK")

            try:
                lvl_choice = int(input(">>> "))
            except ValueError:
                continue

            if lvl_choice == 0:
                continue
            if lvl_choice not in range(1, len(board_options) + 1):
                continue

            selected_file   = board_options[lvl_choice - 1][0]
            selected_boards = [f"boards/{selected_file}"]
        else:
            for difficulty in [1, 2, 3]:
                for filename in board_files[difficulty]:
                    selected_boards.append(f"boards/{filename}")

        # ── driver selection ─────────────────────────────────────────
        print("\nSELECT DRIVER:")
        print("  [1] ALL DRIVERS")
        print("  [2] RIGHT HAND DRIVER")
        print("  [3] LEFT HAND DRIVER")
        print("  [4] RANDOM DRIVER")
        print("  [5] A* DRIVER")
        print("  [6] EXPLORATION (DFS) DRIVER")
        print("  [0] BACK")

        try:
            driver_choice = int(input("\n>>> "))
        except ValueError:
            continue

        if driver_choice == 0:
            continue
        if driver_choice not in [1, 2, 3, 4, 5, 6]:
            continue

        time.sleep(1)

        driver_nums = list(driver_classes.keys()) if driver_choice == 1 else [driver_choice]

        try:
            for board_path in selected_boards:
                for driver_num in driver_nums:
                    run_simulation(
                        board_path,
                        driver_classes[driver_num],
                        board_names.get(board_choice, "?"),
                        driver_names[driver_num],
                        use_exploration_robot=(driver_num in exploration_drivers),
                    )
        except Exception as e:
            print(f"\nError: {e}")
            continue

        again = input("\nRun another simulation? (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting.")