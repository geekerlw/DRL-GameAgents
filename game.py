import pymem
from pymem.ptypes import RemotePointer

pm = pymem.Pymem("RichardBurnsRally_SSE.exe")

def get_pointer_address(base, offsets):
    remote_pointer = RemotePointer(pm.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset

class RBRGame:
    def __init__(self):
        self.base_address = pm.base_address

    def gamemode(self):
        return pm.read_int(get_pointer_address(self.base_address + 0x3EAC48, [0x728]))

    def loadmode(self):
        return pm.read_int(get_pointer_address(self.base_address + 0x3EA678, [0x70, 0x10]))

    def startcount(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x244]))

    def is_stage_loaded(self):
        return self.gamemode() == 0x0A and self.loadmode() == 0x08 and self.startcount() <= float(7.0)

    def is_stage_start(self):
        return self.gamemode() == 0x01 and self.startcount() < float(0.0)

    def is_stage_finish(self):
        return self.gamemode() == 0x09 or self.gamemode() == 0x0C

    def car_speed(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x0C]))
    
    def car_rpm(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x10]))

    def car_temp(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x14]))

    def car_turbo(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x18]))

    def drive_distance(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x20]))
    
    def left_distance(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x28]))

    def race_time(self):
        return pm.read_float(get_pointer_address(self.base_address + 0x125FC68, [0x140]))
    
    def race_wrongway(self):
        return 1 == pm.read_int(get_pointer_address(self.base_address + 0x125FC68, [0x150]))
    
    def car_look(self):
        x = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x100]))
        y = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x104]))
        z = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x108]))
        w = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x10C]))
        return [x, y, z, w]

    def car_pos(self):
        x = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x140]))
        y = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x144]))
        z = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x148]))
        w = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x14C]))
        return [x, y, z, w]

    def car_spin(self):
        x = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x190]))
        y = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x194]))
        z = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x198]))
        return [x, y, z]

    def car_acc(self):
        x = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x1C0]))
        y = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x1C4]))
        z = pm.read_float(get_pointer_address(self.base_address + 0x4EF660, [0x1C8]))
        return [x, y, z]