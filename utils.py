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
        return [0, 0, 0]
    
    unit_direction_vector = direction_vector / norm
    return unit_direction_vector

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