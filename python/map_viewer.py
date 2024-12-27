import socket
import time

import pyray as pr
import peewee
import numpy as np

from harvest_track import TrackData
import track_helper
import collision.collision_check

from proto import game_pb2

import draw_helper

db = peewee.SqliteDatabase("track_data.db")
db.connect()

current_track = 0

# Get current track's points
def change_track(track_id: int = 0):
    points = TrackData.select().where(TrackData.track_id==track_id%8).order_by(TrackData.lap_progress)
    points_l = points.where(TrackData.side==0)
    points_r = points.where(TrackData.side==1)
    points_count = points.count()
    return points, points_l, points_r, points_count

points, points_l, points_r, points_count = change_track(0)

# Car angle converter
def calculate_car_angle(raw_angle: int) -> float:
    return (raw_angle*2*np.pi)/4096

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
car_rays: collision.collision_check.CarRays = collision.collision_check.CarRays(car_rays_maxdistance, car_rays_amount, np.pi)

camera = pr.Camera2D(pr.Vector2(0,0))
camera.zoom = 0.01
camera.target = pr.Vector2(points[0].x_pos - 40000, -points[0].z_pos - 40000)
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
    if track_info.track_id is not current_track:
        current_track = track_info.track_id
        points, points_l, points_r, points_count = change_track(current_track)

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

    ## Map change
    # if (pr.is_key_pressed(pr.KEY_Q) or pr.is_key_pressed(pr.KEY_W)):
    #     if pr.is_key_pressed(pr.KEY_Q):
    #         current_track = (current_track-1)%8
    #     if pr.is_key_pressed(pr.KEY_W):
    #         current_track = (current_track+1)%8
    #     points, points_l, points_r, points_count = change_track(current_track)

    ## Toggle Car Rays
    if pr.is_key_pressed(pr.KEY_C):
        car_rays_enable = not car_rays_enable

    ## Car Rays
    if car_rays_enable:
        car_rays.test_rays(
            lap_progress=track_info.lap_progress, 
            car_angle=calculate_car_angle(car_info.applied_direction), 
            car_origin_x=car_info.x_pos, car_origin_y=-car_info.z_pos,
            track_id=track_info.track_id,
            points=points)

    # Draw
    pr.begin_drawing()
    pr.clear_background(pr.WHITE)

    pr.begin_mode_2d(camera)
    # Draw the walls
    for ps in [points_l, points_r]:
        for n in range(ps.count()):
            pr.draw_line(ps[n-1].x_pos, -ps[n-1].z_pos, ps[n].x_pos, -ps[n].z_pos, pr.RED if ps[n].side==0 else pr.BLUE)
    
    # Draw start line aprox
    p_start_l = points_l[0]
    p_start_r = points_r[0]
    pr.draw_line(p_start_l.x_pos, -p_start_l.z_pos, p_start_r.x_pos, -p_start_r.z_pos, pr.GREEN)

    # Draw car
    pr.draw_circle(car_info.x_pos, -car_info.z_pos, 100.0, pr.BLACK)
    ## Car vectors
    draw_helper.draw_arrow(
        car_info.x_pos, 
        -car_info.z_pos,
        calculate_car_angle(car_info.applied_direction),
        800,
        pr.RED)
    draw_helper.draw_arrow(
        car_info.x_pos, 
        -car_info.z_pos,
        calculate_car_angle(car_info.intended_direction),
        800,
        pr.BLUE)

    ## Car rays
    if car_rays_enable:
        car_rays.draw_rays(
            car_info.x_pos, -car_info.z_pos,
            calculate_car_angle(car_info.applied_direction),
            pr.VIOLET)

    pr.end_mode_2d()



    info_text = f"""Points loaded: {points_count}
Time since last packet: {(time.time() - game_packet_recv_time):.2f}s
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
        "Count down" if track_info.track_status is 1 
        else "Racing/Replay" if track_info.track_status is 2 
        else "Race Finished."}
    Track Progress: {track_info.track_progress}
    Lap Progress: {track_info.lap_progress}
"""

    if car_rays_enable:
        info_text = info_text + "\nDistance info:\n"
        for ray in car_rays.rays:
            info_text = info_text + f"  {ray.ray_angle:.2f}: {ray.distance}\n"
    pr.draw_text(info_text, 10, 10, 15, pr.BLACK)

    mouse_pos: pr.Vector2 = pr.get_mouse_position()
    camera_pos: pr.Vector2 = pr.get_screen_to_world_2d(mouse_pos, camera)
    pr.draw_text(f"Mouse pos: {camera_pos.x:.0f},  {camera_pos.y:.0f}", pr.get_screen_width()-300, 10, 15, pr.BLACK)
    pr.end_drawing()
pr.close_window()

game_socket.close()