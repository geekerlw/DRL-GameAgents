import time
import vgamepad as vg
import numpy as np

class Action:
    def __init__(self, continuous=True):
        self.gamepad = vg.VX360Gamepad()
        self.continuous = continuous
        self.actions = [self.none, self.steer_left, self.steer_center, self.steer_right, 
                        self.throttle_full,self.brake_full, self.handbrake, self.reset]

    def dimentions(self):
        if self.continuous:
            return 2
        else:
            return len(self.actions)

    def continuous_action(self, actions):
        self.reset()
        self.steer(actions[0])
        if actions[1] >= 0:
            self.throttle(actions[1])
        else:
            self.brake(-actions[1])

    def discrete_action(self, actions):
        self.actions[actions]()

    # actions will inside [-1.0, 1.0], expand by yourself.
    def execute(self, actions):
        if self.continuous:
            self.continuous_action(actions)
        else:
            self.discrete_action(actions)

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

    def none(self):
        pass

    def steer_left(self):
        self.steer(-1.0)

    def steer_center(self):
        self.steer(0)

    def steer_right(self):
        self.steer(1.0)

    def throttle_full(self):
        self.throttle(1.0)
    
    def brake_full(self):
        self.brake(0.75)