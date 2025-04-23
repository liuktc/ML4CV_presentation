from manim import *


class VGG11Architecture3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=90 * DEGREES, theta=-90 * DEGREES)
        # self.set_camera_orientation(phi=0 * DEGREES, theta=-0 * DEGREES)

        layers = [
            (
                [("Conv1", 64, 224), ("Conv2", 64, 224)],
                "224 \\times 224 \\times 64",
            ),
            # ]
            (
                [
                    ("MaxPool", 128, 112),
                    ("Conv3", 128, 112),
                    ("Conv4", 128, 112),
                ],
                "112 \\times 112 \\times 64",
            ),
            (
                [
                    ("MaxPool", 256, 56),
                    ("Conv5", 256, 56),
                    ("Conv6", 256, 56),
                    ("Conv7", 256, 56),
                ],
                "56 \\times 56 \\times 128",
            ),
            (
                [
                    ("MaxPool", 512, 28),
                    ("Conv8", 512, 28),
                    ("Conv9", 512, 28),
                    ("Conv10", 512, 28),
                ],
                "28 \\times 28 \\times 256",
            ),
            (
                [
                    ("MaxPool", 512, 14),
                    ("Conv11", 512, 14),
                    ("Conv12", 512, 14),
                    ("Conv13", 512, 14),
                ],
                "14 \\times 14 \\times 512",
            ),
        ]

        layer_objects = VGroup()
        x_shift = 0

        def interpolate(value, min_value, max_value):
            return (value - min_value) / (max_value - min_value)

        for layer_list, text in layers:
            for name, channels, spatial_size in layer_list:
                color = BLUE if "Conv" in name else GREEN if "MaxPool" in name else RED

                size = spatial_size / 50  # Scale spatial size for visualization
                # depth = (
                #     (channels / 256) if channels else 0.5
                # )  # Scale depth for visualization
                depth = interpolate(channels, 64, 512) * 2

                print("Box size:", size, "Depth:", depth)
                box = Cube(side_length=1, fill_color=color, fill_opacity=0.7)
                box.scale([depth, size, size])
                box.shift(RIGHT * x_shift)
                box_point = np.array(box.get_all_points())
                print("Box points:", box_point.max(axis=0))
                print(RIGHT)

                # label = Text(name, font_size=24).move_to(box.get_center())
                # if channels:
                #     channels_label = Text(str(channels), font_size=20).next_to(
                #         box, UP, buff=0.2
                #     )
                #     layer_objects.add(channels_label)

                layer_objects.add(box)
                # x_shift += 1.2
                x_shift += depth
            math_label = MathTex(text, font_size=24).move_to(
                box.get_center() + UP * size / 4 + UP * 0.5
            )
            # math_label.rotate(-self.camera.theta, axis=OUT)
            # math_label.rotate(-self.camera.phi, axis=RIGHT)
            # label = Text(text, font_size=24).next_to(box, UP, buff=0.2)
            # layer_list.append(math_label)
            self.add_fixed_in_frame_mobjects(math_label)

        self.play(Create(layer_objects))
        # Move the camera around the model
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(2)
