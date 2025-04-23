from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners
import math
from templates import SlideTemplate


class ERF(MySlide):
    def construct(self):
        np.random.seed(0)  # For reproducibility

        formula = Tex(
            r"The Effective Receptive Field (ERF) for a single activation $a_{i,j}^{\ell}$ at layer $\ell$ is defined as: \[ \text{ERF}(a_{i,j}^{\ell}) = \frac{\partial a_{i,j}^{\ell}}{\partial x}\]"
        )
        formula.scale(0.67)
        formula.to_edge(UP, buff=1)
        self.p.play(Write(formula))
        # input_image = ImageMobject(np.uint8(np.random.rand(28, 28, 1) * 255))
        # input_image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        # input_image.scale_to_fit_width(3)
        # input_image.to_edge(LEFT, buff=0.2)

        feature_map = ImageMobject(
            "./images/attribution_map_layer_20_bilinearUpsampling_small.png"
        )
        feature_map.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        feature_map.scale_to_fit_width(2.5)
        # feature_map.next_to(formula, DOWN, buff=0.5)

        erf = ImageMobject(np.uint8(np.random.rand(224, 224, 1) * 255))
        erf.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        erf.scale_to_fit_width(2.5)

        images_group = Group(feature_map, erf)
        images_group.arrange_in_grid(n_rows=1, n_cols=2, buff=1)
        images_group.next_to(formula, DOWN, buff=0.8)

        # self.p.play([FadeIn(erf)])
        # feature_map.next_to(input_image, RIGHT, buff=0.5)

        # images_group = Group(input_image, feature_map)
        # images_group.move_to(ORIGIN)

        # text_input = Tex("Input Image").scale(0.6)
        # text_input.move_to(input_image.get_top() + 0.2 * UP)
        text_feature_map = Tex(r"Attribution Map\\").scale(0.6)
        # text_feature_map.move_to(feature_map.get_top() + 0.2 * UP)
        text_feature_map.add_updater(lambda m: m.next_to(feature_map, UP, buff=0.2))

        # self.p.play([FadeIn(input_image), Write(text_input)])
        self.p.play([FadeIn(feature_map), Write(text_feature_map)])

        # image_pixels = 2
        # pixel_size = input_image.width / image_pixels
        # small_square_image = Square(side_length=pixel_size, fill_opacity=0.5)

        feature_map_pixels = 7
        feature_map_pixel_size = feature_map.width / feature_map_pixels
        small_square_feature_map = Square(
            side_length=feature_map_pixel_size, fill_opacity=0.5
        )
        small_square_feature_map.set_color(YELLOW)

        upper_left_corner_feature_map = np.array(
            [
                feature_map.get_left()[0] + feature_map_pixel_size / 2,
                feature_map.get_top()[1] - feature_map_pixel_size / 2,
                0,
            ]
        )
        small_square_feature_map.move_to(upper_left_corner_feature_map)
        self.p.play(Create(small_square_feature_map))

        feature_map_i, feature_map_j = ValueTracker(), ValueTracker()

        feature_map_text = MathTex(
            f"a_{{{round(feature_map_i.get_value())},{round(feature_map_j.get_value())}}}"
        )
        feature_map_text.add_updater(lambda m: m.next_to(feature_map, DOWN, buff=0.2))
        feature_map_text.set_color(YELLOW)

        def update_text(text: MathTex):
            text_copy = MathTex(
                f"a_{{{round(feature_map_i.get_value())},{round(feature_map_j.get_value())}}}"
            )
            text_copy.move_to(text.get_center())
            text_copy.set_color(YELLOW)
            text_copy.set_opacity(0.5)

            text.become(text_copy)  # Update the text with the new value

        feature_map_text.add_updater(
            lambda m: update_text(m)  # Update the text with the current i and j values
        )
        self.p.play(Write(feature_map_text))

        def update_square(square: Square):
            upper_left_corner_feature_map = np.array(
                [
                    feature_map.get_left()[0] + feature_map_pixel_size / 2,
                    feature_map.get_top()[1] - feature_map_pixel_size / 2,
                    -1,
                ]
            )
            self.p.bring_to_front(square)
            square.move_to(
                upper_left_corner_feature_map
                + DOWN * feature_map_i.get_value() * feature_map_pixel_size
                + RIGHT * feature_map_j.get_value() * feature_map_pixel_size
            )

        small_square_feature_map.add_updater(
            lambda m: update_square(
                m
            )  # Update the square with the current i and j values
        )

        # small_square_image_corners = get_square_corners(small_square_image)
        # small_square_feature_map_corners = get_square_corners(small_square_feature_map)

        def update_erf(erf: ImageMobject):
            i = round(feature_map_i.get_value())
            j = round(feature_map_j.get_value())

            new_erf = ImageMobject(f"./images/erf_{i}_{j}.png")
            new_erf.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            new_erf.scale_to_fit_width(2.5)
            new_erf.move_to(erf.get_center())
            erf.become(new_erf)

        erf.add_updater(lambda m: update_erf(m))
        erf_text = MathTex(r"\text{ERF}(a_{0,0})").scale(0.6)

        def update_erf_text(erf_text: MathTex):
            i = round(feature_map_i.get_value())
            j = round(feature_map_j.get_value())
            new_erf_text = (
                MathTex(r"\text{ERF}(", f"a_{{{i},{j}}}", ")")
                .scale(0.6)
                .set_color(WHITE)
            )
            new_erf_text.move_to(erf_text.get_center())
            # new_erf_text.set_color(RED)
            new_erf_text[1].set_color(YELLOW)
            # new_erf_text.set_opacity(0.5)

            erf_text.become(new_erf_text)

        # erf_text.move_to(erf.get_top() + 0.2 * UP)
        erf_text.add_updater(lambda m: m.next_to(erf, UP, buff=0.2))
        erf_text.add_updater(
            lambda m: update_erf_text(
                m
            )  # Update the text with the current i and j values
        )

        self.p.add(erf)
        self.p.play([Write(erf_text)])
        self.p.next_slide(loop=True)

        for i in range(7):
            for j in range(7):
                if j == 0:
                    feature_map_i.set_value(i)
                    feature_map_j.set_value(j)
                else:
                    # self.p.play(input_i.animate.set_value(i), input_j.animate.set_value(j))
                    self.p.play(
                        feature_map_i.animate.set_value(i),
                        feature_map_j.animate.set_value(j),
                    )

        # Sum of attributions
        sums = ImageMobject("./images/erf_0_0.png").scale_to_fit_width(2.5)
        sums_text = MathTex(r"\text{ERF-CAM}_c^\ell").scale(0.6)
        sums_text.add_updater(
            lambda m: m.next_to(
                sums, UP, buff=0.2
            )  # Update the text with the new value
        )
        sums_group = Group(sums, sums_text)

        images_group.add(sums)
        sums.next_to(erf, RIGHT, buff=0.5)
        # images_group.arrange(RIGHT, buff=1)
        self.p.next_slide()

        sums_formula = MathTex(
            r"\text{ERF-CAM}_c^\ell = \sum_{i,j} \text{ERF}(a_{i,j}^{\ell}) \cdot \text{CAM}_c^\ell(i,j)"
        )
        sums_formula.scale(0.6).to_edge(DOWN, buff=0.5)
        self.p.play(
            images_group.animate.arrange(RIGHT, buff=1).set_y(images_group.get_y()),
            Write(sums_text),
            Write(sums_formula),
        )
        self.p.next_slide()

        for i in range(7):
            for j in range(7):
                # self.p.play(input_i.animate.set_value(i), input_j.animate.set_value(j))
                if j == 0:
                    # self.p.play(
                    feature_map_i.set_value(i)
                    feature_map_j.set_value(j)
                    # run_time=0.2,
                # )
                else:
                    self.p.play(
                        feature_map_i.animate.set_value(i),
                        feature_map_j.animate.set_value(j),
                        run_time=0.2,
                    )
                # self.p.play(
                #     feature_map_i.animate.set_value(i),
                #     feature_map_j.animate.set_value(j),
                # )
                new_sums = ImageMobject(f"./images/erf_sum_{i}_{j}.png")

                new_sums.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
                new_sums.scale_to_fit_width(2.5)
                new_sums.move_to(sums.get_center())
                sums.become(new_sums)
        self.p.next_slide()
        # Fade out everything
        self.p.remove(small_square_feature_map, erf_text, feature_map_text)
        self.p.play(
            FadeOut(feature_map),
            # FadeOut(feature_map_text),
            # FadeOut(small_square_feature_map),
            FadeOut(erf),
            # FadeOut(erf_text),
            FadeOut(sums_formula),
            FadeOut(images_group),
            FadeOut(sums_text),
            FadeOut(sums),
            FadeOut(formula),
            FadeOut(text_feature_map),
        )
