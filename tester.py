from emulator import *

def main():
    print("Hello World")
    board = BoardLoader.from_file("boards/medium2.txt")
    robot = Robot(board.start, board.goal)
    board.printBoard(robot)
   


if __name__ == "__main__": 
    main()
    
    