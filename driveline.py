import os
import time
from game import RBRGame
import utils

class DriveLine:
    def __init__(self):
        self.pointnum = 0
        self.points = [] # [x, y, z, tx, ty, tz, distance, reserved]

    def reset(self):
        self.points.clear()
        self.pointnum = 0

    def load(self, stage):
        self.reset()
        filepath = os.path.join("rsfdata", f"{stage}-driveline.ini")
        with open(filepath, 'r') as file:
            lines = file.readlines()
            if not lines[0].startswith("[DRIVELINE]"):
                raise ValueError("file format error.")
            
            for line in lines:
                if line.startswith("count="):
                    self.pointnum = int(line.split("=")[1])
                elif line.startswith("K"):
                    self.points.append(list(map(float, line.split("=")[1].split(","))))
            print(f"file successfully load from: {filepath}")

    def save(self, stage):
        filepath = os.path.join("rsfdata", f"{stage}-driveline.ini")
        with open(filepath, 'w') as file:
            file.write("[DRIVELINE]\n")
            file.write(f"count={self.pointnum}\n")
            for (i, point) in enumerate(self.points):
                file.write(f"K{i}={", ".join(map(str, point))}\n")
            print(f"file successfully saved into: {filepath}")

    def record(self, x, y, z, tx, ty, tz, distance, reversed):
        self.points.append([x, y, z, tx, ty, tz, distance, reversed])
        self.pointnum += 1

    def locate_point(self, distance):
        if self.pointnum < 2:
            raise ValueError("driveline data empty, load it first.")
        
        for (i, point) in enumerate(self.points):
            if i > 0 and point[6] > distance:
                return self.points[i-1], self.points[i]

        return self.points[0], self.points[-1]   

    def outline(self, distance, pos):
        last_point, next_point = self.locate_point(distance)
        distance = utils.calculate_point_to_segment_distance(pos, last_point[:3], next_point[:3])
        return distance > 3
    
    def offset(self, distance, last_pos, curr_pos):
        if last_pos == curr_pos:
            return 0
        last_point, _ = self.locate_point(distance)
        target_direction = last_point[3:6]
        direction = utils.calculate_direction_vector(last_pos, curr_pos)
        return utils.calculate_angle_between_vectors(direction, target_direction)

if __name__ == '__main__':
    game = RBRGame()
    driveline = DriveLine()
    while not game.attach():
        print("can't attach game process, please start game.")
        time.sleep(3)

    while not game.is_stage_loaded():
        print("stage is not loaded, select a stage to start.")
        time.sleep(2)

    stageid = game.stageid()

    while not game.is_stage_started():
        time.sleep(0.2)

    last_distance = 0
    points = []
    while game.gamemode() == 0x01:
        distance_from_start = game.drive_distance()
        if distance_from_start - last_distance >= 5.0:
            pos = game.car_pos()
            points.append({
                'distance': distance_from_start,
                'pos': pos
            })
            last_distance = distance_from_start

    for i in range(len(points) - 1):
        curr = points[i]
        next = points[i+1]
        direction = utils.calculate_direction_vector(curr['pos'], next['pos'])
        driveline.record(curr['pos'][0], curr['pos'][1], curr['pos'][2], direction[0], direction[1], direction[2], curr['distance'], 0)

    driveline.save(stageid)