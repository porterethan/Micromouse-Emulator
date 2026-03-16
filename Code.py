from romi import Romi
import board
import digitalio
from adafruit_debouncer import Debouncer
import robot
import time
import Forward_Test
import Turn_Test

pin_toggle = digitalio.DigitalInOut(board.IO14)
pin_toggle.direction = digitalio.Direction.INPUT
pin_toggle.pull = digitalio.Pull.UP
toggle = Debouncer(pin_toggle)

pin_select = digitalio.DigitalInOut(board.IO0)
pin_select.direction = digitalio.Direction.INPUT
pin_select.pull = digitalio.Pull.UP
select = Debouncer(pin_select)

romi = Romi()
romi._getStatus()

forward_test = Forward_Test.Forward_Test(romi)
turn_test = Turn_Test.Turn_Test(romi)

current_mode = 1
selected_mode = None


def print_menu(selected):
    print("\033[2J\033[H")  # Clear terminal

    print("=== ROMI MENU ===\n")

    print("> [1] Exploration" if selected == 1 else "  [1] Exploration")
    print("> [2] Mapping" if selected == 2 else "  [2] Mapping")
    print("> [3] Test Forward" if selected == 3 else "  [3] Test Forward")
    print("> [4] Test Turns" if selected == 4 else "  [4] Test Turns")

    print("\nToggle = Change option")
    print("Select = Confirm")


print_menu(current_mode)

while selected_mode is None:

    toggle.update()
    select.update()

    # Toggle cycles through menu
    if toggle.fell:
        current_mode += 1
        if current_mode > 4:
            current_mode = 1

        print_menu(current_mode)

    # Select confirms choice
    if select.fell:
        selected_mode = current_mode
        print("\nMode", selected_mode, "selected!\n")

    time.sleep(0.05)
    
if selected_mode == 1:
    print("Starting Exploration mode...")
    final_board = robot.explore_full_board(romi)
    robot.print_board(final_board)

elif selected_mode == 2:
    print("Starting Mapping mode...")
    print("Mapping mode not implemented yet.")

elif selected_mode == 3:
    print("Starting Forward Test...\n")
    forward_test.run()

elif selected_mode == 4:
    print("Starting Turn Test...\n")
    turn_test.run()

while True:
    time.sleep(1)