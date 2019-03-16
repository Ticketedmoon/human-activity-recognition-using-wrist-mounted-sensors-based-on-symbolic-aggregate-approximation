# Machine Learning libraries
import tensorflow as tf
import h5py
from keras.models import model_from_json
from keras.models import load_model

# Matrix Operation Libaries
import cv2
import numpy as np

# Import standard libaries
import os
import matplotlib.pyplot as plt
import random
import pickle

class ConvolutionalNeuralNetwork:

    # Images are 64x64 24-bit RGB
    image_size = 64

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
        X = np.array(X).reshape(-1, self.image_size, self.image_size, 1)

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
        # Activation function: sigmoid
        model.add(tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)) 
        model.add(tf.keras.layers.Dense(128, activation=tf.nn.sigmoid)) 

        # Output Layer
        # Uses softmax for probability distribution.
        model.add(tf.keras.layers.Dense(4, activation=tf.nn.softmax))

        # A neural network does not strive to maximize accuracy!
        # It strives to minimise loss!

        # Optimizer: Adam (gradient descent step)
        # Loss function: cross-entropy (sparse for > 2 class labels, binary otherwise)
        model.compile(optimizer='adam', 
                    loss=tf.keras.losses.sparse_categorical_crossentropy, 
                    metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=5)

        # Print out model validation loss and validation accuracy
        # Determine underfitting / overfitting!
        # model.summary (useful statistic)      
        val_loss, val_acc = model.evaluate(x_test, y_test)
        print("Validation Accuracy: {}\nValidation Loss: {}".format(val_acc, val_loss))

        # Save model
        # model.save('./model_data/model/activity_recognition_model.h5')
        # serialize model to JSON
        #  the keras model which is trained is defined as 'model' in this example
        model_json = model.to_json()
        with open("./model_data/model/activity_recognition_model.json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        model.save_weights("./model_data/model/activity_recognition_model.h5", save_format="h5")

    def load_model(self):
        # Test data
        x_test = self.read('./model_data/test/feature_set.pickle')
        y_test = np.asarray(self.read('./model_data/test/class_set.pickle'))

        # load json and create model
        json_file = open('./model_data/model/activity_recognition_model.json', 'r')

        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = tf.keras.models.model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights("./model_data/model/activity_recognition_model.h5")
        print("Loaded model from disk")

        return loaded_model

    def predict(self, index):
        # Test data
        x_test = self.read('./model_data/test/feature_set.pickle')
        y_test = np.asarray(self.read('./model_data/test/class_set.pickle'))

        # Loading Model: 
        new_model = self.load_model()

        # Make a prediction!
        # returns an array of arrays of probability distributions
        predictions = new_model.predict(x_test)

        # Get a value prediction!
        # Predictions returned in form of 0, 1, 2, 3
        # 0 = Walk, 1 = Run, 2 = Low Bike, 3 = High Bike
        categories = ["Walk", "Run", "LowResistanceBike", "HighResistanceBike"]
        prediction_value = np.argmax(predictions[index])
        print("Prediction: " + str(prediction_value) + " (" + categories[prediction_value] + ")")

        self.show_train_image(index)

    def show_train_image(self, imageNo):
        x_train = self.read('./model_data/train/feature_set.pickle')
        im = np.squeeze(x_train[imageNo])
        plt.imshow(im)
        plt.show()


def main():
    # Extract data in matrix form
    cnn = ConvolutionalNeuralNetwork()
    cnn.build_train_test_pickle_files()
    cnn.start_training()
    # cnn.load_model()
    # cnn.predict(2)

if __name__ == "__main__":
    main()