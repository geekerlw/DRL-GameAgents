import pygame
import numpy as np
import utils
from driveline import DriveLine

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen_width, screen_height = 512, 512
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
TRACK_COLOR = (50, 150, 50)  # 赛道颜色
BOUNDARY_COLOR = (0, 0, 0)   # 赛道边界颜色
WHITE = (255, 255, 255)
SCALE = 5

# 定义车辆的初始位置（底部居中）
car_x, car_y = screen_width // 2, screen_height - 30  # 底部居中
car_pos = (103, -61)

driveline = DriveLine()
driveline.load(318)

# select nearby points
left, right, center = driveline.nearby(50)
left = [(point[0] * SCALE, point[1] * SCALE) for point in left]
right = [(point[0] * SCALE, point[1] * SCALE) for point in right]

# rotate and translation
rotation = np.degrees(np.arctan2(1, 0) - np.arctan2(center[0][4], center[0][3]))
translation = (car_x - car_pos[0], car_y - car_pos[1])
matrix = utils.create_transform_matrix(rotation, translation)
print(translation)
print(matrix)
left = utils.calculate_transform_points(left, matrix)
right = utils.calculate_transform_points(right, matrix)
car = utils.calculate_transform_point(car_pos, matrix)

print(car)

# convert to pygame's coordinate
track_left = [(point[0], point[1]) for point in left]
track_right = [(point[0], point[1]) for point in right]

print(track_left)

# track_left = [(car_x - 25, screen_height), (car_x - 50, 300), (car_x + 50, 200), (car_x - 25, 100)]  # 左边界
# track_right = [(car_x + 25, screen_height), (car_x + 0, 300), (car_x + 100, 200), (car_x + 25, 100)]  # 右边界

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill(WHITE)

    # 绘制赛道中间部分
    pygame.draw.polygon(screen, TRACK_COLOR, track_left + track_right[::-1])

    # 绘制赛道边界
    pygame.draw.lines(screen, BOUNDARY_COLOR, False, track_left, 5)
    pygame.draw.lines(screen, BOUNDARY_COLOR, False, track_right, 5)

    # 绘制车辆（简单地用一个矩形表示，车辆中心位置）
    pygame.draw.rect(screen, (255, 0, 0), (car_x - 15, screen_height - 50, 30, 20))

    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()