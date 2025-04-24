from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners
from vgg_model import VGG11_LAYERS, VGGModel
from templates import SlideTemplate
from utils import right_angle_arrow_custom
# from light_theme import *

from settings import *


def arrow_with_fixed_tip_and_stroke(start, end, tip_length=0.2, stroke_width=4):
    """Creates an arrow with a fixed tip length and stroke width."""
    # Create the arrow
    arrow = Arrow(start, end, max_tip_length_to_length_ratio=tip_length, buff=0.1)
    arrow.set_stroke(width=stroke_width)

    # Adjust the tip length
    arrow.tip.scale(tip_length / arrow.tip.get_height())

    return arrow


class MixingArchitecture(MySlide):
    def construct(self):
        # self.add_slide_template()
        # Add an input image
        input_image = ImageMobject("./images/image_16.png").scale(0.6)
        input_image.to_edge(LEFT, buff=0.5)
        input_image.shift(0.3 * DOWN)
        input_image_label = Tex("Input Image").scale(0.6)
        input_image_label.next_to(input_image, UP, buff=0.1)
        self.p.play([FadeIn(input_image), Write(input_image_label)])

        # Create the VGG architecture diagram
        model = VGGModel(self.p)
        model.construct()

        vgg_model = model.vgg_model
        vgg_model.scale_to_fit_width(config.frame_width * 0.3)
        vgg_model.next_to(input_image, buff=0.3)

        arrow_from_input_to_model = Arrow(
            input_image.get_right(),
            np.array([model.layer_group.get_left()[0], input_image.get_right()[1], 0]),
            buff=0.1,
            color=WHITE,
        )
        self.p.play(GrowArrow(arrow_from_input_to_model))
        model.display(hide_legend=True)

        cams = []
        for _ in range(4):
            rect = Rectangle(width=1.5, height=1.5, color=YELLOW, fill_opacity=0.3)
            text = Tex(r"Attr.\\Method").scale_to_fit_width(rect.get_width() * 0.8)
            text.move_to(rect.get_center())
            cams.append(VGroup(rect, text))
        cams_group = Group(*cams)
        cams_group.arrange(DOWN, buff=0.5)
        cams_group.next_to(vgg_model, RIGHT, buff=0.5)

        attribution_maps = [
            ImageMobject(
                f"./images/attribution_map_layer_{i}_16.png"
            ).scale_to_fit_width(2)
            for i in [20, 15, 10, 5]
        ]
        attribution_maps_group = Group(*attribution_maps)
        # attribution_maps_group.arrange(DOWN, buff=0.5)
        # attribution_maps_group.next_to(cams_group, RIGHT, buff=1)

        # self.p.play(FadeIn(attribution_maps_group))

        grid = []
        for i in range(4):
            grid.append(cams[i])
            grid.append(attribution_maps[i])
        grid = Group(*grid).arrange_in_grid(cols=2, rows=4, buff=(2, 0.5))
        grid.scale_to_fit_height(config.frame_height * 0.7)
        grid.next_to(vgg_model, RIGHT, buff=1)

        attribution_maps_text = (
            Tex(r"Upsampled\\Attribution Maps")
            .scale(0.6)
            .move_to(attribution_maps_group.get_center())
            .next_to(attribution_maps_group, UP, buff=0.1)
        )
        self.p.play(Write(attribution_maps_text))

        pool_layers = model.pool_layers
        arrows_pool = []
        for i in range(4):
            arrow_1 = right_angle_arrow_custom(
                (
                    pool_layers[i].get_top() + 0.2 * UP
                    if i <= 1
                    else pool_layers[i].get_bottom() + 0.2 * DOWN
                ),
                cams[i].get_left() + 0.2 * LEFT,
            )
            self.p.play([Create(arrow_1), Write(cams[i])])

            arrow_2 = Arrow(
                cams[i].get_right(), attribution_maps[i].get_left(), buff=0.1
            )
            self.p.play([Create(arrow_2), FadeIn(attribution_maps[i])])
            arrows_pool.append(arrow_1)
            arrows_pool.append(arrow_2)

        self.p.next_slide()
        dashed_line = (
            DashedLine(UP, DOWN, color=WHITE, stroke_width=2)
            .scale_to_fit_height(config.frame_height * 0.7)
            .next_to(grid, RIGHT, buff=0.5)
        )
        self.p.play(Create(dashed_line, run_time=0.3))

        mixed_attribution_maps = [
            ImageMobject(
                f"./images/mixed_attribution_map_layer_{i}_16.png"
            ).scale_to_fit_width(2)
            for i in [20, 15, 10, 5]
        ]
        mixed_attribution_maps_group = Group(*mixed_attribution_maps)
        mixed_attribution_maps_group.arrange(DOWN, buff=0.5)
        mixed_attribution_maps_group.next_to(dashed_line, RIGHT, buff=0.5)
        mixed_attribution_maps_group.scale_to_fit_height(config.frame_height * 0.7)

        mixed_attribution_maps_text = (
            Tex(r"HighResCAM")
            .scale(0.6)
            .move_to(mixed_attribution_maps_group.get_center())
            .next_to(mixed_attribution_maps_group, UP, buff=0.1)
        )
        self.p.play(Write(mixed_attribution_maps_text))

        # self.p.play(FadeIn(mixed_attribution_maps_group))
        attr_to_remove = []
        for i in range(4):
            attribution_maps_to_mix = attribution_maps[: i + 1]
            attribution_maps_to_mix = [attr.copy() for attr in attribution_maps_to_mix]
            attr_to_remove.extend(attribution_maps_to_mix)

            arrows = [
                arrow_with_fixed_tip_and_stroke(
                    attr.get_right(),
                    mixed_attribution_maps[i].get_left(),
                    # max_tip_length_to_length_ratio=0.1,
                )
                for attr in attribution_maps_to_mix
            ]
            arrows_pool.extend(arrows)

            self.p.play([Circumscribe(attr) for attr in attribution_maps_to_mix])

            self.p.play(
                [
                    attribution_maps_to_mix[j].animate.move_to(
                        mixed_attribution_maps[i].get_center()
                    )
                    for j in range(i + 1)
                ]
                + [GrowArrow(arrow) for arrow in arrows]
                + [FadeIn(mixed_attribution_maps[i], shift=UP)]
            )
            self.p.next_slide()

        # Fade out everything
        to_fade_out = (
            [
                input_image,
                input_image_label,
                vgg_model,
                arrow_from_input_to_model,
                dashed_line,
                attribution_maps_group,
                attribution_maps_text,
                mixed_attribution_maps_group,
                mixed_attribution_maps_text,
                cams_group,
                # *cams,
                # *attribution_maps,
            ]
            + attribution_maps
            + mixed_attribution_maps
            + arrows_pool
            + attr_to_remove
        )
        self.p.play(
            FadeOut(
                *to_fade_out,
            )
        )
