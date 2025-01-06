import numpy as np
import pyray as pr

# Angle converter
def calculate_angle(raw_angle: int) -> float:
    return (raw_angle*2*np.pi)/4096

# Calculate point displacement from origin, angle and distance
def calculate_point_displacement(origin_x: int, origin_y: int, angle: float, lenght: int):
    end_x, end_y = origin_x + int(np.sin(angle)*lenght), origin_y - int(np.cos(angle)*lenght)
    return (end_x, end_y)

# Check if two lines intersect and if so, save the collision point
# In replacement of pyray.check_collision_lines that is not working properly
def check_line_intersection(vec_a: pr.Vector2, vec_b: pr.Vector2, vec_c: pr.Vector2, vec_d: pr.Vector2, collision: pr.Vector2):
    s1_x = vec_b.x - vec_a.x
    s1_y = vec_b.y - vec_a.y
    s2_x = vec_d.x - vec_c.x
    s2_y = vec_d.y - vec_c.y

    # Catch division by zero
    divisor = (-s2_x * s1_y + s1_x * s2_y)
    if (divisor) == 0:
        return False

    s = (-s1_y * (vec_a.x - vec_c.x) + s1_x * (vec_a.y - vec_c.y)) / (divisor)
    t = (s2_x * (vec_a.y - vec_c.y) - s2_y * (vec_a.x - vec_c.x)) / (divisor)

    if 0 <= s <= 1 and 0 <= t <= 1:
        collision.x = vec_a.x + (t * s1_x)
        collision.y = vec_a.y + (t * s1_y)
        return True
    
    return False