import pyray as pr
import numpy as np
import time

import track_helper
import draw_helper

class CarRays():
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


    def test_rays(self, current_waypoint: int, car_angle: float, car_origin_x: int, car_origin_y: int, track: track_helper.Track):
        waypoint_count = len(track.waypoints)

        # Get points up to the max distance backwards and forwards
        back_waypoint = (current_waypoint - self.max_waypoints) % waypoint_count

        # Test points until a collision is detected per ray
        ray_indexes = [n for n in range(self.ray_count)]
        # iter_count = 0
        # iter_time_s = time.time()

        for waypoint_n in range(self.max_waypoints*2 + 1):
            last_waypoint_index = (back_waypoint + waypoint_n - 1) % waypoint_count
            waypoint_index = (back_waypoint + waypoint_n) % waypoint_count

            wall_l1 = track.waypoints[last_waypoint_index].left_shoulder
            wall_l2 = track.waypoints[waypoint_index].left_shoulder

            wall_r1 = track.waypoints[last_waypoint_index].right_shoulder
            wall_r2 = track.waypoints[waypoint_index].right_shoulder

            # Test all ray that haven't collided yet
            for ray_index in ray_indexes:
                if self.rays[ray_index].test_collision(pr.Vector2(car_origin_x, car_origin_y), wall_l1, wall_l2, car_angle):
                    ray_indexes.remove(ray_index)
                    continue
                if self.rays[ray_index].test_collision(pr.Vector2(car_origin_x, car_origin_y), wall_r1, wall_r2, car_angle):
                    ray_indexes.remove(ray_index)
                # iter_count += 1
                
            # Exit loops if all rays collided

            if len(ray_indexes) == 0:
                    break
        
        # print(f"Total test collision loops: {iter_count} {(time.time() - iter_time_s)/1000 :.5f}ms")

    def draw_rays(self, car_origin_x: int, car_origin_y: int, car_angle: float, color: pr.Color):
        for ray in self.rays:
            draw_helper.draw_vector(car_origin_x, car_origin_y, car_angle + ray.ray_angle, ray.distance, color)

class CarRay():
    def __init__(
        self,
        ray_angle: float, 
        max_distance: int):

        self.ray_angle: float = ray_angle
        self.max_distance: int = max_distance
        self.distance: int = max_distance

    # BUGGED, Rays very often goes straight through the wall
    def test_collision(self, origin: pr.Vector2, line_point_1: pr.Vector2, line_point_2: pr.Vector2, car_angle: float) -> bool:
        # Reset distance from previous calls
        self.distance = self.max_distance
        
        # Calculate the endpoint of the ray
        endpoint = pr.Vector2(
            origin.x + int(np.sin(car_angle+self.ray_angle)*self.max_distance), 
            origin.y - int(np.cos(car_angle+self.ray_angle)*self.max_distance)
        )
        collision: pr.Vector2 = pr.Vector2()
        if pr.check_collision_lines(
            origin,
            endpoint,
            line_point_1,
            line_point_2,
            collision):

            # print(f"Collision! angle {self.ray_angle} coords {collision.x} {collision.y}")

            # Replace the distance with the collision distance
            self.distance = int(pr.vector2_distance(origin, collision))
            assert(self.distance <= self.max_distance)
            
            return True
        return False


