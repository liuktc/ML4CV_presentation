from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide
from utils import get_square_corners

VGG11_LAYERS = [
    ("conv", (64, 224, 224)),
    # ("conv", (64, 224, 224)),
    ("pool", (64, 112, 112)),
    ("conv", (128, 112, 112)),
    # ("conv", (128, 112, 112)),
    ("pool", (128, 56, 56)),
    ("conv", (256, 56, 56)),
    ("conv", (256, 56, 56)),
    # ("conv", (256, 56, 56)),
    ("pool", (256, 28, 28)),
    ("conv", (512, 28, 28)),
    ("conv", (512, 28, 28)),
    # ("conv", (512, 28, 28)),
    ("pool", (512, 14, 14)),
    ("conv", (512, 14, 14)),
    ("conv", (512, 14, 14)),
    # ("conv", (512, 14, 14)),
    ("pool", (512, 7, 7)),
]

# Map the channels that are in [64,512] to [0, 1]
CHANNELS_TO_WIDTH = {
    64: 0.15,
    128: 0.3,
    256: 0.4,
    512: 0.55,
}

HEIGHT_TO_HEIGHT = {
    224: 4,
    112: 2,
    56: 1,
    28: 0.2,
    14: 0.1,
    7: 0.05,
}

GROUP_LENGHT = [1, 2, 3, 3, 3, 1]


class VGGModel(MySlide):
    def construct(self):
        # # Create the VGG architecture diagram
        # x_start = 2
        self.layers = []
        for layer_type, shape in VGG11_LAYERS:
            channels, height, width = shape
            if layer_type == "conv":
                layer = Rectangle(
                    width=CHANNELS_TO_WIDTH[channels],
                    height=HEIGHT_TO_HEIGHT[height],
                    color=BLUE,
                    fill_opacity=0.3,
                )
            elif layer_type == "pool":
                layer = Rectangle(
                    width=CHANNELS_TO_WIDTH[channels],
                    height=HEIGHT_TO_HEIGHT[height],
                    color=GREEN,
                    fill_opacity=0.3,
                )
            else:
                raise ValueError("Unknown layer type")

            if len(self.layers) > 0:
                layer.next_to(self.layers[-1], RIGHT, buff=0.1)
            else:
                layer.to_edge(LEFT)
            self.layers.append(layer)

        layers_group_for_text = Group(*self.layers)
        layers_group_for_text.scale_to_fit_width(config.frame_width * 0.6)
        layers_group_for_text.move_to(ORIGIN)
        # Add two little squares in the top right corner to make a legend of the types of layers
        # Create a square for the conv layer
        self.conv_square_label = Tex("Conv Layer").scale(0.6)
        self.conv_square = (
            Square(color=BLUE, fill_opacity=0.3)
            .scale(0.1)
            .move_to(self.conv_square_label.get_center())
        )
        self.conv_square.next_to(self.conv_square_label, LEFT, buff=0.1)
        conv_square_group = VGroup(self.conv_square, self.conv_square_label)

        # Create a square for the pool layer
        self.pool_square_label = Tex("Pool Layer").scale(0.6)
        self.pool_square = (
            Square(color=GREEN, fill_opacity=0.3)
            .scale(0.1)
            .move_to(self.pool_square_label.get_center())
        )
        self.pool_square.next_to(self.pool_square_label, LEFT, buff=0.1)
        pool_square_group = VGroup(self.pool_square, self.pool_square_label)

        pool_square_group.to_edge(RIGHT, buff=0.5)
        pool_square_group.to_edge(UP, buff=1)
        conv_square_group.next_to(pool_square_group, DOWN, buff=0.1, aligned_edge=LEFT)

        # Add the squares to the scene
        count = 0
        self.texts = []
        for length in GROUP_LENGHT:
            layers_group_for_text = Group(*self.layers[count : count + length])

            layer_type, shape = VGG11_LAYERS[count]
            channels, height, width = shape

            text = MathTex(f"{channels} \\times {height} \\times {width}").scale(0.5)
            if count == len(self.layers) - 1:
                text.move_to(layers_group_for_text.get_top() + 0.2 * UP + 0.3 * RIGHT)
            else:
                text.move_to(layers_group_for_text.get_top() + 0.2 * UP)

            self.texts.append(text)

            count = count + length

        # self.p.play([Create(layer) for layer in self.layers])
        # self.p.play(
        #     Create(conv_square),
        #     Write(conv_square_label),
        #     Create(pool_square),
        #     Write(pool_square_label),
        # )
        # self.p.play([Write(text) for text in texts])

        self.vgg_model = VGroup(*self.layers, *self.texts)
        self.vgg_group = VGroup(
            *self.layers, *self.texts, conv_square_group, pool_square_group
        )
        self.layer_group = VGroup(*self.layers)
        self.pool_layers = [
            self.layers[i]
            for i in range(len(self.layers))
            if "pool" in VGG11_LAYERS[i][0]
        ][::-1]
        # self.p.play(
        #     [
        #         vgg_group.animate.scale_to_fit_width(config.frame_width * 0.4).to_edge(
        #             DOWN, buff=0.2
        #         ),
        #     ]
        # )
        # Fade out everything
        # self.p.play(
        #     [
        #         FadeOut(item)
        #         for item in layers
        #         + texts
        #         + [conv_square, conv_square_label, pool_square, pool_square_label]
        #     ]
        # )

    def display(self, hide_legend=False):
        self.p.play([Create(layer) for layer in self.layers])
        if not hide_legend:
            self.p.play(
                Create(self.conv_square),
                Write(self.conv_square_label),
                Create(self.pool_square),
                Write(self.pool_square_label),
            )
        self.p.play([Write(text) for text in self.texts])
