from enum import Enum

import numpy as np
import pyray as pr

from utils import calculate_angle, calculate_point_displacement

class TrackLenght(Enum):
    HELTER      = 170330
    WONDER      = 217817
    EDGE        = 184848
    OUT         = 182049
    PHANTOMILE  = 98395
    BRIGHTEST   = 189523
    HEAVEN      = 209919
    SHOOTING    = 129750

def get_track_name(track_id: int) -> str:
    match track_id:
        case 0:
            return "Helter Skelter"
        case 1:
            return "Wonderhill"
        case 2:
            return "Edge of the earth"
        case 3:
            return "Out of blue"
        case 4:
            return "Phantomile"
        case 5:
            return "Brightest nite"
        case 6:
            return "Heaven and hell"
        case 7:
            return "Shooting Hoops"
        case 8:
            return "Helter Skelter (Reverse)"
        case 9:
            return "Wonderhill (Reverse)"
        case 10:
            return "Edge of the earth (Reverse)"
        case 11:
            return "Out of blue (Reverse)"
        case 12:
            return "Phantomile (Reverse)"
        case 13:
            return "Brightest nite (Reverse)"
        case 14:
            return "Heaven and hell (Reverse)"
        case 15:
            return "Shooting Hoops (Reverse)"

def get_track_lenght(track_id: int) -> int:
    match track_id:
        case 0:
            return TrackLenght.HELTER.value
        case 1:
            return TrackLenght.WONDER.value
        case 2:
            return TrackLenght.EDGE.value
        case 3:
            return TrackLenght.OUT.value
        case 4:
            return TrackLenght.PHANTOMILE.value
        case 5:
            return TrackLenght.BRIGHTEST.value
        case 6:
            return TrackLenght.HEAVEN.value
        case 7:
            return TrackLenght.SHOOTING.value
        case 8:
            return TrackLenght.HELTER.value
        case 9:
            return TrackLenght.WONDER.value
        case 10:
            return TrackLenght.EDGE.value
        case 11:
            return TrackLenght.OUT.value
        case 12:
            return TrackLenght.PHANTOMILE.value
        case 13:
            return TrackLenght.BRIGHTEST.value
        case 14:
            return TrackLenght.HEAVEN.value
        case 15:
            return TrackLenght.SHOOTING.value


class Track():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.waypoints = []

    def __str__(self):
        return f"Track {self.name}: {len(self.waypoints)} waypoints."

    def add_waypoint(self, x,z,y,y_tangent,
    right_roadway_width, left_roadway_width, dist_to_next_waypoint, 
    right_shoulder_width, left_shoulder_width):
        self.waypoints.append(self.Waypoint(
            x,z,y,y_tangent,right_roadway_width,left_roadway_width, dist_to_next_waypoint, 
            right_shoulder_width,left_shoulder_width))

    class Waypoint():
        def __init__(self, x,z,y,y_tangent,
        right_roadway_width, left_roadway_width, dist_to_next_waypoint, 
        right_shoulder_width, left_shoulder_width):
            self.x = x
            self.z = -z
            self.y = y
            self.y_tangent = y_tangent
            self.right_roadway_width = right_roadway_width
            self.left_roadway_width = left_roadway_width
            self.dist_to_next_waypoint = dist_to_next_waypoint
            self.right_shoulder_width = right_shoulder_width
            self.left_shoulder_width = left_shoulder_width

            self.process()

        def __str__(self):
            return f"""x, y, z: {self.x}, {self.y}, {self.z}
y_tangent: {self.y_tangent}
left/right roadway width: {self.left_roadway_width}, {self.right_roadway_width}
left/right shoulder width: {self.left_shoulder_width}, {self.right_shoulder_width}
distance to next waypoint: {self.dist_to_next_waypoint}"""

        def process(self, scale: float = 1.0):
            self.angle = calculate_angle((-self.y_tangent + 2048)%4096)
            self.left_angle = calculate_angle((-self.y_tangent + 1024)%4096)
            self.right_angle = calculate_angle((-self.y_tangent + 3072)%4096)

            self.left_roadway = pr.Vector2(*calculate_point_displacement(
                self.x, self.z, self.left_angle, 
                self.left_roadway_width*scale))

            self.right_roadway = pr.Vector2(*calculate_point_displacement(
                self.x, self.z, self.right_angle, 
                self.right_roadway_width*scale))

            self.left_shoulder = pr.Vector2(*calculate_point_displacement(
                self.x, self.z, self.left_angle, 
                (self.left_roadway_width + self.left_shoulder_width)*scale))
                
            self.right_shoulder = pr.Vector2(*calculate_point_displacement(
                self.x, self.z, self.right_angle, 
                (self.right_roadway_width + self.right_shoulder_width)*scale))
            pass