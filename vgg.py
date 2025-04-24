from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners, right_angle_arrow_custom
from vgg_model import VGG11_LAYERS, VGGModel
from templates import SlideTemplate

# from light_theme import *
from settings import *


class VGG(MySlide):
    def construct(self):
        # self.add_slide_template()
        # # # Create the VGG architecture diagram
        # # x_start = 2
        # layers = []
        # for layer_type, shape in VGG11_LAYERS:
        #     channels, height, width = shape
        #     if layer_type == "conv":
        #         layer = Rectangle(
        #             width=CHANNELS_TO_WIDTH[channels],
        #             height=HEIGHT_TO_HEIGHT[height],
        #             color=BLUE,
        #             fill_opacity=0.3,
        #         )
        #     elif layer_type == "pool":
        #         layer = Rectangle(
        #             width=CHANNELS_TO_WIDTH[channels],
        #             height=HEIGHT_TO_HEIGHT[height],
        #             color=GREEN,
        #             fill_opacity=0.3,
        #         )
        #     else:
        #         raise ValueError("Unknown layer type")

        #     if len(layers) > 0:
        #         layer.next_to(layers[-1], RIGHT, buff=0.1)
        #     else:
        #         layer.to_edge(LEFT)
        #     layers.append(layer)

        # layers_group_for_text = Group(*layers)
        # layers_group_for_text.scale_to_fit_width(config.frame_width * 0.6)
        # layers_group_for_text.move_to(ORIGIN)
        # # self.p.play(Create(layers_group))
        # self.p.play([Create(layer) for layer in layers])
        # # self.add(layer)
        # # Add two little squares in the top right corner to make a legend of the types of layers
        # # Create a square for the conv layer
        # conv_square_label = Tex("Conv Layer").scale(0.6)
        # conv_square = (
        #     Square(color=BLUE, fill_opacity=0.3)
        #     .scale(0.1)
        #     .move_to(conv_square_label.get_center())
        # )
        # conv_square.next_to(conv_square_label, LEFT, buff=0.1)
        # conv_square_group = VGroup(conv_square, conv_square_label)

        # # Create a square for the pool layer
        # pool_square_label = Tex("Pool Layer").scale(0.6)
        # pool_square = (
        #     Square(color=GREEN, fill_opacity=0.3)
        #     .scale(0.1)
        #     .move_to(pool_square_label.get_center())
        # )
        # pool_square.next_to(pool_square_label, LEFT, buff=0.1)
        # pool_square_group = VGroup(pool_square, pool_square_label)

        # pool_square_group.to_edge(UP + RIGHT, buff=0.5)
        # conv_square_group.next_to(pool_square_group, DOWN, buff=0.1, aligned_edge=LEFT)

        # # Add the squares to the scene
        # self.p.play(
        #     Create(conv_square),
        #     Write(conv_square_label),
        #     Create(pool_square),
        #     Write(pool_square_label),
        # )

        # count = 0
        # texts = []
        # for length in GROUP_LENGHT:
        #     layers_group_for_text = Group(*layers[count : count + length])
        #     # average_top_position = np.mean(
        #     #     [layer.get_top() for layer in layers_group], axis=0
        #     # )
        #     # print(average_top_position)

        #     layer_type, shape = VGG11_LAYERS[count]
        #     channels, height, width = shape

        #     text = MathTex(f"{channels} \\times {height} \\times {width}").scale(0.5)
        #     # text.move_to(average_top_position + 0.2 * UP)
        #     if count == len(layers) - 1:
        #         text.move_to(layers_group_for_text.get_top() + 0.2 * UP + 0.3 * RIGHT)
        #     else:
        #         text.move_to(layers_group_for_text.get_top() + 0.2 * UP)

        #     texts.append(text)

        #     count = count + length

        # self.p.play([Write(text) for text in texts])

        # vgg_group = VGroup(*layers, *texts)
        # self.p.play(
        #     [
        #         vgg_group.animate.scale_to_fit_width(config.frame_width * 0.4).to_edge(
        #             DOWN, buff=0.2
        #         ),
        #     ]
        # )
        # for each layer "conv" add an image on the upper edge but on the same X, and make an arrow that points to the layer
        model = VGGModel(self.p)
        model.construct()
        model.display()
        self.p.next_slide()

        vgg_model = model.vgg_model
        self.p.play(
            vgg_model.animate.scale_to_fit_width(config.frame_width * 0.4).to_edge(
                LEFT, buff=0.2
            ),
        )

        # layers = model.layers

        pool_layers = model.pool_layers
        pool_layers = [pool_layers[0], pool_layers[-1]]
        # Create 4 images and write a formula indicating a sum of the images
        images = []
        descriptions = [
            r"\textbf{Deep Layer}",
            # "Mid-High features",
            # "Mid-Low features",
            r"\textbf{Shallow Layer}",
        ]

        texts = [
            (
                r"Low spatial resolution.",
                r"Attention to high level concepts.",
                r"Require upsampling and often\\ miss fine-grained details.",
            ),
            (
                r"High spatial resolution.",
                r"Attention to small level details.",
                r"Noisy if not processed.",
            ),
        ]
        top_texts = []
        bottom_texts = []
        arrows = []
        for i in range(2):
            if i == 0:
                image = ImageMobject(
                    f"./images/attribution_map_layer_20_bilinearUpsampling_small.png"
                ).scale_to_fit_width(2)
            else:
                image = ImageMobject(
                    f"./images/attribution_map_layer_5.png"
                ).scale_to_fit_width(2)
            image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            # image.scale(0.5)
            # if len(images) > 0:
            # image.next_to(images[-1], RIGHT, buff=0.5)
            # else:
            # image.to_edge(LEFT)

            top_text = Tex(descriptions[i]).scale(0.6)
            top_text.move_to(image.get_top() + 0.2 * UP)

            images.append(image)

            top_texts.append(top_text)
            bottom_text = BulletedList(*texts[i]).scale(0.5)
            bottom_text[-1].set_color(RED)
            # bottom_text = Tex(texts[i]).scale(0.5)
            bottom_text.next_to(image, RIGHT, buff=0.2)
            bottom_texts.append(bottom_text)

        group_images = Group(
            *[
                Group(image, top_text, bottom_text)
                for image, top_text, bottom_text in zip(images, top_texts, bottom_texts)
            ]
        )
        # group_images.scale_to_fit_width(config.frame_width * 0.4)
        group_images.arrange(DOWN, buff=1).move_to(ORIGIN).next_to(
            vgg_model, RIGHT, buff=1
        )

        # for i in range(2):
        # arrow = Arrow(
        #     pool_layers[i].get_top(), images[i].get_bottom(), buff=0.1, color=WHITE
        # )

        arrows = [
            right_angle_arrow_custom(
                pool_layers[0].get_top(), images[0].get_left(), color=WHITE
            ),
            right_angle_arrow_custom(
                pool_layers[1].get_bottom(), images[1].get_left(), color=WHITE
            ),
        ]

        # Show first image alone
        # self.p.play([FadeIn(images[0]), FadeIn(arrows[0]), Write(top_texts[0])])
        # self.p.play(FadeOut(arrows[0]))
        # self.p.next_slide()

        for i in range(2):
            self.p.play(
                [
                    FadeIn(images[i]),
                    Create(arrows[i]),
                    Write(top_texts[i]),
                    Write(bottom_texts[i]),
                ]
            )
            self.p.next_slide()
            # self.p.play(FadeOut(arrows[i]))

        # self.p.next_slide()
        focus_rect = SurroundingRectangle(
            Group(images[0], top_texts[0], bottom_texts[0]),
            color=YELLOW,
            buff=0.1,
            fill_opacity=0.1,
        )
        self.p.play(Create(focus_rect))
        self.p.next_slide()
        # Fade out everything
        self.p.play(
            [FadeOut(item) for item in images + top_texts + bottom_texts + arrows]
            + [FadeOut(model.vgg_group)]
            + [FadeOut(focus_rect), FadeOut(vgg_model)],
        )
