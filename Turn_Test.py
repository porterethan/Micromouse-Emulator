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

DONE = False

while not DONE:
    toggle.update()
    select.update()

    if toggle.fell:
        for i in range(10):
            start = time.monotonic()
            robot.turnLeft()
            end = time.monotonic()
            total_time = end - start
            print(f"\nRun {i} of 5: {total_time}")
        print("\n >>> Complete <<<")

    if select.fell:
        quit
