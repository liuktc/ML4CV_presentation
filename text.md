# Model

For the model, we used VGG11, with the structure on screen.

# Layer

When using an attribution method, a choiche often ignored, is the selection of the layer with respect to which compute the attribution. Almost all the research uses by default the last convolution layer before the fully connected head. But that's not the only option. As we can see in the animation, other layers can be used, and the results are different, in semantics information and in spatial resolution.

# Upscaling

When using an attribution map from high level features, the spatial resolution is very low (7 x 7 for example).

# Layer Mixing

As you can see from the animation, when using attribution at lower layers, the features are more local, and are not capable of localizing the object, but they are more precise in the details. Higher layers are more capable of localizing the object, but they are less precise in the details. Which one is better? The answer is both.

# Layer Mixing Table

View of upsampled and mixed attribution at various layers.

# Effective Receptive Field

The effective receptive field is the area of the input image that influences a given output feature. The effective receptive field is larger for higher layers, and smaller for lower layers. By following this definition, the erf extends the concept of receptive field by considering example specific information flow.
