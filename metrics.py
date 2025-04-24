from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import right_angle_arrow_custom

# from light_theme import *
from templates import SlideTemplate

from settings import *


class AvgDrop_ROAD(MySlide):
    def construct(self):
        average_drop_title = Tex(r"Average Drop").scale(1).to_edge(UP, buff=1)
        self.p.play(Write(average_drop_title))
        input_image = ImageMobject("./images/image.png")
        input_image.to_edge(LEFT, buff=0.5)
        input_image.to_edge(UP, buff=2)

        cnn = Rectangle(width=1, height=1).set_fill(WHITE, opacity=0.5)
        cnn_text = (
            Text("CNN").move_to(cnn.get_center()).scale_to_fit_width(cnn.width * 0.8)
        )
        cnn = VGroup(cnn, cnn_text).next_to(input_image, RIGHT, buff=3)

        arrow_from_input = Arrow(
            start=input_image.get_right(), end=cnn.get_left(), buff=0.1
        )

        self.p.play(FadeIn(input_image), Create(cnn), Create(arrow_from_input))

        class_confidence = MathTex(r"y_c = 0.99").next_to(cnn, RIGHT, buff=1)
        class_confidence_label = (
            Text("Class confidence").scale(0.5).next_to(class_confidence, UP, buff=0.2)
        )

        arrow_from_cnn = Arrow(
            start=cnn.get_right(), end=class_confidence.get_left(), buff=0.1
        )
        self.p.play(
            Create(arrow_from_cnn),
            FadeIn(class_confidence_label),
            Write(class_confidence),
        )

        input_image_2 = input_image.copy()
        # input_image_2.next_to(input_image, DOWN, buff=3)

        attribution_map = ImageMobject("./images/attribution_map_layer_20.png")

        odot = MathTex(r"\odot").scale(1)

        combination = (
            Group(input_image_2, odot, attribution_map)
            .arrange(RIGHT, buff=0.1)
            .next_to(input_image, DOWN, buff=1.5, aligned_edge=LEFT)
        )

        cnn_2 = cnn.copy()
        cnn_2.next_to(combination, RIGHT, buff=1)

        # x-aling the 2 cnn
        cnn_2.set_x(cnn.get_x())

        arrow_from_input_2 = Arrow(
            start=combination.get_right(), end=cnn_2.get_left(), buff=0.1
        )

        self.p.play(FadeIn(combination), Create(cnn_2), Create(arrow_from_input_2))

        class_confidence_2 = MathTex(r"y'_c = 0.50").next_to(cnn_2, RIGHT, buff=1)
        class_confidence_label_2 = (
            Tex(r"Class confidence\\after masking")
            .scale(0.6)
            .next_to(class_confidence_2, UP, buff=0.2)
        )

        arrow_from_cnn_2 = Arrow(
            start=cnn_2.get_right(), end=class_confidence_2.get_left(), buff=0.1
        )
        self.p.play(
            Create(arrow_from_cnn_2),
            FadeIn(class_confidence_label_2),
            Write(class_confidence_2),
        )

        minus = Circle(radius=0.2, color=WHITE).set_fill(WHITE, opacity=0.3)
        minus_text = (
            Tex("-").move_to(minus.get_center()).scale_to_fit_width(minus.width * 0.6)
        )
        minus = (
            VGroup(minus, minus_text)
            .to_edge(RIGHT, buff=4)
            .set_y((input_image.get_y() + input_image_2.get_y()) / 2)
        )

        arrow_from_class_1_to_minus = right_angle_arrow_custom(
            start=class_confidence.get_right() + 0.1 * RIGHT,
            end=minus.get_top() + 0.1 * UP,
            horizontal_first=True,
            aligned_edge=DOWN,
        )

        arrow_from_class_2_to_minus = right_angle_arrow_custom(
            start=class_confidence_2.get_right() + 0.1 * RIGHT,
            end=minus.get_bottom() + 0.1 * DOWN,
            horizontal_first=True,
            aligned_edge=UP,
        )
        self.p.next_slide()
        self.p.play(
            Write(minus),
            Create(arrow_from_class_1_to_minus),
            Create(arrow_from_class_2_to_minus),
        )

        average_drop = (
            Tex(r"Average Drop\\$y_c - y'_c = 0.49$")
            .scale(0.8)
            .next_to(minus, RIGHT, buff=1)
        )
        arrow_from_minus = Arrow(
            start=minus.get_right(), end=average_drop.get_left(), buff=0.1
        )

        self.p.play(
            Create(arrow_from_minus),
            FadeIn(average_drop),
        )
        self.p.next_slide()

        ##################################
        formulas = [
            Tex(r"ROAD"),
            Tex(r"(", font_size=80),
            Tex(r",", font_size=80),
            Tex(r")", font_size=80),
        ]
        new_combination = Group(
            formulas[0],
            formulas[1],
            input_image_2.copy(),
            formulas[2],
            attribution_map.copy(),
            formulas[3],
        )
        new_combination.arrange(RIGHT, buff=0.1).move_to(
            combination.get_center()
        ).scale_to_fit_width(combination.width)

        road = Tex(r"ROAD Score\\$y_c - y'_c = 0.3$").move_to(average_drop.get_center())
        road_title = Tex(r"ROAD").scale(0.8).to_edge(UP, buff=1)

        new_class_confidence_2 = (
            MathTex(r"y'_c = 0.69").move_to(class_confidence_2.get_center()).scale(0.8)
        )
        # self.p.play(Transform(combination, new_combination))
        self.p.play(Indicate(combination))
        self.p.next_slide()
        self.p.play(FadeOut(combination))
        self.p.play(
            FadeIn(new_combination),
            Transform(average_drop, road),
            Transform(class_confidence_2, new_class_confidence_2),
            Transform(average_drop_title, road_title),
        )

        self.p.next_slide()
        # Fade out everything
        self.p.play(
            FadeOut(new_combination),
            FadeOut(road),
            FadeOut(road_title),
            FadeOut(cnn),
            FadeOut(cnn_2),
            FadeOut(input_image),
            # FadeOut(input_image_2),
            # FadeOut(attribution_map),
            FadeOut(class_confidence_label),
            FadeOut(class_confidence_label_2),
            FadeOut(class_confidence),
            FadeOut(class_confidence_2),
            FadeOut(minus),
            FadeOut(arrow_from_input_2),
            FadeOut(arrow_from_cnn_2),
            FadeOut(arrow_from_input),
            FadeOut(arrow_from_cnn),
            FadeOut(arrow_from_class_1_to_minus),
            FadeOut(arrow_from_class_2_to_minus),
            FadeOut(arrow_from_minus),
            FadeOut(average_drop),
            FadeOut(average_drop_title),
        )


