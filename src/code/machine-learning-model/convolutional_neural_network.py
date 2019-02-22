# Machine Learning libraries
import tensorflow as tf

# Matrix Operation Libaries
import cv2
import numpy as np

# Import standard libaries
import os
import matplotlib.pyplot as plt
import random
import pickle

class ConvolutionalNeuralNetwork:

    # Images are 32x32 24-bit RGB
    train_data_path = './pixel_bitmaps/train/'
    test_data_path = './pixel_bitmaps/test/'
    categories = ["Walk", "Run", "LowResistanceBike", "HighResistanceBike"]

    def create_model_data(self, data_path):

        training_data = []

        # Train Dataset
        for category in self.categories:
            # Path to each exercise category of images
            path = os.path.join(data_path, category)
            class_num = self.categories.index(category)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                    training_data.append([img_array, class_num])
                except Exception as e:
                    print("Image Broken")
                    pass

        return training_data

    def pack(self, data, img_type):
        # Shuffle data so model doesn't over-train
        random.shuffle(data)
        # Feature Set (X)
        X = []
        # Label Set | Classes (y)
        y = []

        # Build these out as lists
        for features, label in data:
            X.append(features)
            y.append(label)

        # -1 is a catch-all for all values
        # 32x32 size image
        # 1 is to specify grey-scale
        X = np.array(X).reshape(-1, 32, 32, 1)

        # Save data
        pickle_out = open("./model_data/{}/feature_set.pickle".format(img_type), "wb")
        pickle.dump(X, pickle_out)
        pickle_out.close()

        pickle_out = open("./model_data/{}/class_set.pickle".format(img_type), "wb")
        pickle.dump(y, pickle_out)
        pickle_out.close()

    # Function which builds the train & test pickle files.
    def build_train_test_pickle_files(self):
        data_train = self.create_model_data(self.train_data_path)
        data_test = self.create_model_data(self.test_data_path)
    
        self.pack(data_train, "train")
        self.pack(data_test, "test")

    # Feature_set contains all image matrix data
    # Class set contains class of specific index of image.
    def read(self, file):
        pickle_in = open(file, "rb")
        X = pickle.load(pickle_in)
        return X

    def start_training(self):
        # Data
        x_train = self.read('./model_data/train/feature_set.pickle')
        y_train = np.asarray(self.read('./model_data/train/class_set.pickle'))
        x_test = self.read('./model_data/test/feature_set.pickle')
        y_test = np.asarray(self.read('./model_data/test/class_set.pickle'))

        # Normalise data -- easier for network to learn
        x_train = tf.keras.utils.normalize(x_train, axis=1)
        x_test = tf.keras.utils.normalize(x_test, axis=1)

        # Model
        model = tf.keras.models.Sequential()

        # Add Layers
        # Add Flattened Layer -- Input Layer
        model.add(tf.keras.layers.Flatten()) 

        # Add Dense Layer -- 2 Hidden Layers
        # Activation function: Relu (Rectified-Linear)
        model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) 
        model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) 

        # Output Layer
        # Uses softmax for probability distribution.
        model.add(tf.keras.layers.Dense(4, activation=tf.nn.softmax))

        # A neural network does not strive to maximize accuracy!
        # It strives to minimise loss!

        # Optimizer: Adam (gradient descent step)
        # Loss function: cross-entropy (sparse for > 2 class labels, binary otherwise)
        model.compile(optimizer='adam', 
                    loss='sparse_categorical_crossentropy', 
                    metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=100)

        # Print out model validation loss and validation accuracy
        # Determine underfitting / overfitting!
        val_loss, val_acc = model.evaluate(x_test, y_test)
        print(val_loss, val_acc)

    def show_train_image(self, imageNo):
        x_train = self.read('./model_data/train/feature_set.pickle')
        im = np.squeeze(x_train[0])
        plt.imshow(im, cmap=plt.cm.binary)
        plt.show()


def main():
    # Extract data in matrix form
    cnn = ConvolutionalNeuralNetwork()
    cnn.build_train_test_pickle_files()
    cnn.start_training()
    

if __name__ == "__main__":
    main()