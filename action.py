import time
import vgamepad as vg
import numpy as np

class Action:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
    
    def dimentions(self):
        return 6

    def take(self, vec):
        self.steer(vec[0])
        self.throttle(vec[1])
        self.brake(vec[2])
        self.handbrake(vec[3])
        self.upgear(vec[4])
        self.downgear(vec[5])

    def steer(self, value): # values between -32768 and 32767
        self.gamepad.left_joystick(x_value=value, y_value=0)
        self.gamepad.update()

    def throttle(self, v): # value between 0 and 255
        self.gamepad.right_trigger(value=v)
        self.gamepad.update()

    def brake(self, v): # value between 0 and 255
        self.gamepad.left_trigger(value=v)
        self.gamepad.update()

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

    def retire(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        self.gamepad.update()

    def restart(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()