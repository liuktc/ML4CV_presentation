from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners


class ReceptiveField(MySlide):
    def construct(self):
        np.random.seed(0)  # For reproducibility
        input_image = ImageMobject(np.uint8(np.random.rand(28, 28, 1) * 255))
        input_image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        input_image.scale_to_fit_width(3)
        input_image.to_edge(LEFT, buff=0.2)

        feature_map = ImageMobject(np.uint8(np.random.rand(7, 7, 1) * 255))
        feature_map.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        feature_map.scale_to_fit_width(3)
        feature_map.next_to(input_image, RIGHT, buff=0.5)

        images_group = Group(input_image, feature_map)
        images_group.move_to(ORIGIN)

        text_input = Tex("Input Image").scale(0.6)
        text_input.move_to(input_image.get_top() + 0.2 * UP)
        text_feature_map = Tex("Feature Map").scale(0.6)
        text_feature_map.move_to(feature_map.get_top() + 0.2 * UP)

        self.p.play([FadeIn(input_image), Write(text_input)])
        self.p.play([FadeIn(feature_map), Write(text_feature_map)])

        image_pixels = 2
        pixel_size = input_image.width / image_pixels
        small_square_image = Square(side_length=pixel_size, fill_opacity=0.5)

        feature_map_pixels = 7
        feature_map_pixel_size = feature_map.width / feature_map_pixels
        small_square_feature_map = Square(
            side_length=feature_map_pixel_size, fill_opacity=0.5
        )
        small_square_feature_map.set_color(RED)

        upper_left_corner_image = np.array(
            [
                input_image.get_left()[0] + pixel_size / 2,
                input_image.get_top()[1] - pixel_size / 2,
                0,
            ]
        )
        small_square_image.move_to(upper_left_corner_image)
        self.p.play(Create(small_square_image))

        upper_left_corner_feature_map = np.array(
            [
                feature_map.get_left()[0] + feature_map_pixel_size / 2,
                feature_map.get_top()[1] - feature_map_pixel_size / 2,
                0,
            ]
        )
        small_square_feature_map.move_to(upper_left_corner_feature_map)
        self.p.play(Create(small_square_feature_map))

        # small_square.
        # Put the small square in the upper right corner of the input image
        old_lines = []
        input_i, input_j = ValueTracker(), ValueTracker()
        feature_map_i, feature_map_j = ValueTracker(), ValueTracker()

        feature_map_text = MathTex(
            f"a_{{{int(feature_map_i.get_value())},{int(feature_map_j.get_value())}}}"
        )
        # feature_map_text.scale(0.5)
        feature_map_text.next_to(feature_map, DOWN, buff=0.2)
        feature_map_text.set_color(RED)

        def update_text(text: MathTex):
            text_copy = MathTex(
                f"a_{{{int(feature_map_i.get_value())},{int(feature_map_j.get_value())}}}"
            )
            # text_copy.scale(0.5)
            text_copy.move_to(text.get_center())
            text_copy.set_color(RED)
            text_copy.set_opacity(0.5)

            text.become(text_copy)  # Update the text with the new value
            # return text_copy

        feature_map_text.add_updater(
            lambda m: update_text(m)  # Update the text with the current i and j values
        )
        self.p.play(Write(feature_map_text))

        small_square_image.add_updater(
            lambda m: m.move_to(
                upper_left_corner_image
                + DOWN * input_i.get_value() * pixel_size
                + RIGHT * input_j.get_value() * pixel_size
            )
        )

        small_square_feature_map.add_updater(
            lambda m: m.move_to(
                upper_left_corner_feature_map
                + DOWN * feature_map_i.get_value() * feature_map_pixel_size
                + RIGHT * feature_map_j.get_value() * feature_map_pixel_size
            )
        )

        small_square_image_corners = get_square_corners(small_square_image)
        small_square_feature_map_corners = get_square_corners(small_square_feature_map)

        def update_line(line: Line):
            i = line.i
            small_square_image_corners = get_square_corners(small_square_image)
            small_square_feature_map_corners = get_square_corners(
                small_square_feature_map
            )
            line.put_start_and_end_on(
                small_square_image_corners[i], small_square_feature_map_corners[i]
            )

        lines = []
        for i in range(4):
            line = Line(
                small_square_image_corners[i], small_square_feature_map_corners[i]
            )
            line.set_color(RED)
            line.set_stroke(width=4)
            line.set_opacity(0.5)
            line.i = i
            line.add_updater(lambda m: update_line(m))
            lines.append(line)
            # self.p.play(FadeIn(line))
        self.p.play([Create(line) for line in lines])

        for i in range(image_pixels):
            for j in range(image_pixels):
                self.p.play(input_i.animate.set_value(i), input_j.animate.set_value(j))
                self.p.play(
                    feature_map_i.animate.set_value(i),
                    feature_map_j.animate.set_value(j),
                )
