import tensorflow as tf
from tensorflow import keras
import func
import matplotlib.pyplot as plt
import numpy as np

#test network here
'''data = keras.datasets.fashion_mnist
(train_images,train_labels) , (test_images, test_labels) = data.load_data()
train_images = train_images/255.0
test_images = train_images/255.0
print(type(train_labels))
model = keras.Sequential(
    [keras.layers.Flatten(input_shape=(28,28)),
     keras.layers.Dense(32,activation="relu"),
     keras.layers.Dense(32,activation="relu"),
     keras.layers.Dense(10,activation="softmax")]
)
model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])

model.fit(train_images,train_labels,epochs=5)'''

train_data = func.readStateRange("dataout.txt")
test_data = func.readStateRange("testout.txt")
train_images,train_labels = func.seperate(train_data)
test_images, test_labels = func.seperate(test_data)
#print(len(train_labels),len(train_images))
#print(len(test_labels),len(test_images))
#print(len(train_labels[0]))
#print(train_labels)
print(train_data[0][0])
model = keras.Sequential(
    [keras.layers.Flatten(input_shape=(5,2)),
     keras.layers.Dense(10,activation="relu"),
     keras.layers.Dense(16,activation="sigmoid")]
)
model.compile(optimizer='adam',loss="binary_crossentropy",metrics=["accuracy"])

model.fit(train_images,train_labels,epochs=2)
'''test_loss,test_acc = model.evaluate(test_images,test_labels)
print(test_acc)'''
print(test_images[0])
testData = np.array(test_images[0])
out = np.expand_dims(testData,0)
print(out)
print(model.predict(out))
#model.save("model.h5")'''
#todo fuckin, .7500? methinks something is wrong with the data generator
