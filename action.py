import pyautogui

def none():
    pass

def left():
    pyautogui.keyDown('a')

def release_left():
    pyautogui.keyUp('a')

def right():
    pyautogui.keyDown('d')

def release_right():
    pyautogui.keyUp('d')

def throttle():
    pyautogui.keyDown('w')

def release_throttle():
    pyautogui.keyUp('w')

def brake():
    pyautogui.keyDown('s')

def release_brake():
    pyautogui.keyUp('s')

def handbrake():
    pyautogui.keyDown('space')

def release_handbrake():
    pyautogui.keyUp('space')

def upgear():
    pyautogui.press('u')

def downgear():
    pyautogui.press('d')

class Action:
    def __init__(self):
        self._actions = [none, left, release_left, right, release_right, 
                        throttle, release_throttle, brake, release_brake, 
                        handbrake, release_handbrake, upgear, downgear]
    
    def dimentions(self):
        return self._actions.count()

    def take(self, index):
        self._actions[index]()