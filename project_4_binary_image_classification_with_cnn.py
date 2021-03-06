# -*- coding: utf-8 -*-
"""Project 4: Binary Image Classification with CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z-ED1rmgV_Yst_ynHDKYaAzWfqUTHFXe

# Step 1: Installation and Setup
"""

# Installing TensorFlow
! pip install -q tensorflow-gpu

import tensorflow as tf
print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""# Step 2: Importing the dataset from Kaggle to Colab"""

# Installing Kaggle API
! pip install -q kaggle

# create a directory as kaggle
! mkdir -p ~/.kaggle

# Import API key to google colab
from google.colab import files
uploaded = files.upload()

# copy API key to kaggle directory
! cp kaggle.json ~/.kaggle/

# disable API key
! chmod 600 /root/.kaggle/kaggle.json

# list of datasets
! kaggle datasets list

# importing the dataset
! kaggle datasets download -d tongpython/cat-and-dog

# unzipping the dataset
! unzip -q /content/cat-and-dog.zip

"""# Step 3: Building the Model"""

# Creating an object (Initilizing CNN)
model = tf.keras.models.Sequential()

# Adding first CCN layer
# 1) filters (kernel/feature detectors) = 64
# 2) kernal size = 3
# 3) padding = same
# 4) activation = ReLU
# 5) input shape = (32, 32, 3)

model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu', input_shape=[32, 32, 3]))

# Adding maxpool layer
# 1) pool size = 2
# 2) strides = 2
# 3) padding = valid

model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=2, padding='valid'))

# adding second CNN layer and maxpool layer

model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))

model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=2, padding='valid'))

# Adding Flattening layer
model.add(tf.keras.layers.Flatten())

# Adding the dropout layer
model.add(tf.keras.layers.Dropout(0.4))

# Adding fully connected layer

model.add(tf.keras.layers.Dense(units=128, activation='relu'))

# Adding output layer

model.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

# Compiling the model

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

"""# Step 4: Fitting CNN to images"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

training_data_dir = '/content/training_set/training_set'
test_data_dir = '/content/test_set/test_set'

# rescale images

datagen = ImageDataGenerator(rescale=1./255)

training_set = datagen.flow_from_directory(directory=training_data_dir, target_size=(32, 32), classes=['dogs', 'cats'],
                                           class_mode = 'binary', batch_size = 20)

test_set = datagen.flow_from_directory(directory=test_data_dir, target_size=(32, 32), classes=['dogs', 'cats'],
                                           class_mode = 'binary', batch_size = 20)

len(training_set), len(test_set)

len(training_set) *20, len(test_set)*20

test_set.batch_size

history = model.fit_generator(generator=training_set, steps_per_epoch=401, epochs=20, validation_data=test_set, validation_steps=102)

"""# Step 5: Plotting the learning curve"""

def learning_curve(history, epoch):

  # training vs validation accuracy
  epoch_range = range(1, epoch+1)
  plt.plot(epoch_range, history.history['accuracy'])
  plt.plot(epoch_range, history.history['val_accuracy'])
  plt.title('Model Accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'val'], loc='upper left')
  plt.show()

  # training vs validation loss
  plt.plot(epoch_range, history.history['loss'])
  plt.plot(epoch_range, history.history['val_loss'])
  plt.title('Model Loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'val'], loc='upper left')
  plt.show()

learning_curve(history, 20)