class Coherency(MySlide):
    def construct(self):
        coherency_title = Tex(r"Coherency").scale(1).to_edge(UP, buff=1)
        self.p.play(Write(coherency_title))
        input_image = ImageMobject("./images/image.png")
        input_image.to_edge(LEFT, buff=0.5)
        input_image.to_edge(UP, buff=2)

        cam = Rectangle(width=1, height=1, color=YELLOW).set_fill(YELLOW, opacity=0.5)
        cam_text = (
            Text("CAM").move_to(cam.get_center()).scale_to_fit_width(cam.width * 0.8)
        )
        cam = VGroup(cam, cam_text).next_to(input_image, RIGHT, buff=3)

        arrow_from_input = Arrow(
            start=input_image.get_right(), end=cam.get_left(), buff=0.1
        )

        self.p.play(FadeIn(input_image), Create(cam), Create(arrow_from_input))

        attribution_1 = ImageMobject("./images/attribution_map_layer_20.png")
        attribution_1.next_to(cam, RIGHT, buff=1)

        arrow_from_cam_1 = Arrow(
            start=cam.get_right(), end=attribution_1.get_left(), buff=0.1
        )
        self.p.play(Create(arrow_from_cam_1), FadeIn(attribution_1))

        input_image_2 = input_image.copy()
        input_image_2.next_to(input_image, DOWN, buff=3)

        attribution_map_2 = ImageMobject("./images/attribution_map_layer_20.png")

        odot = MathTex(r"\odot").scale(1)

        combination = (
            Group(input_image_2, odot, attribution_map_2)
            .arrange(RIGHT, buff=0.1)
            .next_to(input_image, DOWN, buff=1.5, aligned_edge=LEFT)
        )

        cam_2 = cam.copy()
        cam_2.next_to(combination, RIGHT, buff=1)

        # x-aling the 2 cam
        cam_2.set_x(cam.get_x())

        arrow_from_input_2 = Arrow(
            start=combination.get_right(), end=cam_2.get_left(), buff=0.1
        )

        arrow_from_attribution_map_1_to_2 = Arrow(
            attribution_1.get_bottom(), attribution_map_2.get_top(), buff=0.1
        )

        self.p.play(GrowArrow(arrow_from_attribution_map_1_to_2), FadeIn(combination))
        self.p.play(Create(cam_2), Create(arrow_from_input_2))

        # attr = ImageMobject("./images/attribution_map_layer_20.png")
        # np.random.seed(0)
        # noise = np.random.normal(0, 0.1, size=attr.get_pixel_array().shape)
        # img = np.clip(attr.get_pixel_array() + noise, 0, 1)
        # img = attr.get_pixel_array() + noise
        attribution_map_3 = ImageMobject("./images/attribution_map_layer_20.png")
        # Add some noise to the attribution map
        # attribution_map_3.get_pixel_array()
        attribution_map_3.next_to(cam_2, RIGHT, buff=1)
        attribution_map_3.set_x(attribution_1.get_x())
        arrow_from_cam_2 = Arrow(
            start=cam_2.get_right(), end=attribution_map_3.get_left(), buff=0.1
        )
        self.p.play(Create(arrow_from_cam_2), FadeIn(attribution_map_3))

        pearson = (
            Tex(r"Pearson\\Correlation")
            .scale(0.8)
            .to_edge(RIGHT, buff=3)
            .set_y((input_image.get_y() + input_image_2.get_y()) / 2)
        )

        arrow_from_class_1_to_pearson = right_angle_arrow_custom(
            start=attribution_1.get_right() + 0.1 * RIGHT,
            end=pearson.get_top() + 0.1 * UP,
            horizontal_first=True,
            aligned_edge=DOWN,
        )

        arrow_from_class_2_to_pearson = right_angle_arrow_custom(
            start=attribution_map_3.get_right() + 0.1 * RIGHT,
            end=pearson.get_bottom() + 0.1 * DOWN,
            horizontal_first=True,
            aligned_edge=UP,
        )
        self.p.next_slide()
        self.p.play(
            Write(pearson),
            Create(arrow_from_class_1_to_pearson),
            Create(arrow_from_class_2_to_pearson),
        )

        coherency = Tex(r"Coherency").scale(0.8).next_to(pearson, RIGHT, buff=1)
        arrow_from_pearson = Arrow(
            start=pearson.get_right(), end=coherency.get_left(), buff=0.1
        )
        self.p.play(
            Create(arrow_from_pearson),
            FadeIn(coherency),
        )
        self.p.next_slide()
        # Fade out everything
        self.p.play(
            FadeOut(coherency),
            FadeOut(pearson),
            FadeOut(cam),
            FadeOut(cam_2),
            FadeOut(input_image),
            FadeOut(attribution_1),
            FadeOut(attribution_map_3),
            FadeOut(attribution_map_2),
            FadeOut(arrow_from_input_2),
            FadeOut(arrow_from_cam_2),
            FadeOut(arrow_from_input),
            FadeOut(arrow_from_cam_1),
            FadeOut(arrow_from_class_1_to_pearson),
            FadeOut(arrow_from_class_2_to_pearson),
            FadeOut(arrow_from_pearson),
            FadeOut(coherency_title),
            FadeOut(odot),
            FadeOut(input_image_2),
            FadeOut(arrow_from_attribution_map_1_to_2),
        )


