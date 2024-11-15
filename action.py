import time
import vgamepad as vg
import numpy as np

class Action:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
    
    def dimentions(self):
        return 3

    # actions will inside [-1.0, 1.0], expand by yourself.
    def execute(self, actions):
        reward = 0
        self.steer(actions[0])
        if actions[0] < -0.2 and actions[0] > 0.2:
            reward -= 1
        else:
            reward += 1
        if actions[1] >= 0.5:
            self.throttle((actions[1] + 1.0) / 2)
            reward += 2
        elif actions[1] < -0.9:
            self.handbrake()
            reward -= 1
        elif actions[1] < -0.5:
            self.brake((actions[1] + 1.0) / 2)
            reward -= 1
        else:
            reward += 1
    
        if actions[2] >= 0.9:
            self.upgear()
            reward -= 1
        elif actions[2] <= -0.9:
            self.downgear()
            reward -= 1
        else:
            reward += 1

        return reward

    def steer(self, weight): # weight is float between -1.0 and 1.0
        self.gamepad.left_joystick_float(x_value_float=weight, y_value_float=0)
        self.gamepad.update()
        return weight < -0.5 or weight > 0.5

    def throttle(self, weight): # weight is float between 0.0 and 1.0
        self.gamepad.right_trigger_float(value_float=weight)
        self.gamepad.update()
        return weight > 0.5

    def brake(self, weight): # weight is float between 0.0 and 1.0
        self.gamepad.left_trigger_float(value_float=weight)
        self.gamepad.update()
        return weight > 0.5

    def handbrake(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(0.2)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

    def upgear(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gamepad.update()

    def downgear(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()

    def back(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()

    def start(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()