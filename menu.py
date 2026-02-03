from emulator import *

def menu():
    
    board_files = {
        1: {"easy1.txt": "Easy Board 1", "easy2.txt": "Easy Board 2", "easy3.txt": "Easy Board 3"},
        2: {"medium1.txt": "Medium Board 1", "medium2.txt": "Medium Board 2", "medium3.txt": "Medium Board 3"},
        3: {"hard1.txt": "Hard Board 1", "hard2.txt": "Hard Board 2"}
    }
    
    driver_classes = {
        2: RightHandDriver,
        3: LeftHandDriver,
        4: RandomDriver  
    }
    
    board_names = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "ALL"}
    driver_names = {1: "ALL DRIVERS", 2: "RIGHT HAND DRIVER", 3: "LEFT HAND DRIVER", 4: "RANDOM DRIVER", 5: "FLOODFILL"}
    
    while True:
        print("\n" + "="*40)
        print("Micromouse Emulator")
        print("="*40)
        print("\nSELECT BOARD:")
        print("[1] EASY")
        print("[2] MEDIUM")
        print("[3] HARD")
        print("[4] ALL")
        print("[0] EXIT")  
        
        try:
            board_choice = int(input("\n>>> "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if board_choice == 0:
            print("\nExiting Micromouse Emulator. Goodbye! 🐭")
            break
        
        if board_choice not in [1, 2, 3, 4]:
            print("Invalid choice! Please select 0-4.")
            continue
        
        selected_boards = []
        
        if board_choice in [1, 2, 3]:
            print("\n" + "="*40)
            print(f"SELECT {board_names[board_choice]} BOARD:")
            board_options = list(board_files[board_choice].items())
            for i, (filename, name) in enumerate(board_options, 1):
                print(f"[{i}] {name}")
            print("[0] BACK")
            print("="*40)
            
            try:
                lvl_board_choice = int(input(">>> "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            
            if lvl_board_choice == 0:
                continue
            
            if lvl_board_choice not in range(1, len(board_options) + 1):
                print(f"Invalid choice! Please select 0-{len(board_options)}.")
                continue
            
            selected_file = board_options[lvl_board_choice - 1][0]
            selected_boards = [f"boards/{selected_file}"]
        else:
            selected_boards = []
            for difficulty in [1, 2, 3]:
                for filename in board_files[difficulty].keys():
                    selected_boards.append(f"boards/{filename}")
        
        print("\n" + "="*60)
        print("SELECT DRIVER:")
        print("[1] ALL DRIVERS")
        print("[2] RIGHT HAND DRIVER")
        print("[3] LEFT HAND DRIVER")
        print("[4] RANDOM DRIVER")
        print("[0] BACK")
        print("="*40)
        
        try:
            driver_choice = int(input("\n>>> "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if driver_choice == 0:
            continue
        
        if driver_choice not in [1, 2, 3, 4]:
            print("Invalid choice! Please select 0-4.")
            continue
        
        print(f"\n Running simulation with {board_names[board_choice]} board and {driver_names[driver_choice]}...")
        print("="*60 + "\n")
        time.sleep(1)
        
        driver_nums = list(driver_classes.keys()) if driver_choice == 1 else [driver_choice]
        if not board_choice == 4: 
            try:
                for board_path in selected_boards:
                    for driver_num in driver_nums:
                        run_simulation(board_path, driver_classes[driver_num], 
                                    board_names[board_choice], driver_names[driver_num])
            except Exception as e:
                print(f"\n Error during simulation: {e}")
                print("Please check that all board files exist and emulator is properly configured.")
                continue
        else: 
            try:
                for board_path in selected_boards:
                    for driver_num in driver_names:
                        run_simulation(board_path, driver_classes[driver_num], board_names[board_choice], driver_names[driver_num], live_run=True)
            except Exception as e:
                print(Exception, e)
        print("\n" + "="*40)
        print("Complete!")
        print("="*40 + "\n")
        
        again = input("Run another simulation? (y/n): ").lower()
        if again != 'y':
            print("\nExiting Micromouse Emulator. Goodbye! 🐭")
            break


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! ")
    except Exception as e:
        print(f"\n\nFatal error: {e}")