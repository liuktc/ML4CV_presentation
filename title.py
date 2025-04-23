import numpy as np
from my_scene import MySlide
from manim import *


class Title(MySlide):
    def construct(
        self,
        title_str="Title of the Slide",
        name="Luca Domeniconi",
        date_text="2025-04-24",
    ):
        # Build the title imitating the beamer style
        title = Tex(title_str, font_size=48)
        title.to_edge(UP, buff=2)

        title_rect = SurroundingRectangle(
            title,
            color=WHITE,
            buff=0.5,
            stroke_width=2,
            fill_opacity=0.5,
            corner_radius=0.2,
        )

        title_group = VGroup(title, title_rect)

        # Add the author
        author = Tex(name, font_size=30)
        author.next_to(title_group, DOWN, buff=0.5)

        supervisors_title = Tex("Supervisors:", font_size=24)
        supervisors_title.next_to(author, DOWN, buff=0.5)

        supervisors = Group(
            Tex(
                r"Prof. Samuele Salti",
                font_size=28,
            ),
            Tex(
                r"Prof. Michele Lombardi",
                font_size=28,
            ),
        )
        supervisors.arrange(RIGHT, buff=0.4)
        supervisors.next_to(supervisors_title, DOWN, buff=0.2)

        # Add the university
        university = Tex(
            r"Department of Computer Science and Engineering\\University of Bologna",
            font_size=24,
        )
        university.next_to(supervisors, DOWN, buff=0.8)

        # Add the date
        date = Tex(date_text, font_size=30)
        date.next_to(university, DOWN, buff=0.5)

        self.p.play(Write(title_group))
        self.p.play(
            Write(author),
            Write(university),
            Write(date),
            *[Write(s) for s in supervisors],
            Write(supervisors_title),
        )
        self.p.next_slide()
        # Unwrite everythin
        self.p.play(
            Unwrite(title_group),
            Unwrite(author),
            Unwrite(university),
            Unwrite(date),
            *[Unwrite(s) for s in supervisors],
            Unwrite(supervisors_title),
        )
