import socket
import time

import pyray as pr
import numpy as np

import track_helper
import collision.collision_check
import extract_tracks

from proto import game_pb2

import draw_helper

from utils import calculate_angle, calculate_point_displacement

# Load tracks
tracks = []
try:
    tracks = sorted(extract_tracks.get_tracks(), key=lambda x: x.id)
except Exception as err:
    print("Error fetching track info. Have you extracted R4.BIN yet?")
    exit()

# Get current track
def change_track(track_id: int = 0):
    return tracks[track_id%8]

current_track: track_helper.Track = change_track(0)

# Track drawing mode
track_draw_full = True

# Game info socket parameters
UDP_HOST, UDP_PORT = "localhost", 7651
game_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
game_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
game_socket.bind((UDP_HOST, UDP_PORT))
game_socket.setblocking(False)

# Game packet
game_info: game_pb2.GameInfo = game_pb2.GameInfo()
car_info: game_pb2.GameInfo.CarInfo = game_info.CarInfo()
track_info: game_pb2.GameInfo.TrackInfo = game_info.TrackInfo()
game_packet_recv_time = time.time()

# Collision "rays"
car_rays_maxdistance = 2000
car_rays_amount = 5
car_rays_enable = False
car_rays: collision.collision_check.CarRays = collision.collision_check.CarRays(car_rays_maxdistance, 10, car_rays_amount, np.pi)

camera = pr.Camera2D(pr.Vector2(0,0))
camera.zoom = 0.01
camera.target = pr.Vector2(0, 0)
camera.offset = pr.Vector2(pr.get_screen_width()/2.0, pr.get_screen_height()/2.0)
camera_follow_car = False
camera_follow_car_rotation = False

pr.set_target_fps(60)

