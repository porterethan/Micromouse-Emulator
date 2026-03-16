import robot
import time

class Forward_Test:

    def __init__(self, romi):
        self.romi = romi

    def run(self):
        print("Running Turn Test...\n")
        for i in range(5):
            start = time.monotonic()
            robot.turnRight(self.romi)
            end = time.monotonic()
            total_time = end - start
            print(f"Run {i+1} of 5: {total_time:.3f} seconds")
            time.sleep(1)
        print("\n>>> Forward Test Complete <<<")