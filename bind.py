import time
import numpy as np
from action import Action

if __name__ == '__main__':
    action = Action()

    while True:
        print("start steer bind")
        for i in range(20):
            action.steer(np.random.randint(-30000, 30000))
            time.sleep(0.2)

        action.reset()

        print("start throttle bind")
        for i in range(20):
            action.throttle(np.random.randint(0, 255))
            time.sleep(0.3)

        action.reset()

        print("start handbrake bind")
        for i in range(5):
            action.handbrake()
            time.sleep(1)

        action.reset()

        print("start up gear bind")
        for i in range(5):
            action.upgear()
            time.sleep(1)

        action.reset()

        print("start down gear bind")
        for i in range(5):
            action.downgear()
            time.sleep(1)

        action.reset()

        print("free to set other keys")
        time.sleep(20)

        action.reset()