from manim import *  # or: from manimlib import *
from manim_slides import Slide
from templates import SlideTemplate
from vgg import VGG
from layer_mixing import LayerMixing
from layer_mixing_table import LayerMixingTable
from title import TitleSlide
from grad_cam import GradCAM
from mixing_architecture import MixingArchitecture
from erf import ERF
from upscaling import Upscaling
from qualitative_results import QualitativeResults

# import light_theme
from metrics import AvgDrop_ROAD, Coherency, Complexity, CompositeMetrics
from results import Results

from settings import *

# TITLE = "Explainable AI (XAI)"
# NAME = "Luca Domeniconi"
# SUBTITLE = "ML4CV XAI"
# DATE_TEXT = "2025-04-04"
TEXT_SCALE = 0.72


class ExampleScene(SlideTemplate):
    def __init__(self, **kwargs):
        super().__init__(
            title_str="XAI in Computer Vision (CV)",
            name="Luca Domeniconi",
            subtitle="ML4CV XAI",
            date_text="2025-04-04",
            **kwargs,
        )

    def construct(self):
        self.wait_time_between_slides = 0.1
        title = TitleSlide(self)
        title.construct(
            title_str="High Resolution Class Activation Mapping",
            name="Luca Domeniconi",
            date_text="April 24, 2025",
        )

        self.wait_time_between_slides = 0.1
        self.add_slide_template()
        ########################################
        # Slide 1
        ########################################
        content = Tex(
            r"In the field of CV, a popular approach to explain the functioning of a model is the \underline{attribution map}."
        )
        self.add_content(content)
        images = [
            ("./images/image.png", r"Input Image"),
            ("./images/attribution_map_layer_20.png", r"Attribution Map"),
            (
                "./images/attribution_map_layer_20_overlay.png",
                r"Overlayed\\Attribution Map",
            ),
        ]

        images_group = Group()
        descriptions_group = Group()
        for image_path, description in images:
            image = ImageMobject(image_path).scale_to_fit_width(3)
            images_group.add(image)

        images_group.arrange(RIGHT, buff=1)
        images_group.to_edge(DOWN, buff=1)

        for i, (image_path, description) in enumerate(images):
            description_text = Tex(description).scale(TEXT_SCALE)
            description_text.next_to(images_group[i], UP, buff=0.1)
            descriptions_group.add(description_text)

        self.p.play([FadeIn(images_group)] + [Write(d) for d in descriptions_group])
        self.next_slide()
        self.p.play(
            FadeOut(images_group),
            *[Unwrite(d) for d in descriptions_group],
        )
        self.remove_content()

        ########################################
        # Slide 1.1
        ########################################
        content = Tex(r"How do we measure the \textbf{importance} of each input pixel?")
        content.move_to(ORIGIN)
        self.p.play(Write(content))
        self.next_slide()
        self.p.play(Unwrite(content))
        ########################################
        # Slide 2
        ########################################
        self.change_title_and_add_page_number("Grad-CAM (Class Activation Mapping)")
        gradcam = GradCAM(self)
        gradcam.construct()
        self.next_slide()

        ##########################################
        # Slide 3
        ##########################################
        self.change_title_and_add_page_number("Layer Selection")
        vgg = VGG(self)
        vgg.construct()
        self.next_slide()

        #############################################
        # Slide 4
        #############################################
        self.change_title_and_add_page_number("Layer Filtering")
        architecture = MixingArchitecture(self)
        architecture.construct()
        self.next_slide()

        # ##############################################
        # # Slide 5
        # ##############################################
        self.change_title_and_add_page_number("Upscaling Methods")
        upscaling = Upscaling(self)
        upscaling.construct()
        self.next_slide()

        self.change_title_and_add_page_number(
            "Effective Receptive Field (ERF) Upsampling"
        )
        erf = ERF(self)
        erf.construct()
        self.next_slide()

        self.change_title_and_add_page_number("Experimental Setup")
        content = r"""\begin{itemize}
                \item \textbf{VGG11} fine-tuned on:
                \begin{itemize}
                    \item \textbf{Imagenette/Imagewoof}: 10 easy + 10 hard (dog) classes
                    \item \textbf{Synthetic}: 6 shape classes on distorted "Where's Waldo?" backgrounds
                \end{itemize}
            \end{itemize}"""
        print(content)
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{enumitem}")
        content = Tex(content, tex_template=template)  # Ensure xcolor is loaded)
        content.scale(TEXT_SCALE)
        self.add_content(content)
        images = [
            ("./images/image.png", r"Imagenette\\Easy Class"),
            ("./images/imagewoof.jpeg", r"Imagewoof\\Hard Class"),
            ("./images/synthetic_0.png", r"Synthetic\\Filled shape"),
            ("./images/synthetic_1.png", r"Synthetic\\Empty shape"),
        ]

        images_group = Group()
        for image_path, description in images:
            image = ImageMobject(image_path).scale_to_fit_width(2)
            description_text = Tex(description).scale(TEXT_SCALE)
            description_text.next_to(image, UP, buff=0.1)
            image_group = Group(image, description_text)
            image_group.arrange(DOWN, buff=0.1)
            images_group.add(image_group)

        images_group.arrange(RIGHT, buff=1)
        # images_group.move_to(ORIGIN)
        images_group.next_to(content, DOWN, buff=0.5)
        images_group.set_x(0)
        self.p.play(FadeIn(images_group))
        self.next_slide()
        self.p.play(FadeOut(images_group))
        self.remove_content()

        # # self.change_title_and_add_page_number("Layer Mixing")
        # # layer_mixing = LayerMixing(self)
        # # layer_mixing.construct()
        # # self.next_slide()
        # # self.remove_content()

        # # ################################################
        # # # Slide 6
        # # ################################################
        self.change_title_and_add_page_number("Metrics")
        content = Tex(
            r"How do we \underline{measure} the quality of an attribution map?"
        ).move_to(ORIGIN)
        self.p.play(Write(content))
        self.next_slide()
        self.p.play(Unwrite(content))

        AvgDrop_ROAD(self).construct()
        self.next_slide()
        Coherency(self).construct()
        self.next_slide()
        Complexity(self).construct()
        self.next_slide()
        CompositeMetrics(self).construct()
        self.next_slide()

        ##################################################
        # # Slide 7
        # ##################################################
        self.change_title_and_add_page_number("Results")
        Results(self).construct()
        self.next_slide()

        # ##################################################
        # # # Slide 8
        # # ##################################################
        self.change_title_and_add_page_number("Qualitative Results")
        qualitative_results = QualitativeResults(self)
        qualitative_results.construct()
        self.next_slide()

        # ###################################################
        # # Slide 9
        # #####################################################
        self.change_title_and_add_page_number("Future Work")
        content = r"""\begin{itemize}
        \item- Repeat the experiments with different models (e.g., ResNet family, SwinTransformer, etc.)
        \item- Compare even more attribution methods with the filtering technique
    \end{itemize}"""
        print(content)
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{enumitem}")
        content = Tex(content, tex_template=template)  # Ensure xcolor is loaded)
        content.scale(TEXT_SCALE)
        self.add_content(content)
        # # # self.change_title_and_add_page_number("Layer M")
        # # layer_mixing_table = LayerMixingTable(self)
        # # layer_mixing_table.construct()
        # # self.next_slide()
        # # self.remove_content()
