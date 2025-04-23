from manim_slides import Slide


class MySlide(Slide):
    def __init__(self, parent_object: Slide = None, **kwargs):
        super().__init__(**kwargs)
        if parent_object is None:
            self.p: Slide = self
        else:
            self.p: Slide = parent_object
