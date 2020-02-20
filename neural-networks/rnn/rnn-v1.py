import tensorflow as tf
import numpy as np
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb

train, test = imdb.load_data(path='data/imdb.pkl',
                             n_words=30000,
                             valid_portion=0.1)
trainX, trainY = train
testX, testY = test
trainX = pad_sequences(trainX, maxlen=500, value=0.)
testX = pad_sequences(testX, maxlen=500, value=0.)
trainY = to_categorical(trainY, nb_classes=2)
testY = to_categorical(testY, nb_classes=2)

class IMDBDataset():
    def __init__(self, X, Y):
        self.num_examples = len(X)
        self.inputs = X
        self.tags = Y
        self.ptr = 0

    def minibatch(self, size):
        ret = None
        if self.ptr + size < len(self.inputs):
            ret = self.inputs[self.ptr:self.ptr + size], \
                  self.tags[self.ptr:self.ptr + size]
        else:
            ret = np.concatenate((self.inputs[self.ptr:],
                                  self.inputs[:size-len(self.inputs[self.ptr:])])), \
                  np.concatenate((self.tags[self.ptr:],self.tags[:size-len(self.tags[self.ptr:])]))
        self.ptr = (self.ptr + size) % len(self.inputs)
        return ret

train = IMDBDataset(trainX, trainY)
test = IMDBDataset(testX, testY)

def embedding_layer(input, weight_shape):
    weight_init = tf.random_normal_initializer(stddev=(1.0/weight_shape[0])**0.5)
    E = tf.get_variable("E", weight_shape, initializer=weight_init)
    incoming = tf.cast(input, tf.int32)
    embeddings = tf.nn.embedding_lookup(E, incoming)
    return embeddings

def lstm(input, hidden_dim, keep_prob, phase_train):
    lstm = tf.nn.rnn_cell.BasicLSTMCell(hidden_dim)
    dropout_lstm = tf.nn.rnn_cell.DropoutWrapper(lstm,
                                                 input_keep_prob=keep_prob,
                                                 output_keep_prob=keep_prob)
    stacked_lstm = tf.nn.rnn_cell.MultiRNNCell([dropout_lstm] * 2,
                                               state_is_tuple=True)
    lstm_outputs, state = tf.nn.dynamic_rnn(dropout_lstm,
                                            input,dtype=tf.float32)
    return tf.squeeze(tf.slice(lstm_outputs,
                               [0, tf.shape(lstm_outputs)[1]-1,0],
                               [tf.shape(lstm_outputs[0]), 1, tf.shape(lstm_outputs)[2]]))

def inference(input, phase_train):
    embedding = embedding_layer(input, [30000, 512])
    lstm_output = lstm(embedding, 512, 0.5, phase_train)
    output = tf.layer(lstm_output, [512, 2], [2], phase_train)
