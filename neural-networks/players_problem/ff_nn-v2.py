import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np

def transform_label_to_vector_form(label):

   if label == 'Atacante':
      return np.array([1,0])
   elif label == 'Defensor':
      return np.array([0,1])

class MyModel(tf.keras.Model):

    def __init__(self,num_classes):

        super(MyModel, self).__init__(name='my_model')
        self.num_classes = num_classes

        self.dense_1 = layers.Dense(7,activation='sigmoid')
        self.dense_2 = layers.Dense(64,activation='sigmoid')
        self.dense_3 = layers.Dense(64,activation='sigmoid')
        self.dense_4 = layers.Dense(num_classes,activation='softmax')
    
    def call(self, inputs):

        x = self.dense_1(inputs)
        x = self.dense_2(x)
        x = self.dense_3(x)

        return self.dense_4(x)
    
    def compute_output_shape(self, input_shape):
        
        shape = tf.TensorShape(input_shape).as_list()
        shape[-1] = self.num_classes
        return tf.TensorShape(shape)

model = MyModel(2)

model.compile(
    optimizer = tf.train.AdamOptimizer(0.001),
    loss = 'categorical_crossentropy',
    metrics = ['accuracy']
)

data = pd.read_csv('/home/danilocrgm/Documents/neural_networks/players_problem/data/treino.csv')

useful_data = data[['Altura','Tecnica','Passe','Chute','Forca','Velocidade','Drible']].values
labels = data['Classe'].values

new_labels = np.asarray(list(map(transform_label_to_vector_form,labels)))

model.fit(useful_data, new_labels, epochs=50, batch_size=24)
# model.save_weights('my_model_weights-v5.h5')
json = model.to_json()
# print(json)
# import json
# import pprint
# pprint.pprint(json.loads(json))