class Complexity(MySlide):
    def construct(self):
        complexity_title = Tex(r"Complexity").scale(1).to_edge(UP, buff=1)
        self.p.play(Write(complexity_title))
        input_image = ImageMobject("./images/image.png")
        input_image.to_edge(LEFT, buff=0.5)

        cam = Rectangle(width=1, height=1, color=YELLOW).set_fill(YELLOW, opacity=0.5)
        cam_text = (
            Text("CAM").move_to(cam.get_center()).scale_to_fit_width(cam.width * 0.8)
        )
        cam = VGroup(cam, cam_text).next_to(input_image, RIGHT, buff=1)

        cam.set_y(input_image.get_y())
        arrow_from_input = Arrow(
            start=input_image.get_right(), end=cam.get_left(), buff=0.1
        )
        self.p.play(FadeIn(input_image), Create(cam), Create(arrow_from_input))

        attribution_map = ImageMobject("./images/attribution_map_layer_20.png")
        attribution_map.next_to(cam, RIGHT, buff=1)

        arrow_from_cam = Arrow(
            start=cam.get_right(), end=attribution_map.get_left(), buff=0.1
        )
        self.p.play(Create(arrow_from_cam), FadeIn(attribution_map))

        flatten = Tex(r"Flatten").scale(0.8).next_to(attribution_map, RIGHT, buff=1)
        flatten.next_to(attribution_map, buff=0.5)

        arrow_from_attribution_map = Arrow(
            start=attribution_map.get_right(), end=flatten.get_left(), buff=0.1
        )
        self.p.play(Create(arrow_from_attribution_map), FadeIn(flatten))

        norm_1 = MathTex(r"\| \cdot \|_1").scale(1.2).next_to(flatten, RIGHT, buff=1)
        norm_1.next_to(flatten, buff=0.5)

        arrow_from_flatten = Arrow(
            start=flatten.get_right(), end=norm_1.get_left(), buff=0.1
        )

        self.p.play(Create(arrow_from_flatten), FadeIn(norm_1))

        complexity = Tex(r"Complexity").scale(0.8).next_to(norm_1, RIGHT, buff=1)
        arrow_from_norm_1 = Arrow(
            start=norm_1.get_right(), end=complexity.get_left(), buff=0.1
        )
        self.p.play(
            Create(arrow_from_norm_1),
            FadeIn(complexity),
        )
        self.p.next_slide()
        # Fade out everything
        self.p.play(
            FadeOut(complexity),
            FadeOut(cam),
            FadeOut(input_image),
            FadeOut(attribution_map),
            FadeOut(flatten),
            FadeOut(norm_1),
            FadeOut(arrow_from_input),
            FadeOut(arrow_from_cam),
            FadeOut(arrow_from_attribution_map),
            FadeOut(arrow_from_flatten),
            FadeOut(arrow_from_norm_1),
            FadeOut(complexity_title),
        )