pr.set_config_flags(
    pr.FLAG_WINDOW_RESIZABLE
)
pr.init_window(800, 600, "Map viewer")
# Main Loop
while not pr.window_should_close():
    # Update

    ## Car info retrieval via socket
    try:
        recv_data, recv_addr = game_socket.recvfrom(1024)
        game_info.ParseFromString(recv_data)
        car_info = game_info.car_info
        track_info = game_info.track_info
        # print(game_info)

        game_packet_recv_time = time.time()
    except:
        pass

    ## Check for map change
    if track_info.track_id is not current_track.id:
        current_track = change_track(track_info.track_id)

    ## Camera mouse movement
    if (pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT)):
        delta: pr.Vector2 = pr.get_mouse_delta()
        delta = pr.vector2_scale(delta, -1.0/camera.zoom)
        camera.target = pr.vector2_add(camera.target, delta)

    ## Change car chase mode
    if pr.is_key_pressed(pr.KEY_Z):
        camera_follow_car = not camera_follow_car
    if pr.is_key_pressed(pr.KEY_X):
        camera_follow_car_rotation = not camera_follow_car_rotation

        # Reset camera rotation
        if not camera_follow_car_rotation:
            camera.rotation = 0.0

    ## Car chase
    if camera_follow_car:
        camera.offset = pr.Vector2(pr.get_screen_width()/2.0, pr.get_screen_height()/2.0)
        camera.target = pr.Vector2(car_info.x_pos, -car_info.z_pos)

        if camera_follow_car_rotation:
            camera.rotation = -(car_info.applied_direction*360)/4096

    ## Zoom
    wheel: float = pr.get_mouse_wheel_move()
    if wheel != 0.0:
        scale_factor: float = 1.0 +(0.25*abs(wheel))
        if (wheel < 0):
            scale_factor = 1.0/scale_factor
        camera.zoom = pr.clamp(camera.zoom*scale_factor, 0.00125, 64.0)

    ## Toggle track drawing mode
    if (pr.is_key_pressed(pr.KEY_V)):
        track_draw_full = not track_draw_full

    ## Toggle Car Rays
    if pr.is_key_pressed(pr.KEY_C):
        car_rays_enable = not car_rays_enable

    ## Car Rays
    if car_rays_enable:
        car_rays.test_rays(
            current_waypoint=track_info.current_waypoint, 
            car_angle=calculate_angle(car_info.applied_direction), 
            car_origin_x=car_info.x_pos, car_origin_y=-car_info.z_pos,
            track=current_track)

    ## Calculate bounding box
    bbox1_x, bbox1_z = calculate_point_displacement(
        car_info.x_pos + car_info.bbox_vx1,
        -(car_info.z_pos + car_info.bbox_vz1),
        calculate_angle(car_info.applied_direction), -123)
    
    bbox2_x, bbox2_z = calculate_point_displacement(
        car_info.x_pos + car_info.bbox_vx2,
        -(car_info.z_pos + car_info.bbox_vz2),
        calculate_angle(car_info.applied_direction), -123)

    bbox3_x, bbox3_z = calculate_point_displacement(
        car_info.x_pos + car_info.bbox_vx3,
        -(car_info.z_pos + car_info.bbox_vz3),
        calculate_angle(car_info.applied_direction), -123)

    bbox4_x, bbox4_z = calculate_point_displacement(
        car_info.x_pos + car_info.bbox_vx4,
        -(car_info.z_pos + car_info.bbox_vz4),
        calculate_angle(car_info.applied_direction), -123)

    # Draw
    pr.begin_drawing()
    pr.clear_background(pr.WHITE)

    pr.begin_mode_2d(camera)

    # Draw track
    for waypoint_n in range(len(current_track.waypoints)):
        waypoint = current_track.waypoints[waypoint_n]
        last_waypoint = current_track.waypoints[waypoint_n-1]

        ## Draw the road as polygons
        if track_draw_full:
            # Draw road
            pr.draw_triangle(
                last_waypoint.left_roadway,
                waypoint.left_roadway,
                last_waypoint.right_roadway,
                pr.GRAY
                )
            pr.draw_triangle(
                waypoint.left_roadway,
                waypoint.right_roadway,
                last_waypoint.right_roadway,
                pr.GRAY
                )

            # Draw shoulders
            ## Left shoulders
            pr.draw_triangle(
                last_waypoint.left_shoulder,
                waypoint.left_shoulder,
                last_waypoint.left_roadway,
                pr.BROWN
                )
            pr.draw_triangle(
                waypoint.left_roadway, 
                last_waypoint.left_roadway,
                waypoint.left_shoulder,
                pr.BROWN
                )

            ## Right shoulders
            pr.draw_triangle(
                last_waypoint.right_roadway,
                waypoint.right_shoulder,
                last_waypoint.right_shoulder,
                pr.BROWN
                )
            pr.draw_triangle(
                waypoint.right_shoulder, 
                last_waypoint.right_roadway,
                waypoint.right_roadway,
                pr.BROWN
                )
        else:
            # Draw road
            pr.draw_line(int(last_waypoint.left_roadway.x), 
            int(last_waypoint.left_roadway.y), 
            int(waypoint.left_roadway.x), 
            int(waypoint.left_roadway.y), pr.BROWN)

            pr.draw_line(int(last_waypoint.right_roadway.x), 
            int(last_waypoint.right_roadway.y), 
            int(waypoint.right_roadway.x), 
            int(waypoint.right_roadway.y), pr.BROWN)

            # Draw shoulders
            pr.draw_line(int(last_waypoint.left_shoulder.x), 
            int(last_waypoint.left_shoulder.y), 
            int(waypoint.left_shoulder.x), 
            int(waypoint.left_shoulder.y), pr.GRAY)

            pr.draw_line(int(last_waypoint.right_shoulder.x), 
            int(last_waypoint.right_shoulder.y), 
            int(waypoint.right_shoulder.x), 
            int(waypoint.right_shoulder.y), pr.GRAY)

            pr.draw_text(f"{int(waypoint.right_shoulder.x)} {int(waypoint.right_shoulder.y)}",
            int(waypoint.right_shoulder.x), int(waypoint.right_shoulder.y), 15, pr.BLACK)

            # Connect waypoint sides
            pr.draw_line(int(waypoint.left_shoulder.x), 
            int(waypoint.left_shoulder.y), 
            int(waypoint.right_shoulder.x), 
            int(waypoint.right_shoulder.y), pr.GREEN)

            pr.draw_line(int(waypoint.left_roadway.x), 
            int(waypoint.left_roadway.y), 
            int(waypoint.right_roadway.x), 
            int(waypoint.right_roadway.y), pr.GREEN)

            pr.draw_circle(int(waypoint.x), int(waypoint.z), 25.0, pr.GREEN)

            # Draw waypoint order and distance to next waypoint
            pr.draw_text(f"{waypoint_n}         {waypoint.dist_to_next_waypoint}",
                waypoint.x - 110, waypoint.z + 30, 30, pr.BLACK)

    # Draw car Bounding Box
    pr.draw_line(
        bbox1_x,
        bbox1_z,
        bbox2_x,
        bbox2_z,
        pr.BLACK
    )

    pr.draw_line(
        bbox2_x,
        bbox2_z,
        bbox4_x,
        bbox4_z,
        pr.BLACK
    )

    pr.draw_line(
        bbox4_x,
        bbox4_z,
        bbox3_x,
        bbox3_z,
        pr.BLACK
    )
    
    pr.draw_line(
        bbox3_x,
        bbox3_z,
        bbox1_x,
        bbox1_z,
        pr.BLACK
    )

    if not track_draw_full:
        pr.draw_text(f"{bbox1_x} {bbox1_z}",
        bbox1_x, bbox1_z, 15, pr.BLACK)
        pr.draw_text(f"{bbox2_x} {bbox2_z}",
        bbox2_x, bbox2_z, 15, pr.BLACK)
        pr.draw_text(f"{bbox3_x} {bbox3_z}",
        bbox3_x, bbox3_z, 15, pr.BLACK)
        pr.draw_text(f"{bbox4_x} {bbox4_z}",
        bbox4_x, bbox4_z, 15, pr.BLACK)

    ## Car vectors
    draw_helper.draw_arrow(
        car_info.x_pos, 
        -car_info.z_pos,
        calculate_angle(car_info.applied_direction),
        800,
        pr.RED)
    draw_helper.draw_arrow(
        car_info.x_pos, 
        -car_info.z_pos,
        calculate_angle(car_info.intended_direction),
        800,
        pr.BLUE)

    ## Car rays
    if car_rays_enable:    
        car_rays.draw_rays(    
            car_info.x_pos, -car_info.z_pos,        
            calculate_angle(car_info.applied_direction),        
            pr.VIOLET)

    pr.end_mode_2d()



    info_text = f"""Time since last packet: {(time.time() - game_packet_recv_time):.2f}s
Packet frequency: {(1/(time.time() - game_packet_recv_time)):.2f}Hz
FPS: {pr.get_fps()}

Car Info:
    Coords: X:{car_info.x_pos}, Y:{car_info.y_pos}, Z:{car_info.z_pos}
    Applied Direction: {car_info.applied_direction}
    Intended Direction: {car_info.intended_direction}
    
    Speed: {car_info.speed}
    RPM: {car_info.rpm}
    Gear: {car_info.gear}
    
    In Air: {"True" if car_info.free_fall else "False"}
    Drift Timeout: {car_info.drift_timeout}
    
Track Info:
    Current track: {track_helper.get_track_name(track_info.track_id)}
    Current lap: {track_info.lap}
    Track Status: {
        "Count down" if track_info.track_status == 1 
        else "Racing/Replay" if track_info.track_status == 2 
        else "Race Finished."}
    Track Progress: {track_info.track_progress}
    Lap Progress: {track_info.lap_progress}
    Current Waypoint: {track_info.current_waypoint}
"""



    # if car_rays_enable:
    #     info_text = info_text + "\nDistance info:\n"
    #     for ray in car_rays.rays:
    #         info_text = info_text + f"  {ray.ray_angle:.2f}: {ray.distance}\n"
    pr.draw_text(info_text, 10, 10, 15, pr.BLACK)

    mouse_pos: pr.Vector2 = pr.get_mouse_position()
    camera_pos: pr.Vector2 = pr.get_screen_to_world_2d(mouse_pos, camera)
    pr.draw_text(f"Mouse pos: {camera_pos.x:.0f},  {camera_pos.y:.0f}", pr.get_screen_width()-300, 10, 15, pr.BLACK)
    pr.end_drawing()
pr.close_window()

game_socket.close()