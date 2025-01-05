import pyray as pr
import numpy as np

import utils

def draw_vector(origin_x: int, origin_y: int, angle: float, lenght: int, color: pr.Color):
    pr.draw_line(
        origin_x, 
        origin_y, 
        origin_x + int(np.sin(angle)*lenght), 
        origin_y - int(np.cos(angle)*lenght), 
        color)

def draw_arrow(origin_x: int, origin_y: int, angle: float, lenght: int, color: pr.Color):
    end_x, end_y = utils.calculate_point_displacement(origin_x, origin_y, angle, lenght)
    pr.draw_line(origin_x, origin_y, end_x, end_y, color)
    pr.draw_line(
        end_x, end_y,
        end_x + int(np.sin(angle+2.2)*lenght/3),
        end_y - int(np.cos(angle+2.2)*lenght/3),
        color
    )
    pr.draw_line(
        end_x, end_y,
        end_x + int(np.sin(angle-2.2)*lenght/3),
        end_y - int(np.cos(angle-2.2)*lenght/3),
        color
    )
    pass