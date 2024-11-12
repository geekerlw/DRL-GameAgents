import time
import vgamepad as vg
import numpy as np

class Action:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
    
    def dimentions(self):
        return 6

    # actions will inside [-1.0, 1.0], expand by yourself.
    def execute(self, actions):
        self.steer(actions[0])
        self.throttle((actions[1] + 1.0) / 2)
        self.brake((actions[2] + 1.0) / 2)
        self.handbrake(actions[3] > 0)
        self.upgear(actions[4] > 0)
        self.downgear(actions[5] > 0)

    def steer(self, weight): # weight is float between -1.0 and 1.0
        self.gamepad.left_joystick_float(x_value=weight, y_value=0)
        self.gamepad.update()

    def throttle(self, weight): # weight is float between 0.0 and 1.0
        self.gamepad.right_trigger_float(value=weight)
        self.gamepad.update()

    def brake(self, weight): # weight is float between 0.0 and 1.0
        self.gamepad.left_trigger_float(value=weight)
        self.gamepad.update()

    def handbrake(self, press=True):
        if press :
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            self.gamepad.update()
            time.sleep(0.2)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            self.gamepad.update()

    def upgear(self, press=True):
        if press:
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            self.gamepad.update()

    def downgear(self, press=True):
        if press:
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()