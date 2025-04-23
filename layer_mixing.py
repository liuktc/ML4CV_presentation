from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide


class LayerMixing(MySlide):
    def construct(self):
        lower_level = ImageMobject("image.jpeg")
        lower_level.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        lower_level.scale_to_fit_width(4)

        lower_level_text = Tex(
            r"Low-Level Attribution Map\\$224 \times 224$ (Upsampled)"
        ).scale(0.67)
        lower_level_text.move_to(lower_level.get_top() + 0.2 * UP, aligned_edge=DOWN)

        lower_level_group = Group(lower_level, lower_level_text)

        high_level = ImageMobject("image.jpeg")
        high_level.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        high_level.scale_to_fit_width(4)

        high_level_text = Tex(
            r"High-Level Attribution Map\\$224 \times 224$ (Upsampled)"
        ).scale(0.67)
        high_level_text.move_to(high_level.get_top() + 0.2 * UP, aligned_edge=DOWN)

        high_level_group = Group(high_level, high_level_text)

        high_level_group.next_to(lower_level_group, RIGHT, buff=1.5)

        lower_high_level_group = Group(lower_level_group, high_level_group)
        lower_high_level_group.move_to(ORIGIN)

        self.p.play([FadeIn(lower_level), Write(lower_level_text)])
        self.p.next_slide()

        self.p.play([FadeIn(high_level), Write(high_level_text)])
        self.p.next_slide()

        self.p.play(Circumscribe(lower_level_group, color=YELLOW))
        self.p.play(Circumscribe(high_level_group, color=YELLOW))

        self.p.next_slide()

        mixed_level = ImageMobject("image.jpeg")
        mixed_level.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        mixed_level.scale_to_fit_width(4)

        mixed_level_text = Tex(r"Mixed Attribution Map\\$224 \times 224$").scale(0.67)
        mixed_level_text.move_to(mixed_level.get_top() + 0.2 * UP, aligned_edge=DOWN)

        mixed_level_group = Group(mixed_level, mixed_level_text)

        # lower_high_level_group.add(mixed_level_group)

        self.p.play(
            [
                lower_high_level_group.animate.scale(0.8).to_edge(LEFT, buff=0.5),
                # Write(odot_text),
            ]
        )

        odot_text = (
            MathTex(r"\odot")
            .scale(1)
            .move_to((lower_level.get_center() + high_level.get_center()) * 0.5)
        )

        self.p.play(Write(odot_text))

        mixed_level_group.scale(0.8).next_to(lower_high_level_group, RIGHT, buff=1.5)

        equal_text = MathTex(r"=").move_to(odot_text.get_center()).scale(1)
        equal_text.move_to((high_level.get_center() + mixed_level.get_center()) * 0.5)

        self.p.play([FadeIn(mixed_level), Write(mixed_level_text), Write(equal_text)])
        self.p.next_slide()

        # Fade out everything
        self.p.play(
            [
                FadeOut(lower_high_level_group),
                FadeOut(odot_text),
                FadeOut(equal_text),
                FadeOut(mixed_level_group),
            ]
        )
