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
        raise ValueError("The two points are the same; direction vector cannot be normalized.")
    
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

    # 转换为度数（可选）
    angle_deg = np.degrees(angle_rad)

    return angle_rad, angle_deg