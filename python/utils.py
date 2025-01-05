import numpy as np

# Angle converter
def calculate_angle(raw_angle: int) -> float:
    return (raw_angle*2*np.pi)/4096

# Calculate point displacement from origin, angle and distance
def calculate_point_displacement(origin_x: int, origin_y: int, angle: float, lenght: int):
    end_x, end_y = origin_x + int(np.sin(angle)*lenght), origin_y - int(np.cos(angle)*lenght)
    return (end_x, end_y)