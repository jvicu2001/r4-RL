import pyray as pr
import peewee

from harvest_track import TrackData

db = peewee.SqliteDatabase("track_data.db")
db.connect()


current_track = 0

# Get current track's points
def change_track(track_id: int = 0):
    points = TrackData.select().where(TrackData.track_id==track_id).order_by(TrackData.lap_progress)
    points_l = points.where(TrackData.side==0)
    points_r = points.where(TrackData.side==1)
    points_count = points.count()
    return points, points_l, points_r, points_count

points, points_l, points_r, points_count = change_track(0)

camera = pr.Camera2D(pr.Vector2(0,0))
camera.zoom = 0.01
camera.target = pr.Vector2(points[0].x_pos, points[0].z_pos)

pr.set_target_fps(60)

pr.set_config_flags(
    pr.FLAG_WINDOW_RESIZABLE
)
pr.init_window(800, 600, "Map viewer")
# Main Loop
while not pr.window_should_close():
    # Update

    ## Camera movement
    if (pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT)):
        delta: pr.Vector2 = pr.get_mouse_delta()
        delta = pr.vector2_scale(delta, -1.0/camera.zoom)
        camera.target = pr.vector2_add(camera.target, delta)

    ## Zoom
    wheel: float = pr.get_mouse_wheel_move()
    if wheel != 0.0:
        scale_factor: float = 1.0 +(0.25*abs(wheel))
        if (wheel < 0):
            scale_factor = 1.0/scale_factor
        camera.zoom = pr.clamp(camera.zoom*scale_factor, 0.00125, 64.0)

    ## Map change
    if (pr.is_key_pressed(pr.KEY_Q) or pr.is_key_pressed(pr.KEY_W)):
        if pr.is_key_pressed(pr.KEY_Q):
            current_track = (current_track-1)%8
        if pr.is_key_pressed(pr.KEY_W):
            current_track = (current_track+1)%8
        points, points_l, points_r, points_count = change_track(current_track)

    # Draw
    pr.begin_drawing()
    pr.clear_background(pr.WHITE)

    pr.begin_mode_2d(camera)
    # Draw the walls
    for ps in [points_l, points_r]:
        for n in range(ps.count()):
            pr.draw_line(ps[n-1].x_pos, ps[n-1].z_pos, ps[n].x_pos, ps[n].z_pos, pr.RED if ps[n].side==0 else pr.BLUE)
    pr.end_mode_2d()

    info_text = f"""Points loaded: {points_count}
Current track: {current_track}"""
    pr.draw_text(info_text, 10, 10, 15, pr.BLACK)
    pr.end_drawing()
pr.close_window()