import numpy as np
from my_scene import MySlide
from manim import *
from templates import SlideTemplate

from settings import *


class QualitativeResults(MySlide):
    def construct(self):
        # self.add_slide_template()
        image_1 = ImageMobject(
            "./images/qualitativi_imagenettewoof_dark.png"
        ).scale_to_fit_width(config.frame_width * 0.4)
        image_2 = ImageMobject(
            "./images/qualitativi_synthetic_dark.png"
        ).scale_to_fit_width(config.frame_width * 0.4)

        image_group = (
            Group(image_1, image_2)
            .arrange(RIGHT, buff=0.5)
            .move_to(ORIGIN)
            .to_edge(DOWN, buff=0.7)
        )

        column_groups = []
        for image in image_group:
            columns = ["Input Image", "GradCAM++", r"HighResCAM\\(GradCAM++)"]
            columns_group = VGroup()
            for i, column in enumerate(columns):
                column_text = Tex(column).scale(0.3)
                columns_group.add(column_text)
            columns_group.arrange(RIGHT, buff=0.5).next_to(
                image, UP, buff=0.1
            ).scale_to_fit_width(image.width * 0.9)
            column_groups.append(columns_group)

        self.p.play(FadeIn(image_group), [Write(c) for c in column_groups])
        self.p.next_slide()
        # Fade out everything
        self.p.play(FadeOut(image_group), [Unwrite(c) for c in column_groups])
