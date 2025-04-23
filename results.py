from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import right_angle_arrow_custom
# from light_theme import *


class Results(MySlide):
    def construct(self):
        title = Tex("VGG11 - Imagenettewoof Dataset").to_edge(UP, buff=1)
        # Load an svg
        svg = SVGMobject("./images/results_imagenettewoof_presentation.svg")
        svg.scale_to_fit_width(config.frame_width * 0.99).next_to(title, DOWN, buff=0.2)
        self.p.play(Write(title))
        self.p.play(DrawBorderThenFill(svg))
        self.p.next_slide()

        new_title = Tex("VGG11 - Synthetic Dataset").to_edge(UP, buff=1)
        # Load an svg
        svg2 = SVGMobject("./images/results_synthetic_presentation.svg")
        svg2.scale_to_fit_width(config.frame_width * 0.99).next_to(
            title, DOWN, buff=0.2
        )
        self.p.play(
            Transform(title, new_title, run_time=1.5), Transform(svg, svg2, run_time=2)
        )
        self.p.next_slide()

        # Fade out everything
        self.p.play(Unwrite(title), Uncreate(svg))
        self.p.next_slide()
