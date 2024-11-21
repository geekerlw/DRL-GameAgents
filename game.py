import time
import pymem
from pymem.ptypes import RemotePointer

class RBRGame:
    def __init__(self):
        self.pm = None
        self.base_address = 0
        self.pacenotes = []
        self.last_gear = 1 # default N
        self.last_distance = 0
        self.last_pos = [0.0, 0.0, 0.0]

    def reset(self):
        self.last_gear = 1 # default N
        self.last_distance = 0
        self.last_pos = [0.0, 0.0, 0.0]

    def attach(self):
        if self.pm != None:
            return True

        try:
            self.pm = pymem.Pymem("RichardBurnsRally_SSE.exe")
            self.base_address = self.pm.base_address
            return True
        except:
            return False

    def address(self, base, offsets):
        remote_pointer = RemotePointer(self.pm.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(self.pm.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset

    def gamemode(self):
        return self.pm.read_int(self.address(self.base_address + 0x3EAC48, [0x728]))

    def loadmode(self):
        return self.pm.read_int(self.address(self.base_address + 0x3EA678, [0x70, 0x10]))

    def startcount(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x244]))

    def is_stage_loaded(self):
        return self.gamemode() == 0x0A and self.loadmode() == 0x08 and self.startcount() == float(7.0)

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
    
    def car_gear_last(self):
        return self.pm.read_int(self.address(self.base_address + 0x4EF660, [0x10DC]))

    def car_gear(self):
        return self.pm.read_int(self.address(self.base_address + 0x4EF660, [0x1100]))

    def car_temp(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x14]))

    def car_turbo(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x18]))

    def drive_distance(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x20]))
    
    def travel_distance(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x24]))

    def left_distance(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x28]))

    def race_time(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x140]))
    
    def race_failstart(self):
        return 1 == self.pm.read_int(self.address(self.base_address + 0x125FC68, [0x248]))

    def race_wrongway(self):
        return 1 == self.pm.read_int(self.address(self.base_address + 0x125FC68, [0x150]))

    def stageid(self):
        return self.pm.read_int(self.address(self.base_address + 0x3EA678, [0x70, 0x20]))
    
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
        return [x, y, z]

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
        return [throttle, brake, handbrake, steer]
    
    def pacenote(self):
        if len(self.pacenotes):
            pacenote = self.pacenotes[0]
            return [float(pacenote['type']), float(pacenote['distance'] - self.drive_distance())]
        return [0.0, 0.0]

    def load_pacenotes(self):
        self.pacenotes.clear()
        numpacenotes = self.pm.read_int(self.address(self.base_address + 0x3EABA8, [0x10, 0x20]))
        for i in range(numpacenotes):
            self.pacenotes.append({
                'type': self.pm.read_int(self.address(self.base_address + 0x3EABA8, [0x10, 0x24, 0xC * i])),
                'distance': self.pm.read_float(self.address(self.base_address + 0x3EABA8, [0x10, 0x24, 0xC * i + 0x8]))
            })

    def step(self):
        if time.time() % 3 == 0: # update every three seconds.
            self.last_gear = self.car_gear()
            self.last_pos = self.car_pos()
            self.last_distance = self.drive_distance()
        if len(self.pacenotes):
            if (self.drive_distance() + 10.0) > self.pacenotes[0]['distance']:
                del self.pacenotes[0]
            