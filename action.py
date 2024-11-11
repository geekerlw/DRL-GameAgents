import time
import vgamepad as vg
import numpy as np

class Action:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
    
    def dimentions(self):
        return 6

    # actions nees to be inside [-1, 1], expand by yourself.
    def execute(self, actions):
        print(actions)
        # self.steer(actions[0])
        # self.throttle(actions[1])
        # self.brake(actions[2])
        # self.handbrake(actions[3])
        # self.upgear(actions[4])
        # self.downgear(actions[5])

        self.steer(np.random.randint(-30000, 30000))
        self.throttle(np.random.randint(0, 255))
        self.brake(np.random.randint(0, 255))
        self.handbrake(False)
        self.upgear(np.random.randint(0, 1) == 1)
        self.downgear(np.random.randint(0, 1) == 1)

    def steer(self, v): # values between -32768 and 32767
        self.gamepad.left_joystick(x_value=v, y_value=0)
        self.gamepad.update()

    def throttle(self, v): # value between 0 and 255
        self.gamepad.right_trigger(value=v)
        self.gamepad.update()

    def brake(self, v): # value between 0 and 255
        self.gamepad.left_trigger(value=v)
        self.gamepad.update()

    def handbrake(self, v=True):
        if v :
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            self.gamepad.update()
            time.sleep(0.2)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            self.gamepad.update()
        
    
    def upgear(self, v=True):
        if v:
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            self.gamepad.update()

    def downgear(self, v=True):
        if v:
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()