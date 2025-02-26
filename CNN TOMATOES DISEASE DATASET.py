#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:97b3a3b1-a0f6-496a-83e4-26a0b561d80a.png)

# In[16]:


import tensorflow as tf 
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import seaborn as sns
from tensorflow.keras import Sequential
import pathlib
import matplotlib.image as img
import imageio
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import *
import os


# In[7]:


# train_path=r'C:/Shamba/PlantVillage'
# train_path = '/home/dominic/Shamba/PlantVillage'
# images_classes = os.listdir(train_path)
# print(images_classes)
train_path = '/home/dominic/Shamba/PlantVillage'
val_path = '/home/dominic/Shamba/plantvillage_val'

images_classes = os.listdir(train_path)


# In[9]:


images_classes = os.listdir(train_path)
images_classes


# In[21]:


dataset = tf.keras.utils.image_dataset_from_directory(
    train_path,
    batch_size=32,
    image_size=(256, 256),
    seed=123,
    shuffle=True
)


# In[5]:


plt.figure(figsize=(15, 15))
for image, lable in dataset.take(1):
    for i in range(10):
        ax = plt.subplot(5, 2, i + 1)
        plt.imshow(image[i].numpy().astype("uint8"))
        plt.title(images_classes[lable[i].numpy()])
        plt.axis('OFF')

# VISUALIZING THE IMAGES OF THE MODEL 


# # Image preprocessing 

# In[6]:


# data_generator = ImageDataGenerator(rescale=(1/255)) # performing scaling on the pixels of the image 
data_generator = ImageDataGenerator(rescale=1/255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')


# In[7]:


train_data = data_generator.flow_from_directory(train_path,
                                               target_size = (224, 224),
                                               batch_size = 16)


# In[9]:


test_data = data_generator.flow_from_directory(val_path,
                                              target_size=(224,224),
                                              batch_size= 16)


# <!-- MODEL BUILDING  -->

# # MODEL BUILDING 

# In[10]:


#CNN Model
model = Sequential()
#add Conv layer with filters, kernel, padding, activation, input shape
model.add(Conv2D(filters = 32, kernel_size = 3, padding = 'same',
                activation = 'relu', input_shape = [224,224,3])) #feature extraction

#add pooling layer ---> dimensionality reduction 
model.add(MaxPooling2D(pool_size = (2,2)))

#add batch normalization layer
model.add(Dropout(0.3))

#add Conv layer with filters, kernel, padding, activation
model.add(Conv2D(filters = 64, kernel_size = 3, padding = 'same',activation = 'relu')) #feature extraction
#add pooling layer ---> dimensionality reduction 
model.add(MaxPooling2D())

#add batch normalization layer
#model.add(BatchNormalization())
model.add(Dropout(0.3))


#add Conv layer with filters, kernel, padding, activation
model.add(Conv2D(filters = 128, kernel_size = 3, padding = 'same',activation = 'relu')) #feature extraction

#add pooling layer ---> dimensionality reduction 
model.add(MaxPooling2D())
# add dropout layer
model.add(Dropout(0.3))

#add Flatten layer ---> 1D
model.add(Flatten())

#add Fully Connnected Layers
model.add(Dense(128, activation = 'relu'))
model.add(Dense(128, activation = 'relu'))
#add output layer
model.add(Dense(12, activation = 'softmax')) #12 classes


# In[46]:


model.summary()


# In[48]:

optimizer = Adam(learning_rate=0.0001)
#compile model
model.compile(optimizer = optimizer,
                loss = 'categorical_crossentropy',
                metrics = ['accuracy'])



# In[50]:
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

#fit model
model_history = model.fit(train_data,
                         epochs = 12,
                         validation_data = test_data,
                         callbacks=[lr_scheduler, early_stopping])


# # Model Evaluation 

# In[53]:

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(model_history.history['accuracy'], label = 'Train Accuracy')
plt.plot(model_history.history['val_accuracy'], label = 'Validation Accuracy')
plt.title('Model Accuracy')
plt.legend()


# In[55]:


plt.subplot(1, 2, 2)
plt.plot(model_history.history['loss'], label = 'Train Loss')
plt.plot(model_history.history['val_loss'], label = 'Validation Loss')
plt.title('Model Loss')
plt.legend()
plt.show()


# In[57]:


model.evaluate(test_data)


# In[60]:


model.evaluate(train_data)


# In[12]:
model.save('disease_detection_model.keras')


