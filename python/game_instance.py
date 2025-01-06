import socket
import time

import proto.game_pb2 as game_pb2
from collision import collision_check
from track_helper import Track
import extract_tracks

from utils import calculate_angle

class GameCar:
    def __init__(self, 
                 udp_host: str, udp_port: int, socket_blocking: bool,
                 rays_max_distance: int, rays_max_waypoints: int, ray_count: int, ray_arc: float, rays_enabled: bool):
        
        self.game_info: game_pb2.GameInfo = game_pb2.GameInfo()
        self.track_info: game_pb2.GameInfo.TrackInfo = self.game_info.TrackInfo()
        self.car_info: game_pb2.GameInfo.CarInfo = self.game_info.CarInfo()

        self.tracks: list[Track] = []
        self.current_track: Track = None

        self.active_waypoints: list[Track.Waypoint] = []

        self.configure_socket(udp_host, udp_port, socket_blocking)
        self.time_since_last_packet = time.time()

        self.configure_rays(rays_max_distance, rays_max_waypoints, ray_count, ray_arc, rays_enabled)
        self.fetch_tracks()
        self.change_track(0)
        self.update_waypoints()
        pass

    def configure_socket(self, host: str, port: int, blocking: bool = False):
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.game_socket.bind((host, port))

        # For the map viewer, the socket should be non-blocking
        # For the NN model, the socket should be blocking to wait for the next frame
        self.game_socket.setblocking(blocking)
        pass

    def configure_rays(self, max_distance: int, max_waypoints: int, ray_count: int, ray_arc: float, ray_enabled: bool):
        self.car_rays: collision_check.CarRays = collision_check.CarRays(max_distance, max_waypoints, ray_count, ray_arc)
        self.car_rays_enabled = ray_enabled
        pass

    def fetch_tracks(self):
        self.tracks = extract_tracks.get_tracks()

    def change_track(self, track_id: int):
        self.current_track = [x for x in self.tracks if x.id == track_id%8][0]
        pass

    def update_waypoints(self):
        self.active_waypoints: list[Track.Waypoint] = []

        back_waypoint = (self.track_info.current_waypoint - self.car_rays.max_waypoints) % len(self.current_track.waypoints)
        front_waypoint = (self.track_info.current_waypoint + self.car_rays.max_waypoints) % len(self.current_track.waypoints)

        if back_waypoint < front_waypoint:
            self.active_waypoints: list[Track.Waypoint] = self.current_track.waypoints[back_waypoint:front_waypoint]
        else:
            self.active_waypoints: list[Track.Waypoint] = self.current_track.waypoints[back_waypoint:] + self.current_track.waypoints[:front_waypoint]

    def receive_data(self):
        try:
            data, addr = self.game_socket.recvfrom(1024)
            self.game_info.ParseFromString(data)
            self.track_info = self.game_info.track_info
            self.car_info = self.game_info.car_info
            return True
        except:
            return False
    
    def update(self):
        # Receive data from socket
        if self.receive_data():
            self.time_since_last_packet = time.time()

            # Check if track changed
            if self.track_info.track_id != self.current_track.id:
                self.change_track(self.track_info.track_id%8)

            # Update waypoints
            self.update_waypoints()

            # Process rays if enabled
            if self.car_rays_enabled:
                self.car_rays.test_rays(
                    car_angle=calculate_angle(self.car_info.applied_direction), 
                    car_origin_x=self.car_info.x_pos, 
                    car_origin_y=-self.car_info.z_pos, 
                    waypoints=self.active_waypoints)
            
            return True
        return False
    