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

    def get_gamemode(self):
        return pm.read_int(get_pointer_address(self.base_address + 0x3EAC48, [0x728]))

    def is_stage_start(self):
        return 1 == pm.read_int(get_pointer_address(self.base_address + 0x125FC68, [0x08]))

    def is_stage_finish(self):
        pass

    def get_car_speed(self):
        pass

    def get_drive_distance(self):
        return 5

    def get_car_direction(self):
        pass

if __name__ == '__main__':
    print(1)
    game = RBRGame()
    print(game.get_drive_distance())
    print(game.get_gamemode())
    print('game start' + game.is_stage_start())