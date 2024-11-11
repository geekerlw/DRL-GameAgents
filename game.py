import pymem
from pymem.ptypes import RemotePointer
class RBRGame:
    def __init__(self):
        self.pm = None
        self.base_address = 0

    def attach(self):
        self.pm = pymem.Pymem("RichardBurnsRally_SSE.exe")
        self.base_address = self.pm.base_address

    def address(self, base, offsets):
        remote_pointer = RemotePointer(self.pm.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(self.pm.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset

    def launch(self):
        # spawn a game.
        pass
    
    def start(self):
        # start race, press esc to start
        pass

    def restart(self):
        # restart race by onekey map
        pass

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

    def overfinish(self):
        return 1 == self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x2C4]))

    def car_speed(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x0C]))
    
    def car_rpm(self):
        return self.pm.read_float(self.address(self.base_address + 0x125FC68, [0x10]))

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