import keras
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, BatchNormalization
from keras.optimizers import Adam
import numpy as np
import random as rand
import matplotlib.pyplot as plt

# Loading the training data, test data.
(train_inputs, train_targets), (test_inputs, test_targets) = mnist.load_data()

# Preprocessing data shapes.
# Images are gray-scaled. Each image should be transformed into a 28x28x1 array.
rows = train_inputs.shape[1]
cols = train_inputs.shape[2]
train_inputs = np.reshape( train_inputs, (train_inputs.shape[0], rows, cols, 1) )
test_inputs = np.reshape( test_inputs, (test_inputs.shape[0], rows, cols, 1) )

# One-Hot encoding targets.
train_targets = np_utils.to_categorical(train_targets)
test_targets = np_utils.to_categorical(test_targets)
num_of_classes = train_targets.shape[1]

# Building & Compiling the model.
# Adding Convolutional layers.
model = Sequential()
model.add(
    Conv2D(
        filters=32, kernel_size=3, strides=1, padding='valid',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None, input_shape=(rows, cols, 1)
    )
)
model.add( BatchNormalization() )
model.add(
    Conv2D(
        filters=32, kernel_size=3, strides=1, padding='valid',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)
model.add( BatchNormalization() )
model.add(
    Conv2D(
        filters=32, kernel_size=5, strides=2, padding='same',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)
model.add( BatchNormalization() )
model.add( Dropout(rate=0.4) )

model.add(
    Conv2D(
        filters=64, kernel_size=3, strides=1, padding='valid',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)
model.add( BatchNormalization() )
model.add(
    Conv2D(
        filters=64, kernel_size=3, strides=1, padding='valid',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)
model.add( BatchNormalization() )
model.add(
    Conv2D(
        filters=64, kernel_size=5, strides=2, padding='same',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)
model.add( BatchNormalization() )
model.add( Dropout(rate=0.4) )

model.add(
    Conv2D(
        filters=128, kernel_size=4, strides=2, padding='valid',
        activation='relu', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer='l1', bias_regularizer='l1'
    )
)
model.add( BatchNormalization() )
model.add( Flatten() )

# Adding the final output layer.
model.add(
    Dense(
        units=num_of_classes, activation='softmax', kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform',
        kernel_regularizer=None, bias_regularizer=None
    )
)

model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(learning_rate=0.001),
    metrics=['accuracy']
)
print( model.summary() )

# Training the model.
batch_size = 64
epochs = 10

history = model.fit(
    x=train_inputs, y=train_targets, batch_size=batch_size, epochs=epochs, verbose=1,
    sample_weight=None, validation_data=(train_inputs, train_targets)
)

# Testing model's accuracy.
test_metrics = model.evaluate(test_inputs, test_targets, verbose=0)
test_loss, test_accuracy = test_metrics[0], test_metrics[1]
print('Test Loss:', test_loss)
print('Test Accuracy:', test_accuracy)

# Plotting Training, Validation loss.
history_dict = history.history
epoch_steps = range(1, epochs+1)

train_loss = history_dict['loss']
valid_loss = history_dict['val_loss']
plt.plot(epoch_steps, train_loss, label='Training Loss')
plt.plot(epoch_steps, valid_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Saving the model.
model.save('mnist_cnn.h5')