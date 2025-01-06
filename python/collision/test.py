import pyray as pr

collision = pr.Vector2()
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

# Set test vectors
r1 = pr.Vector2(30470, -41061)
r2 = pr.Vector2(30117, -41060)

ray_origin = pr.Vector2(30108, -41398)
ray_end = pr.Vector2(31473, -39937)

# Test collision

print(pr.check_collision_lines(ray_origin, ray_end, r1, r2, collision))
print(check_line_intersection(ray_origin, ray_end, r1, r2, collision))