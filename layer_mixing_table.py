from manim import *  # or: from manimlib import *
import numpy as np
from my_scene import MySlide

from settings import *


class LayerMixingTable(MySlide):
    def construct(self):
        image = ImageMobject("image.jpeg").scale(0.5)
        table_rows = ["Layer 20", "Layer 15", "Layer 10", "Layer 5"]
        table_columns = [
            "Attribution",
            "Upsampled\\\\Attribution",
            "Mixed\\\\Attribution",
        ]
        table_data = [image.copy() for _ in range(len(table_rows) * len(table_columns))]
        table_data_group = Group(*table_data)

        table_data_group.arrange_in_grid(
            rows=len(table_rows), cols=len(table_columns), buff=0.5
        )

        # Display the table rows
        row_labels = []
        for i, row in enumerate(table_rows):
            row_label = (
                Tex(row)
                .scale(0.6)
                .move_to(table_data[i * len(table_columns)].get_center())
                .next_to(table_data[i * len(table_columns)], LEFT)
            )
            row_labels.append(row_label)

        # Display the table columns
        column_labels = []
        for j, column in enumerate(table_columns):
            column_label = (
                Tex(column)
                .scale(0.6)
                .move_to(table_data[j].get_center())
                .next_to(table_data[j], UP)
            )
            column_labels.append(column_label)

        table_group = Group(table_data_group, *row_labels, *column_labels)
        table_group.to_edge(UP, buff=0.5)

        self.p.play([Write(label) for label in row_labels] + [Write(column_labels[0])])

        self.p.play(
            [
                GrowFromCenter(table_data[i * len(table_columns)])
                for i in range(len(table_rows))
            ]
        )

        self.p.next_slide()

        self.p.play(Write(column_labels[1]))
        self.p.play(
            [
                GrowFromCenter(table_data[i * len(table_columns) + 1])
                for i in range(len(table_rows))
            ]
        )
        self.p.next_slide()

        self.p.play(Write(column_labels[2]))

        for i in range(len(table_rows)):
            images = table_data[
                1 : (i + 1) * len(table_columns) + 1 : len(table_columns)
            ]

            target_image = table_data[i * len(table_columns) + 2]

            images = [image.copy() for image in images]

            self.p.play(
                [Circumscribe(image, color=YELLOW, time_width=0.5) for image in images]
            )

            self.p.next_slide()

            self.p.play(
                [
                    image.animate.move_to(target_image.get_center()).fade(0.5)
                    for image in images
                ]
                + [
                    FadeIn(target_image, shift=DOWN * 0.5),
                ]
            )
            self.p.remove(*images)

        self.p.next_slide()

        # Fade out all images and text except the last two
        to_focus = table_data[-2:]

        self.p.play(
            [
                FadeOut(item)
                for item in table_data + row_labels + column_labels
                if item not in to_focus
            ]
        )

        to_focus_group = Group(*(to_focus))

        self.p.play(
            to_focus_group.animate.arrange_in_grid(rows=1, cols=len(to_focus), buff=0.5)
            .move_to(ORIGIN)
            .scale(3)
        )

        text_upsample = (
            Tex("Upsampled\\\\Attribution")
            .scale(0.6)
            .next_to(to_focus[0], UP, buff=0.5)
        )

        text_mixed = (
            Tex("Mixed\\\\Attribution").scale(0.6).next_to(to_focus[1], UP, buff=0.5)
        )

        self.p.play(Write(text_upsample), Write(text_mixed))
