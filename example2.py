from manim import *


class SlideTemplate(Scene):
    def construct(self):
        # Define the title
        title = Text("Title of the Slide", font_size=48)
        title.to_edge(UP)

        # Define the subtitle
        subtitle = Text("Subtitle of the Slide", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)

        # Define the content area
        content = VGroup(
            Text("Content Point 1", font_size=24),
            Text("Content Point 2", font_size=24),
            Text("Content Point 3", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        content.next_to(subtitle, DOWN, buff=1.0)

        # Add all elements to the scene
        # self.add(title, subtitle, content)
        self.add(title)

        self.wait(2)

        self.add(subtitle, content)


class ExampleSlide(SlideTemplate):
    def construct(self):
        super().construct()
        # You can add more custom elements here if needed
        additional_text = Text("Additional Information", font_size=24)
        additional_text.next_to(self.mobjects[-1], DOWN, buff=0.5)
        self.add(additional_text)


class Main(Scene):
    def construct(self):
        # Create an instance of the ExampleSlide class
        slide = ExampleSlide()
        slide.render()
        # Play the animation for the slide
        # self.play(Create(slide))
        # self.wait(2)  # Wait for a moment to see the slide before ending the scene
