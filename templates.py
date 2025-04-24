from manim import *  # or: from manimlib import *
from manim_slides import Slide
from my_scene import MySlide

from settings import *


class SlideTemplate(MySlide):
    def __init__(
        self,
        title_str="Title",
        name="Name",
        subtitle="Subtitle",
        date_text="01/01/1970",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.content = None
        self.title = None
        self.title_str = title_str
        self.name = name
        self.subtitle = subtitle
        self.date_text = date_text
        self.page_number = 1
        self.page_number_mobject = None

    def add_slide_template(self):
        screen_width = config.frame_width
        # Define the slide title
        self.title = Tex(f"\\textbf{{{self.title_str}}}", font_size=24)
        self.title.to_edge(UP, buff=0.3)
        self.title.to_edge(LEFT, buff=0.5)

        title_line = Line(start=ORIGIN, end=screen_width * 2 * RIGHT)
        title_line.next_to(self.title, DOWN, buff=0.2)

        DOWN_BUFF = 0.15
        # Define the subtitle
        subtitle = Tex(f"\\textit{{{self.subtitle}}}", font_size=24)
        subtitle.to_edge(DOWN, buff=DOWN_BUFF)

        self.page_number_mobject = Tex(self.page_number, font_size=24)
        self.page_number_mobject.to_edge(DOWN, buff=DOWN_BUFF)
        self.page_number_mobject.to_edge(RIGHT, buff=0.5)

        # # Define the footer with the date
        date_text = Tex(self.date_text, font_size=24)
        # Put the date text at the bottom right of the screen
        # date_text.to_edge(DOWN)
        # date_text.to_edge(DOWN, buff=DOWN_BUFF)
        # date_text.to_edge(RIGHT, buff=4.5)
        date_text.next_to(self.page_number_mobject, LEFT, buff=0.5)

        # # Define the footer with the website URL
        name = Tex(f"\\textbf{{{self.name}}}", font_size=24)
        # url_text.next_to(date_text, UP, buff=0.2)
        name.to_edge(DOWN, buff=DOWN_BUFF)
        name.to_edge(LEFT, buff=0.5)

        line = Line(start=ORIGIN, end=screen_width * 2 * RIGHT)
        line.next_to(subtitle, UP, buff=0.1)
        line.set_stroke(width=2)

        # Play more animations at the same time
        self.play(
            Write(subtitle),  # Fade in the subtitle
            Write(date_text),  # Fade in the date text
            Write(name),  # Fade in the URL text
            Create(line),  # Fade in the line
            Write(self.title),  # Fade in the title
            Create(title_line),  # Fade in the title line
            Write(self.page_number_mobject),  # Fade in the page number
        )

    def add_content(self, content: Mobject):
        self.content = content
        if content.width > config.frame_width * 0.9:
            before_width = content.width
            content.scale_to_fit_width(config.frame_width * 0.9)
            after_width = content.width
            print(
                f"Before width: {before_width}, After width: {after_width}, Scale: {after_width / before_width}"
            )

        content.next_to(self.title, DOWN, buff=1)
        content.align_to(self.title, LEFT)
        self.play(Write(content))
        # self.wait(1)  # Wait for a moment to let the content be visible

    def remove_content(self):
        self.play(FadeOut(self.content))
        self.content = None

    def change_title(self, new_title: str):
        # Create a new title object with the new text
        new_title_obj = Tex(f"\\textbf{{{new_title}}}", font_size=24)
        new_title_obj.move_to(self.title.get_center())
        new_title_obj.align_to(self.title, LEFT)  # Align to the left of the old title

        # Animate the replacement of the old title with the new one
        self.play(ReplacementTransform(self.title, new_title_obj))
        self.title = new_title_obj

    def add_page_number(self):
        self.page_number += 1

        if self.page_number_mobject:
            new_page_number_mobject = Tex(self.page_number, font_size=24)
            new_page_number_mobject.move_to(self.page_number_mobject.get_center())
            self.play(
                ReplacementTransform(self.page_number_mobject, new_page_number_mobject)
            )
            self.page_number_mobject = new_page_number_mobject

    def change_title_and_add_page_number(self, new_title: str):
        # Create a new title object with the new text
        new_title_obj = Tex(f"\\textbf{{{new_title}}}", font_size=24)
        new_title_obj.move_to(self.title.get_center())
        new_title_obj.align_to(self.title, LEFT)  # Align to the left of the old title

        # Animate the replacement of the old title with the new one

        self.page_number += 1

        new_page_number_mobject = Tex(self.page_number, font_size=24)
        new_page_number_mobject.move_to(self.page_number_mobject.get_center())

        self.play(
            [
                ReplacementTransform(self.title, new_title_obj),
                ReplacementTransform(self.page_number_mobject, new_page_number_mobject),
            ]
        )

        self.title = new_title_obj
        self.page_number_mobject = new_page_number_mobject