class CompositeMetrics(MySlide):
    def construct(self):
        title = Tex(r"Composite Metrics").scale(1).to_edge(UP, buff=1)
        self.p.play(Write(title))
        adcc = MathTex(
            r"\text{ADCC}",
            r"= 3 \cdot \left(",
            r"\frac{1}{1 - \text{AverageDrop}}",
            r"+ \frac{1}{1 - \text{Complexity}}",
            r"+ \frac{1}{\text{Coherency}} \right)^{-1}",
        )
        adcc[0].set_color(YELLOW)
        adcc.scale(0.8).next_to(title, DOWN, buff=1)

        rect = SurroundingRectangle(adcc[2], color=YELLOW, buff=0.1, fill_opacity=0.1)

        self.p.play(Write(adcc))
        self.p.next_slide()
        self.p.play(Create(rect))

        arcc = MathTex(
            r"\text{ARCC}",
            r" = 3 \cdot \left(",
            r"\frac{1}{\text{ROADScore}}",
            r"+ \frac{1}{1 - \text{Complexity}}",
            r"+ \frac{1}{\text{Coherency}} \right)^{-1}",
        )
        arcc[0].set_color(BLUE)

        arcc.scale(0.8).next_to(adcc, DOWN, buff=1)
        rect_2 = SurroundingRectangle(arcc[2], color=BLUE, buff=0.1, fill_opacity=0.1)
        self.p.play(TransformMatchingTex(adcc.copy(), arcc), Create(rect_2))
        self.p.next_slide()

        # Fade out everything
        self.p.play(
            FadeOut(title),
            FadeOut(adcc),
            FadeOut(arcc),
            FadeOut(rect),
            FadeOut(rect_2),
        )
