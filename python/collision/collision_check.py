import pyray as pr
import numpy as np
import time

import track_helper
import draw_helper

from utils import calculate_point_displacement, check_line_intersection, cubic_bezier_curve

class CarRays:
    def __init__(self,
        max_distance: int,
        max_waypoints: int,
        ray_count: int,
        ray_arc: float):

        self.rays: list[CarRay] = []
        self.ray_count = ray_count
        self.max_distance = max_distance
        self.max_waypoints = max_waypoints
        for n in range(ray_count):
            n_angle = ray_arc * (n/(ray_count-1) - 0.5)
            self.rays.append(CarRay(n_angle, max_distance))
        pass


    def test_rays(self, car_angle: float, car_origin_x: int, car_origin_y: int, waypoints: list[track_helper.Track.Waypoint]):
        # Reset all ray distances
        for ray in self.rays:
            ray.distance = ray.max_distance
        
        waypoint_count = len(waypoints)

        # Test points until a collision is detected per ray
        ray_indexes = [n for n in range(self.ray_count)]
        # iter_count = 0
        # iter_time_s = time.time()

        for waypoint_n in range(1, waypoint_count):
            last_waypoint= waypoints[waypoint_n-1]
            waypoint = waypoints[waypoint_n]

            wall_l1 = last_waypoint.left_shoulder
            wall_l2 = waypoint.left_shoulder

            wall_r1 = last_waypoint.right_shoulder
            wall_r2 = waypoint.right_shoulder

            # Test all rays
            for ray_index in ray_indexes:
                ray = self.rays[ray_index]
                ray_origin = pr.Vector2(car_origin_x, car_origin_y)
                ray_end = pr.Vector2(*calculate_point_displacement(
                    car_origin_x, car_origin_y, car_angle + ray.ray_angle, ray.max_distance
                ))
                collision = pr.Vector2()

                # Check left wall
                if check_line_intersection(ray_origin, ray_end, wall_l1, wall_l2, collision):
                    new_distance = int(pr.vector2_distance(ray_origin, collision))
                    if new_distance < ray.distance:
                        ray.distance = new_distance
                    continue

                # Check right wall
                if check_line_intersection(ray_origin, ray_end, wall_r1, wall_r2, collision):
                    new_distance = int(pr.vector2_distance(ray_origin, collision))
                    if new_distance < ray.distance:
                        ray.distance = new_distance
                    continue

                # # Check left wall vertices
                # if pr.check_collision_point_line(wall_l1, ray_origin, ray_end, 10):
                #     new_distance = int(pr.vector2_distance(ray_origin, wall_l1))
                #     if new_distance < ray.distance:
                #         ray.distance = new_distance
                #     continue
                # if pr.check_collision_point_line(wall_l2, ray_origin, ray_end, 10):
                #     new_distance = int(pr.vector2_distance(ray_origin, wall_l2))
                #     if new_distance < ray.distance:
                #         ray.distance = new_distance
                #     continue

                # # Check right wall vertices
                # if pr.check_collision_point_line(wall_r1, ray_origin, ray_end, 10):
                #     new_distance = int(pr.vector2_distance(ray_origin, wall_r1))
                #     if new_distance < ray.distance:
                #         ray.distance = new_distance
                #     continue
                # if pr.check_collision_point_line(wall_r2, ray_origin, ray_end, 10):
                #     new_distance = int(pr.vector2_distance(ray_origin, wall_r2))
                #     if new_distance < ray.distance:
                #         ray.distance = new_distance
                #     continue
        
        # print(f"Total test collision loops: {iter_count} {(time.time() - iter_time_s)/1000 :.5f}ms")

    def draw_rays(self, car_origin_x: int, car_origin_y: int, car_angle: float, color: pr.Color):
        for ray in self.rays:
            draw_helper.draw_vector(car_origin_x, car_origin_y, car_angle + ray.ray_angle, ray.distance, color)

class CarRay:
    def __init__(
        self,
        ray_angle: float, 
        max_distance: int):

        self.ray_angle: float = ray_angle
        self.max_distance: int = max_distance
        self.distance: int = max_distance