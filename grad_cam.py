from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from templates import SlideTemplate
from utils import right_angle_arrow_custom


class GradCAM(MySlide):
    def construct(self):
        # self.add_slide_template()
        # Input placeholder
        input_image = ImageMobject("./images/image.png")
        input_image.to_edge(LEFT, buff=0.5)
        input_image.to_edge(UP, buff=1.6)

        input_image_label = (
            Tex(r"Input Image\\$x$").scale(0.6).next_to(input_image, DOWN, buff=0.1)
        )

        self.p.play(FadeIn(input_image), Write(input_image_label))

        # CNN
        cnn = Rectangle(width=2, height=1).next_to(input_image, RIGHT, buff=1)
        cnn_text = Tex("CNN").scale(0.6).move_to(cnn.get_center())
        arrow_from_input = Arrow(
            input_image.get_right(), cnn.get_left(), buff=0.1, color=WHITE
        )
        self.p.play(Write(cnn), Write(cnn_text), GrowArrow(arrow_from_input))

        # Rectified conv
        single_layer = Polygon(
            *[
                [0, 0, 0],
                [0, 1, 0],
                [0.2, 1.2, 0],
                [0.2, 0.2, 0],
            ],
            fill_opacity=1,
            fill_color=BLACK,
            color=WHITE,
        )
        # Stack many single layers next to each other
        feature_map = VGroup([single_layer.copy() for _ in range(5)])
        feature_map.arrange(RIGHT, buff=-0.05).next_to(cnn, RIGHT, buff=2)

        feature_map_label = (
            Tex(r"Feature Map\\$A^\ell$").scale(0.6).next_to(feature_map, UP, buff=0.1)
        )
        arrow_from_cnn = Arrow(
            cnn.get_right(), feature_map.get_left(), buff=0.1, color=WHITE
        )
        # Draw the feature map
        self.p.play(
            Write(feature_map), Write(feature_map_label), GrowArrow(arrow_from_cnn)
        )

        # Raw class scores
        class_scores = (
            VGroup(
                *[
                    Rectangle(width=0.5, height=0.5, fill_opacity=1, fill_color=BLACK)
                    for _ in range(10)
                ]
            )
            .arrange(DOWN, buff=0)
            .next_to(feature_map, RIGHT, buff=3, aligned_edge=UP)
        )

        target_class = class_scores[-2]
        target_class.set_fill(WHITE, opacity=0.3)
        target_class_text = Tex("c").scale(0.6).move_to(target_class.get_center())
        target_class_label = (
            Tex("Target Class").scale(0.6).next_to(target_class, RIGHT, buff=0.1)
        )
        class_scores_label = (
            Tex(r"Raw Class\\Scores before\\Softmax")
            .scale(0.6)
            .next_to(class_scores, UP, buff=0.1)
            # .next_to(class_scores, DOWN, buff=0.1)
        )

        arrow_from_feature_map = Arrow(
            feature_map.get_right(),
            np.array([class_scores.get_left()[0], feature_map.get_right()[1], 0]),
            buff=0.1,
            color=WHITE,
        )

        # Draw the class scores
        self.p.play(
            Write(class_scores),
            Write(class_scores_label),
            GrowArrow(arrow_from_feature_map),
            Write(target_class_text),
            Write(target_class_label),
        )
        self.p.next_slide()

        # Backprop till conv
        feature_map_gradient = feature_map.copy()
        colors = [RED, GREEN, BLUE, PINK, ORANGE]
        for i, layer in enumerate(feature_map_gradient):
            layer.set_fill(colors[i], opacity=1)
            layer.set_color(colors[i])

        feature_map_gradient.next_to(target_class, LEFT, buff=3)

        arrow_from_target_class = Arrow(
            target_class.get_left(),
            feature_map_gradient.get_right(),
            buff=0.1,
            color=WHITE,
        )
        arrow_from_target_class_label = (
            Tex("Backpro till conv")
            .scale(0.6)
            .next_to(arrow_from_target_class, UP, buff=0.1)
        )
        feature_map_gradient_label = (
            Tex(r"Feature Map\\Gradient")
            .scale(0.6)
            .next_to(feature_map_gradient, DOWN, buff=0.1)
        )

        self.p.play(
            GrowArrow(arrow_from_target_class),
            Write(arrow_from_target_class_label),
            Create(feature_map_gradient),
            Write(feature_map_gradient_label),
        )

        # Avg pool of feature map gradient
        # Create 3 lines, from big to small from the top of the gradient

        avg_pool_lines = VGroup(
            Line(3 * LEFT, 3 * RIGHT, stroke_width=4, color=WHITE).shift(UP * 0),
            Line(2 * LEFT, 2 * RIGHT, stroke_width=4, color=WHITE).shift(UP * 1),
            Line(LEFT, RIGHT, stroke_width=4, color=WHITE).shift(UP * 2),
        )
        avg_pool_lines.scale_to_fit_width(feature_map_gradient.get_width())
        avg_pool_lines.next_to(feature_map_gradient, UP, buff=0.2)

        self.p.play(Create(avg_pool_lines))

        # Weights
        # For each activation layer create a square of the same color
        weights = VGroup(
            *[
                Rectangle(width=0.5, height=0.5, fill_opacity=1, fill_color=color)
                for i, color in enumerate(colors)
            ]
        ).arrange(RIGHT, buff=0)

        weights.next_to(avg_pool_lines, UP, buff=0.5)
        weights_labels = VGroup(
            *[
                Tex(f"$w_{i}^c$").scale(0.6).move_to(weights[i].get_center())
                for i in range(len(weights))
            ]
        )
        for i, label in enumerate(weights_labels):
            label.move_to(weights[i].get_center())

        layer_copies = VGroup()
        for i, layer in enumerate(feature_map_gradient):
            layer_copy = layer.copy()
            self.p.play(Transform(layer_copy, weights[i]))
            layer_copies.add(layer_copy)

        self.p.play(Write(weights_labels))

        self.p.next_slide()

        # Draw a line from each activation to the respective weight
        arrows_from_features_to_weights = VGroup(
            *[
                Arrow(
                    feature_map[i].get_bottom(),
                    weights[i].get_top(),
                    buff=0.1,
                    color=colors[i],
                )
                for i in range(len(weights))
            ]
        )

        self.p.play([GrowArrow(arr) for arr in arrows_from_features_to_weights])

        sum = Circle(radius=0.25, color=WHITE).next_to(weights, LEFT, buff=1)
        sum_label = Tex("+").scale(0.6).move_to(sum.get_center())
        sum_group = VGroup(sum, sum_label)

        arrows_from_weights_to_sum = VGroup(
            *[
                CurvedArrow(
                    weights[i].get_bottom(),
                    sum_group.get_bottom(),
                    color=colors[i],
                    angle=-PI / 2,
                )
                for i in range(len(weights))
            ]
        )

        self.p.play(
            [Create(arr) for arr in arrows_from_weights_to_sum] + [Write(sum_group)]
        )

        # ReLU block
        relu_block = Rectangle(width=1, height=0.5, fill_opacity=1, fill_color=BLACK)
        relu_block.next_to(sum_group, LEFT, buff=1)
        relu_block_text = Tex("ReLU").scale(0.6).move_to(relu_block.get_center())
        relu_block = VGroup(relu_block, relu_block_text)

        arrow_from_sum_to_relu = Arrow(
            sum_group.get_left(), relu_block.get_right(), buff=0.1, color=WHITE
        )
        self.p.play(Write(relu_block), GrowArrow(arrow_from_sum_to_relu))

        attribution_map = ImageMobject("./images/attribution_map_layer_20_overlay.png")
        attribution_map.next_to(input_image, DOWN, buff=1.5)

        attribution_map_label = (
            Tex(r"Attribution Map\\$\text{CAM}_c^\ell(x)$")
            .scale(0.6)
            .next_to(attribution_map, DOWN, buff=0.1)
        )

        arrow_from_relu_to_attribution_map = right_angle_arrow_custom(
            relu_block.get_bottom() + 0.1 * DOWN,
            attribution_map.get_right() + 0.3 * RIGHT,
            color=WHITE,
        )

        self.p.play(
            FadeIn(attribution_map),
            Write(attribution_map_label),
            Create(arrow_from_relu_to_attribution_map),
        )

        # Other CAM-Like methods
        cam_like_method = Tex(r"Other CAM-like\\methods").scale(0.6)

        rect = Rectangle(
            width=2.5, height=1.5, fill_opacity=0, fill_color=BLACK, stroke_width=2
        ).move_to(cam_like_method.get_center())

        cam_like_method_group = VGroup(cam_like_method, rect)
        cam_like_method_group.move_to(feature_map_gradient.get_center())

        arrow_from_target_class_to_cam_like_method = Arrow(
            target_class.get_left(),
            cam_like_method_group.get_right(),
            buff=0.1,
            color=WHITE,
        )

        arrows_from_cam_like_to_weights = VGroup(
            *[
                Arrow(
                    cam_like_method_group.get_top(),
                    weights[i].get_bottom(),
                    buff=0.1,
                    color=WHITE,
                    max_stroke_width_to_length_ratio=1,
                    max_tip_length_to_length_ratio=0.1,
                )
                for i in range(len(weights))
            ]
        )

        # avg_pool_lines.next_to(cam_like_method, UP, buff=0.2)

        to_add = VGroup(
            arrows_from_cam_like_to_weights,
            cam_like_method_group,
            arrow_from_target_class_to_cam_like_method,
        )

        to_remove = VGroup(
            arrow_from_target_class,
            arrow_from_target_class_label,
            feature_map_gradient,
            feature_map_gradient_label,
            avg_pool_lines,
        )

        self.p.next_slide()
        self.p.play(Circumscribe(weights), ReplacementTransform(to_remove, to_add))
        self.p.wait(1)

        other_cams = Tex(r"GradCAM++\\ScoreCAM\\LayerCAM").scale(0.6)
        other_cams_group = VGroup(other_cams, rect)

        to_add_2 = VGroup(
            arrows_from_cam_like_to_weights,
            other_cams_group,
            arrow_from_target_class_to_cam_like_method,
            # arrow_from_target_class_to_cam_like_method,
            # arrow_from_target_class,
        )

        other_cams.move_to(cam_like_method.get_center())
        self.p.next_slide()
        # self.remove(cam_like_method)
        self.p.play(ReplacementTransform(to_add, to_add_2))
        self.p.wait(1)
        self.p.next_slide()

        # Fade out everything
        self.p.play(
            FadeOut(input_image),
            FadeOut(input_image_label),
            FadeOut(cnn),
            FadeOut(cnn_text),
            FadeOut(arrow_from_input),
            FadeOut(feature_map),
            FadeOut(feature_map_label),
            FadeOut(arrow_from_cnn),
            FadeOut(class_scores),
            FadeOut(class_scores_label),
            FadeOut(target_class),
            FadeOut(target_class_text),
            FadeOut(target_class_label),
            FadeOut(arrow_from_feature_map),
            FadeOut(feature_map_gradient_label),
            FadeOut(avg_pool_lines),
            FadeOut(weights_labels),
            FadeOut(weights),
            # FadeOut(sum_label),
            # FadeOut(sum_group),
            FadeOut(relu_block),
            FadeOut(relu_block_text),
            FadeOut(arrow_from_sum_to_relu),
            FadeOut(attribution_map),
            FadeOut(attribution_map_label),
            FadeOut(arrow_from_relu_to_attribution_map),
            FadeOut(arrows_from_weights_to_sum),
            FadeOut(weights),
            FadeOut(layer_copies),
            # FadeOut(to_remove),
            # FadeOut(to_add),
            FadeOut(to_add_2),
            FadeOut(sum_group),
            # FadeOut(arrow_from_target_class_to_cam_like_method),
            # FadeOut(cam_like_method_group),
            # FadeOut(arrow_from_target_class),
            FadeOut(arrows_from_cam_like_to_weights),
            # FadeOut(other_cams),
            FadeOut(rect),
            FadeOut(cam_like_method),
            *[FadeOut(arr) for arr in arrows_from_features_to_weights],
        )

        # self.p.remove(to_remove, to_add, to_add_2)
        # self.p.wait(2)
