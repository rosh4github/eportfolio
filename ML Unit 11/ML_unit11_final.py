'''
To create a Neural Network model for object recognition using the CIFAR-10 dataset, we'll use Python with TensorFlow and Keras. Below is the code to define, train, and evaluate the model.
    
Step-by-Step Guide
Import Libraries
Load and Preprocess Data
Define the Model
Compile the Model
Train the Model
Evaluate the Model
'''

### IMPORT LIBRARIES

import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

### LOAD AND PREPROCESS DATA

# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize pixel values to be between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

# Convert class vectors to binary class matrices
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Split training data into training and validation sets

# Partitioning: Method used to partition the validation set from the training data
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

### DEFINE THE MODEL

model = Sequential()

## Architecture of the Artificial Neural Network

# Convolutional Layers:

# First Convolutional Layer
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3))) # Activation function - ReLU (Rectified Linear Unit)
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Second Convolutional Layer
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Third Convolutional Layer
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Flatten the layers
model.add(Flatten())

## Fully Connected Layers

# Dense Layer
model.add(Dense(512, activation='relu'))

# Dropout Layer
model.add(Dropout(0.5))

# Output Layer
model.add(Dense(10, activation='softmax')) # Activation function - Softmax

### COMPILE THE MODEL

# Categorical Crossentropy (Loss function)
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

### TRAIN THE MODEL

# Number of epochs used in the modeling process
history = model.fit(x_train, y_train, epochs=25, batch_size=64,
                    validation_data=(x_val, y_val))


### EVALUATE THE MODEL

# Evaluate on test data
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc}')

# Plot training & validation accuracy and loss
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Training and Validation Loss')

plt.show()


''' 
EXPLANATION OF CHOICES

Activation Function: 
ReLU is used in hidden layers to introduce non-linearity. Softmax is used in the output layer for multiclass classification.

Loss Function: 
Categorical Crossentropy is used as it is suitable for multi-class classification problems.

Optimizer: 
Adam optimizer is chosen for its efficiency and adaptability.

Dropout Layers: 
Added to prevent overfitting. 
'''


'''
ADDITIONAL TIPS

Hyperparameter Tuning: 
You can experiment with different numbers of layers, filters, kernel sizes, and epochs to improve performance.

Data Augmentation: 
You can add data augmentation to increase the diversity of the training data and improve generalization.
'''

