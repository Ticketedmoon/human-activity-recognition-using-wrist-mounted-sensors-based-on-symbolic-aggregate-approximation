"""
The process of building a Convolutional Neural Network always involves four major steps.
Step - 1 : Convolution
Step - 2 : Pooling
Step - 3 : Flattening
Step - 4 : Full connection
"""

# Importing the Keras libraries and packages

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np

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

class NeuralNetwork:

    # Initialising the CNN
    def __init__(self):
        self.classifier = Sequential()

    # Step 1 - Convolution
    def convolution(self):
        self.classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 2), activation='relu'))

    # Step 2 - Pooling
    def apply_pooling(self):
        self.classifier.add(MaxPooling2D(pool_size = (2, 2)))

        self.classifier.add(Flatten())
        self.classifier.add(Dense(units = 128, activation = 'relu'))
        self.classifier.add(Dense(units = 1, activation = 'sigmoid'))

    # Adding a second convolutional layer
    def add_second_convol_layer(self):
        self.classifier.add(Conv2D(32, (3, 3), activation='relu'))
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    def flatten(self):
        self.classifier.add(Flatten())

    # Step 4 - Full connection
    def densify(self):
        self.classifier.add(Dense(units=128, activation='relu'))
        self.classifier.add(Dense(units=1, activation='sigmoid'))

    # Optimizer  parameter is to choose the stochastic gradient descent algorithm.
    # Loss parameter is to choose the loss function.
    # Finally, the metrics parameter is to choose the performance metric.
    def compile(self):
        self.classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    # we are creating synthetic data out of the same images by performing different type of
    # operations on these images like flipping, rotating, blurring, etc.
    def reduce_overfitting(self):
        train_datagen = ImageDataGenerator(rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        self.training_set = train_datagen.flow_from_directory('pixel_bitmaps/train',
            target_size=(64, 64),
            batch_size=32,
            class_mode='binary')
        self.test_set = test_datagen.flow_from_directory('pixel_bitmaps/test',
            target_size=(64, 64),
            batch_size=32,
            class_mode='binary')

    def fit(self):
        self.classifier.fit_generator(self.training_set,
            steps_per_epoch = 12455,
            epochs = 25,
            validation_data = self.test_set,
            validation_steps = 2000)

    def predict(self):
        test_image = image.load_img('pixel_bitmaps/test/Walk/walk01-1.png', target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = self.classifier.predict(test_image)
        self.training_set.class_indices
        if result[0][0] == 1:
            prediction = 'Walk'
        else:
            prediction = 'Not Walk'

        return prediction

def main():
    network = NeuralNetwork()
    network.convolution()
    network.apply_pooling()
    network.add_second_convol_layer()
    network.flatten()
    network.densify()
    network.compile()
    network.fit()

if __name__ == "__main__":
    main()
