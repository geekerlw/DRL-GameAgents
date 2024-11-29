import numpy as np

def calculate_direction_vector(point_a, point_b):
    # 将点转换为 NumPy 数组
    a = np.array(point_a)
    b = np.array(point_b)
    
    # 计算方向向量
    direction_vector = b - a
    
    # 归一化方向向量
    norm = np.linalg.norm(direction_vector)
    if norm == 0:
        return np.zeros_like(direction_vector)
    
    unit_direction_vector = direction_vector / norm
    return unit_direction_vector

def calculate_points_with_vertical_direction(P, D, d):
    dx, dy = D
    
    # 计算在 xy 平面上的垂直向量 N
    N = np.array([-dy, dx])  # 垂直于 D 的二维向量
    
    # 计算左右目标点
    # 直接使用 N，按比例缩放
    L = np.array(P) + N * (d / np.linalg.norm(N))  # 左点
    R = np.array(P) - N * (d / np.linalg.norm(N))  # 右点

    return L.tolist(), R.tolist()

def calculate_angle_between_vectors(u, v):
    # 确保输入为 NumPy 数组
    u = np.array(u)
    v = np.array(v)

    # 计算点积
    dot_product = np.dot(u, v)

    # 确保点积在 [-1, 1] 范围内
    dot_product = np.clip(dot_product, -1.0, 1.0)

    # 计算夹角（以弧度为单位）
    angle_rad = np.arccos(dot_product)

    # 转换为度数
    angle_deg = np.degrees(angle_rad)

    return angle_deg

def calculate_point_to_segment_distance(point, segment_start, segment_end):
    # 将输入转换为 NumPy 数组
    point = np.array(point)
    segment_start = np.array(segment_start)
    segment_end = np.array(segment_end)
    
    # 计算线段的向量和点到线段起点的向量
    segment_vector = segment_end - segment_start
    point_vector = point - segment_start
    
    # 计算线段的长度的平方
    segment_length_squared = np.dot(segment_vector, segment_vector)
    
    # 处理线段长度为零的情况
    if segment_length_squared == 0:
        return np.linalg.norm(point_vector)  # 点到起点的距离
    
    # 计算投影系数 t
    t = np.dot(point_vector, segment_vector) / segment_length_squared
    
    # 限制 t 的范围在 [0, 1] 之间
    t = max(0, min(1, t))
    
    # 计算最近点的坐标
    nearest_point = segment_start + t * segment_vector
    
    # 计算距离
    distance = np.linalg.norm(point - nearest_point)
    
    return distance

def calculate_two_points_distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    
    distance = np.linalg.norm(point2 - point1)
    return distance

def create_transform_matrix(rotation_angle, translation_vector):
    # 创建旋转矩阵
    theta = np.radians(rotation_angle)  # 将角度转换为弧度
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])
    
    # 创建平移矩阵
    tx, ty = translation_vector
    translation_matrix = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    
    # 组合矩阵
    transform_matrix = np.dot(translation_matrix, rotation_matrix)
    return transform_matrix

def calculate_transform_point(point, transform_matrix):
    # 将点转换为齐次坐标
    point_homogeneous = np.array([point[0], point[1], 1])  # 单个点的齐次坐标
    
    # 应用变换
    transformed_point = np.dot(transform_matrix, point_homogeneous)
    
    return transformed_point[:2]  # 返回到二维坐标

def calculate_transform_points(points, transform_matrix):
    points = np.array(points)
    # 将点转换为齐次坐标
    points_homogeneous = np.hstack([points, np.ones((points.shape[0], 1))])
    
    # 应用变换
    transformed_points = np.dot(points_homogeneous, transform_matrix.T)
    
    return transformed_points[:, :2].tolist()  # 返回到二维坐标