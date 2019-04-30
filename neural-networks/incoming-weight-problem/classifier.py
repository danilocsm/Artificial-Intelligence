# missing implementation:
# 1 - Callbacks
# 2 - Model Save
# 3 - RandomSearch

import pandas as pd 
import numpy as np 
import tensorflow as tf
from tensorflow.keras import layers
import os

def map_label_to_vector_form(label):
    if label == 1:
        return np.array([1,0])
    else:
        return np.array([0,1])

# creates a sequential model using few parameters
def create_model(input_size, output_size):
    # the created model has 5 layers, which 3 of them are hidden
    inputs = tf.keras.Input(shape=(input_size,))
    x = layers.Dense(64, activation='relu')(inputs)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(64, activation='relu')(x)
    predictions = layers.Dense(output_size, activation='softmax')(x)
    model = tf.keras.Model(inputs=inputs, outputs=predictions)
    model.compile(
        optimizer=tf.train.AdamOptimizer(0.01),
        loss='mean_squared_error',
        metrics=['accuracy'])
    return model

# train the model without using a validation dataset
def train_model(dataset, labels, model, epochs, batch_size):

    history = model.fit(
        dataset,
        labels, 
        epochs=epochs, 
        batch_size=batch_size)
    return history 

def get_accuracy():
    pass

def save_model_weights(model, version):

    file_path = './weights/model_weights-v' + version +'.h5'
    model.save_weights(file_path, save_format='h5')

def get_set(dataset, set_size, ratio_1, ratio_2):

    label_1_dataset = dataset[dataset['incoming'] == 1]
    label_2_dataset = dataset[dataset['incoming'] == 0]
    temp_dataset_1 = label_1_dataset.sample(n=int(set_size*ratio_1),replace=True,random_state=1)
    temp_dataset_2 = label_2_dataset.sample(n=int(set_size*ratio_2),replace=True,random_state=1)
    temp_dataset_1.drop(['race'],axis=1,inplace=True)
    temp_dataset_2.drop(['race'],axis=1,inplace=True)
    temp_dataset_1.dropna(inplace=True)
    temp_dataset_2.dropna(inplace=True)
    new_dataset = pd.concat([temp_dataset_1, temp_dataset_2])
    return new_dataset

def classify_data(dataset, model, batch_size):

    prediction = model.predict(dataset,batch_size=batch_size)
    return prediction

file_path = os.getcwd() + '/' + 'pre_processed_data.csv'
dataset = pd.read_csv(file_path)
dataset.drop(['Unnamed: 0','capital-loss','capital-gain'], axis=1, inplace=True)
print(dataset.head())

train_set = get_set(dataset, 400, 0.24, 0.76)
test_set = get_set(dataset, 50, 0.24, 0.76)
feats = list(train_set.columns[:len(train_set.columns)-1])
labels = np.asarray(list(map(map_label_to_vector_form,train_set['incoming'].values)))

model = create_model(len(train_set.columns)-1, 2)
history = train_model(train_set[feats].values, labels, model, 90, 40)
# print(history.history['acc'])

version = 1

# print(dataset[dataset['incoming'] == 1].count())
# print(dataset[dataset['incoming'] == 0].count())
# train_set, test_set = split_data_into_train_test_sets(dataset) 
# model = create_model()
# model = train_model(train_set)
# predicted_data = classify_data(test_set)
# accuracy = get_accuracy(predicted_data,test_set)

# save the predicted data into a .csv file
# save_result.to_csv(path_to_file)
# print(dataset.head())