import ctypes
import ctypes.wintypes
import time
import win32gui
import win32con
import win32api
import pymem
from pymem.ptypes import RemotePointer

class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ("dwData", ctypes.wintypes.ULONG),  # Custom data identifier
        ("cbData", ctypes.wintypes.DWORD),  # Size of the data
        ("lpData", ctypes.wintypes.LPVOID)   # Pointer to the data
    ]

class RBRGame:
    def __init__(self):
        self.pm = None
        self.base_address = 0
        self.pacenotes = []

    def attach(self):
        if self.pm != None:
            return True

        try:
            self.pm = pymem.Pymem("RichardBurnsRally_SSE.exe")
            self.base_address = self.pm.base_address
            return True
        except Exception as e:
            print(f"attach process error: {e}")
            return False

    def address(self, base, offsets):
        remote_pointer = RemotePointer(self.pm.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(self.pm.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset
    
    def sendmessage(self, message, wparam, lparam):
        hwnd = win32gui.FindWindow(None, "Richard Burns Rally - DirectX9\0")
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SendMessage(hwnd, message, wparam, lparam)

    def restart(self):
        cds = COPYDATASTRUCT()
        cds.dwData = 3  # RSF Quick Restart Stage
        cds.cbData = 0  # Size of the data
        cds.lpData = ctypes.c_void_p(None)  # Cast to void pointer
        self.sendmessage(win32con.WM_COPYDATA, 0xDEAF01, ctypes.byref(cds))

    def gamemode(self):
        return self.pm.read_int(self.address(self.base_address + 0x3EAC48, [0x728]))

    def loadmode(self):
        return self.pm.read_int(self.address(self.base_address + 0x3EA678, [0x70, 0x10]))

    def startcount(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x244]))

    def is_stage_loaded(self):
        return self.gamemode() == 0x0A and self.loadmode() == 0x08 and self.startcount() >= float(6.0)

    def is_stage_started(self):
        return self.gamemode() == 0x01 and self.startcount() < float(0.0)

    def oversplitone(self):
        return 1 == self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x254]))

    def overfinish(self):
        return 1 == self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x2C4]))

    def car_speed(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x0C]))
    
    def car_rpm(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x10]))

    def car_gear(self):
        return self.pm.read_int(self.address(self.base_address + 0x4EF660, [0x1100]))

    def car_temp(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x14]))

    def car_turbo(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x18]))

    def drive_distance(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x20]))
    
    def left_distance(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x28]))

    def race_time(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x140]))
    
    def race_failstart(self):
        return 1 == self.pm.read_int(self.address(self.base_address + 0x125FC68, [0x248]))

    def race_wrongway(self):
        return 1 == self.pm.read_int(self.address(self.base_address + 0x125FC68, [0x150]))
    
    def car_look(self):
        x = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x100]))
        y = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x104]))
        z = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x108]))
        w = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x10C]))
        return [x, y, z, w]

    def car_pos(self):
        x = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x140]))
        y = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x144]))
        z = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x148]))
        w = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x14C]))
        return [x, y, z, w]

    def car_spin(self):
        x = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x190]))
        y = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x194]))
        z = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x198]))
        return [x, y, z]

    def car_acc(self):
        x = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x1C0]))
        y = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x1C4]))
        z = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x1C8]))
        return [x, y, z]

    def car_control(self):
        throttle = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x85C]))
        brake = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x860]))
        handbrake = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x864]))
        steer = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x868]))
        clutch = self.pm.read_float(self.address(self.base_address + 0x4EF660, [0x86C]))
        return [throttle, brake, handbrake, steer, clutch]
    
    def pacenote(self):
        if len(self.pacenotes):
            pacenote = self.pacenotes[0]
            return [float(pacenote['type']), float(pacenote['distance'] - self.drive_distance())]
        return [0.0, 0.0]
    
    def load_pacenotes(self):
        self.pacenotes.clear()
        numpacenotes = self.pm.read_int(self.address(self.base_address + 0x3EABA8, [0x10, 0x20]))
        addrpacenote = self.pm.read_int(self.address(self.base_address + 0x3EABA8, [0x10, 0x24]))
        for i in range(numpacenotes):
            self.pacenotes.append({
                'type': self.pm.read_int(self.address(self.base_address, [addrpacenote + 0xC * i + 0x00])),
                'distance': self.pm.read_int(self.address(self.base_address, [addrpacenote + 0xC * i + 0x08]))
            })

    def step(self):
        if len(self.pacenotes):
            if self.pacenotes[0]['distance'] < self.drive_distance():
                del self.pacenotes[0]
            