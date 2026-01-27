from emulator import *

def menu():
    
    board_files = {
        1: "boards/easy1.txt",
        2: "boards/medium1.txt",
        3: "boards/hard1.txt"
    }
    
    
    driver_classes = {
        2: RightHandDriver,
        3: LeftHandDriver,
        4: RandomDriver  
    }
    
    board_names = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "ALL"}
    driver_names = {1: "ALL DRIVERS", 2: "RIGHT HAND DRIVER", 3: "LEFT HAND DRIVER", 4: "RANDOM DRIVER"}
    
    while True:
        print("\n" + "="*40)
        print("Micromouse Emulator")
        print("="*40)
        print("\nSELECT BOARD:")
        print("[1] EASY")
        print("[2] MEDIUM")
        print("[3] HARD")
        print("[4] ALL")
        
        try:
            board_choice = int(input("\n>>> "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if board_choice not in [1, 2, 3, 4]:
            print("Invalid choice! Please select 1-4.")
            continue
        
        print("\n" + "="*40)
        print("SELECT DRIVER:")
        print("[1] ALL DRIVERS")
        print("[2] RIGHT HAND DRIVER")
        print("[3] LEFT HAND DRIVER")
        print("[4] RANDOM DRIVER")
        print("="*40)
        
        try:
            driver_choice = int(input("\n>>> "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if driver_choice not in [1, 2, 3, 4]:
            print("Invalid choice! Please select 1-4.")
            continue
        
        print(f"\n🐭 Running simulation with {board_names[board_choice]} board and {driver_names[driver_choice]}...")
        print("="*40 + "\n")
        
        if board_choice == 4:  
            if driver_choice == 1:  
                for board_num in [1, 2, 3]:
                    for driver_num in [2, 3, 4]:
                        run_simulation(board_files[board_num], driver_classes[driver_num], 
                                     board_names[board_num], driver_names[driver_num])
            else:  
                for board_num in [1, 2, 3]:
                    run_simulation(board_files[board_num], driver_classes[driver_choice],
                                 board_names[board_num], driver_names[driver_choice])
        else: 
            if driver_choice == 1:  
                for driver_num in [2, 3, 4]:
                    run_simulation(board_files[board_choice], driver_classes[driver_num],
                                 board_names[board_choice], driver_names[driver_num])
            else: 
                run_simulation(board_files[board_choice], driver_classes[driver_choice],
                             board_names[board_choice], driver_names[driver_choice])
        
        print("\n" + "="*40)
        print("Complete!")
        print("="*40 + "\n")
        
        # Ask if user wants to continue
        again = input("Run another simulation? (y/n): ").lower()
        if again != 'y':
            print("\nExiting Micromouse Emulator. Goodbye! 🐭")
            break



if __name__ == "__main__":
    menu()