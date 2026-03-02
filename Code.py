from romi import Romi
import board
import digitalio
from adafruit_debouncer import Debouncer
import robot
import time

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

current_mode = 1

def print_menu(selected):
    print("\033[2J\033[H")
    print("\n=== ROMI MENU ===")
    print("> [1] Exploration" if selected == 1 else "  [1] Exploration")
    print("> [2] Mapping" if selected == 2 else "  [2] Mapping")
    print("Press SELECT to confirm")

print_menu(current_mode)

selected_mode = None

while selected_mode is None:
    toggle.update()
    select.update()

    if toggle.fell:
        current_mode = 2 if current_mode == 1 else 1
        print_menu(current_mode)

    if select.fell:
        selected_mode = current_mode
        print("\nMode", selected_mode, "selected!")

if selected_mode == 1:
    print("Starting Exploration mode...")
    final_board = robot.explore_full_board(romi)
    robot.print_board(final_board)

elif selected_mode == 2:
    print("Starting Mapping mode...")
    pass

while True:
    time.sleep(1)

