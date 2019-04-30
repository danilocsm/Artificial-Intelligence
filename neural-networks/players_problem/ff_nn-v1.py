import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from matplotlib import pyplot

def transform_predicted_label_to_normal_label(predicted):

   if predicted[0] > predicted[1]:
      return 'Atacante'
   else:
      return 'Defensor'


def transform_label_to_vector_form(label):

   if label == 'Atacante':
      return np.array([1,0])
   elif label == 'Defensor':
      return np.array([0,1])


# Creating the model without giving any training values.
# Architeture of the network

inputs = tf.keras.Input(shape=(7,))

x = layers.Dense(64, activation='sigmoid')(inputs)
x = layers.Dense(64, activation='sigmoid')(x)
predictions = layers.Dense(2, activation='softmax')(x)

model = tf.keras.Model(inputs=inputs, outputs=predictions)

model.compile(
   optimizer=tf.train.AdamOptimizer(0.001),
   loss='categorical_crossentropy',
   metrics=['accuracy']
)
# Reading and pre-processing the data

data = pd.read_csv('/home/danilocrgm/Documents/neural_networks/players_problem/data/treino.csv')

useful_data = data[['Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']].values
labels = data['Classe'].values

new_labels = np.asarray(list(map(transform_label_to_vector_form,labels)))

# Training the model
history = model.fit(useful_data, new_labels, epochs=60, batch_size=24)
# model.save('my_model-v2.h5')
# Plotting 
pyplot.plot(history.history['acc'],label='train')
pyplot.title('lrate',pad=-50)
# Loading unclassified data
pyplot.show()
'''
unclassified_data = pd.read_csv('/home/danilocrgm/Documents/neural_networks/players_problem/data/nao_classificados.csv')

unclassified_data_values = unclassified_data[['Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']].values

preds = model.predict(unclassified_data_values, batch_size=24)
# print(preds)
new_preds = list(map(transform_predicted_label_to_normal_label,preds))
# print(new_preds)

unclassified_data['Classe'] = new_preds

unclassified_data.to_csv('/home/danilocrgm/Documents/neural_networks/players_problem/data/classifcados.csv')
'''
