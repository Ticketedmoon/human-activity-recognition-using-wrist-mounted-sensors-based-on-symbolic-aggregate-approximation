"""
The process of building a Convolutional Neural Network always involves four major steps.
Step - 1 : Convolution
Step - 2 : Pooling
Step - 3 : Flattening
Step - 4 : Full connection
"""

# Importing the Keras libraries and packages

"""
we’ve imported Sequential from keras.models, to initialise our neural network model
as a sequential network. There are two basic ways of initialising a neural network,
either by a sequence of layers or as a graph.
"""
from keras.models import Sequential

"""
we’ve imported Conv2D from keras.layers, this is to perform the convolution operation
i.e the first step of a CNN, on the training images. Since we are working on images here,
which a basically 2 Dimensional arrays, we’re using Convolution 2-D, you may have to use
Convolution 3-D while dealing with videos, where the third dimension will be time.
"""
from keras.layers import Conv2D

"""
we’ve imported MaxPooling2D from keras.layers, which is used for pooling operation,
that is the step — 2 in the process of building a cnn. For building this particular neural network,
we are using a Maxpooling function, there exist different types of pooling operations like Min Pooling,
Mean Pooling, etc. Here in MaxPooling we need the maximum value pixel from the respective region of interest
"""
from keras.layers import MaxPooling2D

"""
We’ve imported Flatten from keras.layers, which is used for Flattening. Flattening is the process
of converting all the resultant 2 dimensional arrays into a single long continuous linear vector.
"""
from keras.layers import Flatten

"""
we’ve imported Dense from keras.layers, which is used to perform the full connection
of the neural network, which is the step 4 in the process of building a CNN.
"""
from keras.layers import Dense

# Documentation aside, implementation below:
# Note: https://becominghuman.ai/building-an-image-classifier-using-deep-learning-in-python-totally-from-a-beginners-perspective-be8dbaf22dd8