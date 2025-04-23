from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners


class Upscaling(MySlide):
    def construct(self):
        # Add an input image
        np.random.seed(0)  # For reproducibility
        input_image = ImageMobject(
            "./images/attribution_map_layer_20_bilinearUpsampling_small.png"
        )
        input_image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        input_image.scale_to_fit_width(2)
        input_image.to_edge(LEFT, buff=0.5)
        text = Tex(r"Attribution Map\\$7 \times 7$").scale(0.67)
        # text.move_to(input_image.get_top() + 0.2 * UP)
        # Move the text above the image without overlapping
        text.move_to(input_image.get_top() + 0.2 * UP, aligned_edge=DOWN)
        # input_image.shift(UP * 2)
        self.p.play([FadeIn(input_image), Write(text)])
        self.p.next_slide()

        upsampled_image = ImageMobject(
            "./images/attribution_map_layer_20_bilinearUpsampling.png"
        )
        upsampled_image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        upsampled_image.move_to(ORIGIN)
        upsampled_image.to_edge(UP, buff=1)
        upsampled_image.scale_to_fit_width(2)
        text_1 = Tex(r"Bilinear Upsampling\\$224 \times 224$").scale(0.67)
        text_1.move_to(upsampled_image.get_top() + 0.2 * UP, aligned_edge=DOWN)
        up_1 = Group(upsampled_image, text_1)

        upsampled_image_2 = ImageMobject(
            "./images/attribution_map_layer_20_ERFUpsamplingFast.png"
        )
        upsampled_image_2.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
        upsampled_image_2.move_to(ORIGIN)
        upsampled_image_2.to_edge(DOWN, buff=0.5)
        upsampled_image_2.scale_to_fit_width(2)
        text_2 = Tex(
            r"Effective Receptive Field (ERF)\\Upsampling\\$224 \times 224$"
        ).scale(0.67)
        text_2.move_to(upsampled_image_2.get_top() + 0.2 * UP, aligned_edge=DOWN)
        up_2 = Group(upsampled_image_2, text_2)

        up = Group(up_1, up_2).arrange(DOWN, buff=1)
        up.move_to(ORIGIN).set_y(input_image.get_y())

        arrow_1 = Arrow(
            start=input_image.get_right() + 0.2 * RIGHT,
            end=upsampled_image.get_left() + 0.2 * LEFT,
            buff=0,
            color=WHITE,
            stroke_width=2,
        )
        arrow_2 = Arrow(
            start=input_image.get_right() + 0.2 * RIGHT,
            end=upsampled_image_2.get_left() + 0.2 * LEFT,
            buff=0,
            color=WHITE,
            stroke_width=2,
        )

        self.p.play([FadeIn(upsampled_image), GrowArrow(arrow_1), Write(text_1)])
        # self.wait(1)
        description_1 = (
            BulletedList(
                r"Fast and efficient", r"Introduces artifacts, loses fine details"
            )
            .scale(0.67)
            .next_to(upsampled_image, RIGHT, buff=0.5)
        )
        description_1.set_color_by_tex("Fast and efficient", GREEN)
        description_1.set_color_by_tex("Introduces artifacts, loses fine details", RED)

        description_2 = (
            BulletedList(
                r"Better preserves shapes/small details",
                r"More computationally expensive",
            )
            .scale(0.67)
            .next_to(upsampled_image_2, RIGHT, buff=0.5)
        )
        description_2.set_color_by_tex("Better preserves shapes/small details", GREEN)
        description_2.set_color_by_tex("More computationally expensive", RED)

        self.p.play(Write(description_1))
        self.p.next_slide()
        self.p.play([FadeIn(upsampled_image_2), GrowArrow(arrow_2), Write(text_2)])
        self.p.play(Write(description_2))
        self.p.next_slide()
        # self.wait(1)
