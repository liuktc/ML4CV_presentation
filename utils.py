import numpy as np
from manim import *


def get_square_corners(square: Mobject):
    """Get the corners of a square in a list."""
    return [
        np.array([square.get_left()[0], square.get_top()[1], 0]),
        np.array([square.get_left()[0], square.get_bottom()[1], 0]),
        np.array([square.get_right()[0], square.get_bottom()[1], 0]),
        np.array([square.get_right()[0], square.get_top()[1], 0]),
    ]


def right_angle_arrow_custom(
    start,
    end,
    horizontal_first: bool = False,
    color=WHITE,
    stroke_width=4,
    right_angle_size=0.2,
    aligned_edge=RIGHT,
):
    """Creates a right-angle arrow with custom path and optional right angle indicator."""
    # Calculate the corner point
    if horizontal_first:
        corner = np.array([end[0], start[1], 0])
    else:
        corner = np.array([start[0], end[1], 0])

    # Create the path
    path = VMobject()
    path.set_points_as_corners([start, corner, end])
    path.set_color(color).set_stroke(width=stroke_width)

    # Create the arrow
    arrow = ArrowTriangleFilledTip().scale(0.8)
    arrow.move_to(end, aligned_edge=aligned_edge)
    arrow.rotate(angle_of_vector(corner - end))
    arrow.set_color(color)

    # Group path and arrow tip
    result = VGroup(path, arrow)

    # Optional: add right angle indicator
    # line1 = Line(start, corner)
    # line2 = Line(corner, end)
    # right_angle = RightAngle(line1, line2, length=right_angle_size, color=color)

    return VGroup(result)
