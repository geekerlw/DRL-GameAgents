import pygame
import numpy as np
import utils
import ctypes
import threading
from driveline import DriveLine
from game import RBRGame

TRACK_COLOR = (50, 150, 50)  # 赛道颜色
BOUNDARY_COLOR = (0, 0, 0)   # 赛道边界颜色
WHITE = (255, 255, 255) # 赛道背景颜色
BACKGROUD_COLOR = (102, 102, 102)
SCREEN_SIZE = (480, 480)

class TrackMonitor(threading.Thread):
    def __init__(self, game: RBRGame, driveline: DriveLine):
        super().__init__()
        self.game = game
        self.driveline = driveline
        self.running = True
        self.fixed_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]-20)
        self.track_background = []
        self.update_region = True
        self.start()

    def stop(self):
        self.running = False

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowPos(hwnd, None, 650, 0, SCREEN_SIZE[0], SCREEN_SIZE[1], 0)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            left, right= self.update_track()
            car = self.update_car()

            # 填充背景
            screen.fill(WHITE)
            for point in self.track_background:
                pygame.draw.circle(screen, BACKGROUD_COLOR, point, 24)

            # 绘制赛道中间部分
            pygame.draw.polygon(screen, TRACK_COLOR, left + right[::-1])

            # 绘制赛道边界
            pygame.draw.lines(screen, BOUNDARY_COLOR, False, left, 5)
            pygame.draw.lines(screen, BOUNDARY_COLOR, False, right, 5)

            # 绘制车辆（简单地用一个矩形表示，车辆中心位置）
            pygame.draw.rect(screen, (255, 0, 0), (car[0] - 8, car[1] - 12, 16, 24))

            # 更新显示
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

    def update_track(self):
        if self.update_region:
            self.track_background.clear()
            for i in range(32):
                self.track_background.append((np.random.randint(0, SCREEN_SIZE[0]), np.random.randint(0, SCREEN_SIZE[0])))

            drive_distance = self.game.drive_distance()
            left, right, center = self.driveline.nearby(drive_distance, 10, 120)
            start = (center[0][0], center[0][1])
            direction = (center[0][3], center[0][4])

            rotation = np.degrees(np.arctan2(-1, 0) - np.arctan2(direction[1], direction[0]))
            translation = (self.fixed_pos[0] - start[0], self.fixed_pos[1] - start[1])
            matrix = utils.create_transform_matrix(start, rotation, translation, scale=5.0)
            self.left = utils.calculate_transform_points(left, matrix)
            self.right = utils.calculate_transform_points(right, matrix)
            self.matrix = matrix
            self.update_region = False

        return self.left, self.right

    def update_car(self):
        car_pos = self.game.car_pos()[0:2]
        car = utils.calculate_transform_point(car_pos, self.matrix)

        (x, y) = car

        if x < 0 or x > SCREEN_SIZE[0] or y < 80 or y > SCREEN_SIZE[1]+40:
            self.update_region = True

        return car
    

if __name__ == '__main__':
    rbr = RBRGame()
    driveline = DriveLine()
    rbr.attach()
    driveline.load(318)

    track = TrackMonitor(rbr, driveline)
    track.join()